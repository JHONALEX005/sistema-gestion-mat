"""Servidor local del prototipo MAT. Solo usa la biblioteca estándar de Python."""

from __future__ import annotations

import json
import os
import re
import sqlite3
import uuid
from contextlib import closing
from datetime import date, timedelta
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parent.parent
STATIC = Path(__file__).resolve().parent / "static"
DB_PATH = Path(os.environ.get("MAT_DB_PATH", str(ROOT / "data" / "mat.sqlite3")))
EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def connect() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH, timeout=10)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with closing(connect()) as db, db:
        db.executescript(
            """
            CREATE TABLE IF NOT EXISTS exhibitions (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                active INTEGER NOT NULL DEFAULT 1 CHECK (active IN (0, 1))
            );
            CREATE TABLE IF NOT EXISTS slots (
                id INTEGER PRIMARY KEY,
                exhibition_id INTEGER NOT NULL REFERENCES exhibitions(id),
                visit_date TEXT NOT NULL,
                start_time TEXT NOT NULL,
                capacity INTEGER NOT NULL CHECK (capacity > 0),
                active INTEGER NOT NULL DEFAULT 1 CHECK (active IN (0, 1)),
                UNIQUE (exhibition_id, visit_date, start_time)
            );
            CREATE TABLE IF NOT EXISTS reservations (
                id INTEGER PRIMARY KEY,
                code TEXT NOT NULL UNIQUE,
                slot_id INTEGER NOT NULL REFERENCES slots(id),
                visitor_name TEXT NOT NULL,
                visitor_email TEXT NOT NULL,
                party_size INTEGER NOT NULL CHECK (party_size BETWEEN 1 AND 4),
                status TEXT NOT NULL DEFAULT 'active'
                    CHECK (status IN ('active', 'cancelled')),
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                cancelled_at TEXT
            );
            CREATE INDEX IF NOT EXISTS idx_reservations_slot_status
                ON reservations(slot_id, status);
            """
        )
        if db.execute("SELECT COUNT(*) FROM exhibitions").fetchone()[0] == 0:
            db.executemany(
                "INSERT INTO exhibitions (title, description) VALUES (?, ?)",
                [
                    ("Colección de muestra", "Contenido demostrativo para explorar el catálogo."),
                    ("Recorrido de muestra", "Contenido demostrativo para practicar una reserva."),
                ],
            )
        if db.execute("SELECT COUNT(*) FROM slots").fetchone()[0] == 0:
            tomorrow = date.today() + timedelta(days=1)
            db.executemany(
                "INSERT INTO slots (exhibition_id, visit_date, start_time, capacity) "
                "VALUES (?, ?, ?, ?)",
                [
                    (1, tomorrow.isoformat(), "10:00", 12),
                    (1, (tomorrow + timedelta(days=1)).isoformat(), "14:00", 12),
                    (2, (tomorrow + timedelta(days=2)).isoformat(), "11:00", 8),
                ],
            )


def exhibitions() -> list[dict]:
    with closing(connect()) as db, db:
        rows = db.execute(
            "SELECT id, title, description FROM exhibitions WHERE active = 1 ORDER BY id"
        ).fetchall()
    return [dict(row) for row in rows]


def slots() -> list[dict]:
    with closing(connect()) as db, db:
        rows = db.execute(
            """
            SELECT s.id, s.exhibition_id, e.title AS exhibition_title,
                   s.visit_date, s.start_time, s.capacity,
                   s.capacity - COALESCE(SUM(CASE WHEN r.status = 'active'
                                               THEN r.party_size ELSE 0 END), 0) AS available
            FROM slots s
            JOIN exhibitions e ON e.id = s.exhibition_id
            LEFT JOIN reservations r ON r.slot_id = s.id
            WHERE s.active = 1 AND e.active = 1 AND s.visit_date >= ?
            GROUP BY s.id
            ORDER BY s.visit_date, s.start_time, s.id
            """,
            (date.today().isoformat(),),
        ).fetchall()
    return [dict(row) for row in rows]


def create_reservation(payload: dict) -> dict:
    name = str(payload.get("name", "")).strip()
    email = str(payload.get("email", "")).strip().lower()
    try:
        slot_id = int(payload.get("slot_id"))
        party_size = int(payload.get("party_size"))
    except (ValueError, TypeError):
        raise ValueError("Selecciona un horario y un número de visitantes válidos.") from None
    if not (2 <= len(name) <= 100):
        raise ValueError("El nombre debe tener entre 2 y 100 caracteres.")
    if len(email) > 254 or not EMAIL_PATTERN.fullmatch(email):
        raise ValueError("Escribe un correo electrónico válido.")
    if not 1 <= party_size <= 4:
        raise ValueError("Una reserva admite entre 1 y 4 visitantes.")

    with closing(connect()) as db, db:
        db.execute("BEGIN IMMEDIATE")
        slot = db.execute(
            """
            SELECT s.id, s.visit_date, s.capacity
            FROM slots s JOIN exhibitions e ON e.id = s.exhibition_id
            WHERE s.id = ? AND s.active = 1 AND e.active = 1
            """,
            (slot_id,),
        ).fetchone()
        if slot is None or slot["visit_date"] < date.today().isoformat():
            raise ValueError("El horario ya no está disponible.")
        used = db.execute(
            "SELECT COALESCE(SUM(party_size), 0) FROM reservations "
            "WHERE slot_id = ? AND status = 'active'",
            (slot_id,),
        ).fetchone()[0]
        if used + party_size > slot["capacity"]:
            raise ValueError("No hay cupos suficientes para ese horario.")
        code = uuid.uuid4().hex[:16].upper()
        db.execute(
            "INSERT INTO reservations "
            "(code, slot_id, visitor_name, visitor_email, party_size) "
            "VALUES (?, ?, ?, ?, ?)",
            (code, slot_id, name, email, party_size),
        )
    return {"code": code, "slot_id": slot_id, "party_size": party_size}


def cancel_reservation(payload: dict) -> dict:
    code = str(payload.get("code", "")).strip().upper()
    email = str(payload.get("email", "")).strip().lower()
    if not code or not email:
        raise ValueError("Ingresa el código y el correo de la reserva.")
    with closing(connect()) as db, db:
        db.execute("BEGIN IMMEDIATE")
        cursor = db.execute(
            """
            UPDATE reservations
            SET status = 'cancelled', cancelled_at = CURRENT_TIMESTAMP
            WHERE code = ? AND visitor_email = ? AND status = 'active'
            """,
            (code, email),
        )
        if cursor.rowcount == 0:
            raise ValueError("No se encontró una reserva activa con esos datos.")
    return {"code": code, "status": "cancelled"}


class Handler(BaseHTTPRequestHandler):
    def send_json(self, status: HTTPStatus, data: dict | list) -> None:
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        path = urlsplit(self.path).path
        if path == "/health":
            self.send_json(HTTPStatus.OK, {"status": "ok"})
        elif path == "/api/exhibitions":
            self.send_json(HTTPStatus.OK, exhibitions())
        elif path == "/api/slots":
            self.send_json(HTTPStatus.OK, slots())
        else:
            files = {
                "/": ("index.html", "text/html; charset=utf-8"),
                "/app.js": ("app.js", "text/javascript; charset=utf-8"),
                "/styles.css": ("styles.css", "text/css; charset=utf-8"),
            }
            if path not in files:
                self.send_error(HTTPStatus.NOT_FOUND)
                return
            filename, content_type = files[path]
            body = (STATIC / filename).read_bytes()
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    def do_POST(self) -> None:
        path = urlsplit(self.path).path
        if path not in ("/api/reservations", "/api/reservations/cancel"):
            self.send_json(HTTPStatus.NOT_FOUND, {"error": "Ruta no encontrada."})
            return
        if "application/json" not in self.headers.get("Content-Type", ""):
            self.send_json(HTTPStatus.UNSUPPORTED_MEDIA_TYPE, {"error": "Envía JSON."})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= 8192:
                raise ValueError("La solicitud está vacía o es demasiado grande.")
            payload = json.loads(self.rfile.read(length))
            if not isinstance(payload, dict):
                raise ValueError("La solicitud debe contener un objeto JSON.")
            if path == "/api/reservations":
                result = create_reservation(payload)
                self.send_json(HTTPStatus.CREATED, result)
            else:
                result = cancel_reservation(payload)
                self.send_json(HTTPStatus.OK, result)
        except (ValueError, json.JSONDecodeError) as exc:
            self.send_json(HTTPStatus.BAD_REQUEST, {"error": str(exc)})


def main() -> None:
    initialize_database()
    host = os.environ.get("MAT_HOST", "127.0.0.1")
    port = int(os.environ.get("MAT_PORT", "8000"))
    server = ThreadingHTTPServer((host, port), Handler)
    print(f"MAT disponible en http://{host}:{port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()

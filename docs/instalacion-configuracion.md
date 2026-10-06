# Instalación, configuración y ejecución

## Requisitos

- Python 3.12.
- Navegador con JavaScript.
- Puerto local 8000 libre o un puerto alternativo.

No se necesita instalar paquetes de Python ni un servidor de base de datos. SQLite viene con Python.

## Inicio en Windows

1. Abra PowerShell en la carpeta raíz `sistema-gestion-mat`.
2. Compruebe Python con `python --version` o `py -3.12 --version`.
3. Ejecute `python src/server.py` o `py -3.12 src/server.py`.
4. Abra `http://127.0.0.1:8000` en el navegador.
5. Detenga el servidor con `Ctrl+C`.

## Inicio en macOS o Linux

Desde la raíz del repositorio:

```sh
python3 --version
python3 src/server.py
```

Después abra `http://127.0.0.1:8000`.

## Primer inicio y persistencia

El programa crea `data/mat.sqlite3` y añade datos demostrativos si la base no tiene exposiciones ni horarios. Las reservas permanecen al reiniciar. Para comenzar de nuevo, detenga el servidor y elimine **únicamente** `data/mat.sqlite3`; al iniciarlo se creará otra base con los datos de muestra. No borre una base que contenga información que necesite conservar.

## Configuración

| Variable | Valor predeterminado | Uso |
| --- | --- | --- |
| `MAT_HOST` | `127.0.0.1` | Dirección donde escucha el servidor. Manténgala local para esta demostración. |
| `MAT_PORT` | `8000` | Puerto HTTP. |
| `MAT_DB_PATH` | `data/mat.sqlite3` dentro del proyecto | Ruta del archivo SQLite. |

Ejemplo de puerto alternativo en PowerShell:

```powershell
$env:MAT_PORT = '8001'
python src/server.py
```

En macOS o Linux: `MAT_PORT=8001 python3 src/server.py`.

## Problemas frecuentes

- **«python no se reconoce»**: instale Python 3.12 o utilice el comando `py -3.12` si está disponible.
- **«Address already in use»**: cierre el servidor anterior o cambie `MAT_PORT`.
- **No aparecen horarios**: los datos iniciales solo se crean cuando la tabla de horarios está vacía; si transcurrieron las fechas de muestra, reinicie la base como se explicó arriba.
- **No se puede escribir la base**: ejecute desde una carpeta donde tenga permiso para crear `data/`, o configure `MAT_DB_PATH` con una ruta escribible.

## Comprobación de integración continua

El archivo `.github/workflows/ci.yml` compila la sintaxis Python con `python -m compileall -q src` en cada `push` y solicitud de cambios. Puede ejecutar ese mismo comando localmente. Esta evaluación no requiere pruebas automatizadas; `tests/` queda reservado para una entrega posterior.


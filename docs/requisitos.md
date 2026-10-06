# Requisitos y alcance actual

Fecha de corte: 5 de octubre de 2026. Este documento describe el prototipo entregado en este repositorio. El proyecto de aula original propone más capacidades; las que no están en el código figuran como **previstas** y no se presentan como funcionales.

## Requisitos funcionales

| ID | Requisito | Estado | Evidencia en el repositorio |
| --- | --- | --- | --- |
| RF-01 | Consultar el título y la descripción de exposiciones activas. | Implementado | `GET /api/exhibitions` e interfaz principal |
| RF-02 | Consultar horarios futuros y cupos restantes. | Implementado | `GET /api/slots` y selector de horarios |
| RF-03 | Crear una reserva de 1 a 4 personas cuando exista cupo. | Implementado | `POST /api/reservations` |
| RF-04 | Obtener un código único al confirmar la reserva. | Implementado | Respuesta de creación de reserva |
| RF-05 | Cancelar una reserva activa con su código y correo; liberar cupos. | Implementado | `POST /api/reservations/cancel` |
| RF-06 | Crear cuentas e iniciar sesión. | Previsto | Sin código |
| RF-07 | Comprar y pagar entradas. | Previsto | Sin código ni pasarela |
| RF-08 | Descargar entradas digitales. | Previsto | Sin código |
| RF-09 | Administrar exposiciones y horarios desde una interfaz protegida. | Previsto | Solo existen datos de muestra cargados al iniciar |
| RF-10 | Consultar la agenda de guías. | Previsto | Sin código |
| RF-11 | Validar entradas y registrar asistencia. | Previsto | Sin código |
| RF-12 | Generar reportes de ventas y asistencia. | Previsto | Sin código |

**Refinamiento del flujo de reservas:** el material previo mencionaba consulta de disponibilidad y cancelación, pero el paso de crear una reserva no quedaba explícito. RF-03 identifica esa acción y la implementa en este prototipo. La correspondencia con los números definitivos de historias de usuario de la Entrega 1 debe confirmarla el equipo porque los documentos recibidos no contienen una versión única y completa del backlog.

## Requisitos no funcionales

| ID | Requisito comprobable para este prototipo | Estado / evidencia |
| --- | --- | --- |
| RNF-01 | La interfaz debe poder usarse en pantallas de escritorio y móvil. | Implementado mediante diseño adaptable en `src/static/styles.css`. |
| RNF-02 | Las reservas no deben superar la capacidad de un horario. | Implementado mediante transacción SQLite con `BEGIN IMMEDIATE`. |
| RNF-03 | Los datos locales deben conservarse al reiniciar el servidor. | Implementado con archivo SQLite en `data/mat.sqlite3`. |
| RNF-04 | El proyecto debe poder ejecutarse con Python 3.12 sin instalar paquetes de terceros. | Implementado; `src/server.py` usa biblioteca estándar. |
| RNF-05 | El repositorio debe compilar su código Python automáticamente en cada envío de cambios. | Configurado en `.github/workflows/ci.yml`; la ejecución remota se verá al publicarlo en GitHub. |
| RNF-06 | La aplicación debe contar con autenticación y protección para datos personales antes de usarse públicamente. | Pendiente; por eso el uso actual se limita a una demostración local. |

## Trazabilidad

| Necesidad del usuario | Función actual | Requisito | Sección funcional |
| --- | --- | --- | --- |
| Conocer exposiciones | Catálogo público | RF-01 | Flujo 1 |
| Elegir una visita con cupos | Lista de horarios | RF-02 | Flujo 2 |
| Confirmar asistencia | Reserva y código | RF-03, RF-04 | Flujo 3 |
| Liberar un cupo | Cancelación | RF-05 | Flujo 4 |

Los estados previstos pueden revisarse con el equipo y la docente antes de ampliar el software.


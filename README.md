# Sistema de Gestión MAT

Prototipo académico local para consultar exposiciones de muestra y gestionar cupos de visitas. Se creó a partir del alcance inicial del proyecto de aula. **Los nombres y horarios cargados automáticamente son datos demostrativos; no representan la programación real de un museo.**

## Estado actual

Funciona:

- Consulta pública de exposiciones activas.
- Consulta de horarios futuros y cupos disponibles.
- Creación de reservas de 1 a 4 personas, con código de confirmación.
- Cancelación mediante código y correo; el cupo se libera.

Está previsto, sin implementación: cuentas de usuario, pagos, entradas digitales, administración de exposiciones y horarios desde la interfaz, agenda de guías, validación de acceso y reportes. Las [historias y requisitos](docs/requisitos.md) distinguen ambos estados.

## Inicio rápido

Requiere Python 3.12. No hay paquetes externos que instalar.

```text
python src/server.py
```

En Windows, si `python` no está disponible, pruebe `py -3.12 src/server.py`. Abra `http://127.0.0.1:8000` en el navegador. Detenga el servidor con `Ctrl+C`. En el primer inicio se crea `data/mat.sqlite3` con contenido de muestra. La carpeta `data/` se ignora en Git.

Las [instrucciones completas](docs/instalacion-configuracion.md) explican configuración, reinicio de datos y solución de problemas.

## Documentación

- [Requisitos y alcance](docs/requisitos.md)
- [Funciones para el usuario](docs/documentacion-funcional.md)
- [Arquitectura, componentes e interfaces](docs/arquitectura.md)
- [Modelo de datos](docs/modelo-datos.md)
- [Instalación y configuración](docs/instalacion-configuracion.md)
- [Control de cambios y observaciones](docs/control-cambios.md)
- [Evidencia de funcionamiento local](docs/evidencia-ejecucion.md)
- [Estado de la entrega](ENTREGA.md)
- [Publicación en GitHub](PUBLICAR_EN_GITHUB.md)

## Estructura

```text
.
├── .github/workflows/ci.yml  # Compilación de sintaxis automática
├── docs/                     # Documentación técnica y funcional
├── src/server.py             # Servidor y persistencia SQLite
├── src/static/              # Interfaz web
├── tests/README.md           # Espacio para pruebas futuras
├── .gitignore
├── ENTREGA.md
└── README.md
```

## Integración continua y versiones

El flujo de GitHub Actions se ejecuta al hacer `push` o abrir una solicitud de cambios. Selecciona Python 3.12 y compila los archivos de `src/` para verificar su sintaxis. No implementa ni ejecuta pruebas. Los commits del repositorio local separan la aplicación, la documentación y la configuración de integración continua.

## Límite de uso

Esta versión está preparada para ejecución **local y académica**. No incluye autenticación ni un proceso de producción para almacenar datos personales. Para la demostración, utilice nombres y correos ficticios.

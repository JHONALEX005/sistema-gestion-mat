# Evidencia de funcionamiento local

El 5 de octubre de 2026 se inició el servidor con una base SQLite nueva de demostración y se comprobaron manualmente las rutas principales. Esto no constituye una suite de pruebas; la carpeta `tests/` permanece sin casos de prueba, tal como permite la Evaluación 3.

| Acción observada | Resultado |
| --- | --- |
| Consultar `/health`. | El servidor respondió `ok`. |
| Consultar `/api/exhibitions`. | Se recibieron 2 exposiciones de muestra. |
| Consultar `/api/slots`. | Se recibieron 3 horarios de muestra. |
| Reservar 2 personas en un horario de 12 cupos. | El cupo disponible pasó de 12 a 10 y se devolvió un código. |
| Cancelar con el código y el mismo correo. | El estado pasó a `cancelled` y el cupo volvió a 12. |
| Compilar los archivos Python de `src/`. | El comando `python -m compileall -q src` terminó sin errores. |

Las observaciones corresponden a datos ficticios locales. La ejecución del flujo de GitHub Actions podrá comprobarse después de publicar el repositorio remoto.


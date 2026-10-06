# Documentación funcional

La interfaz está dirigida a un visitante que utiliza el prototipo local en su navegador. Los datos de exposiciones y horarios son demostrativos. No se envían correos ni se cobran entradas.

## Flujo 1. Consultar exposiciones

- **Condición:** servidor iniciado.
- **Pasos:** abrir `http://127.0.0.1:8000`; leer las tarjetas bajo «Exposiciones».
- **Resultado:** aparecen el título y la descripción de cada exposición activa.
- **Si no hay datos:** se muestra «No hay exposiciones activas».
- **Requisitos:** RF-01.

## Flujo 2. Consultar disponibilidad

- **Condición:** existen horarios futuros activos.
- **Pasos:** en «Elige una visita», abrir el selector de fecha y horario.
- **Resultado:** cada opción indica exposición, fecha, hora y cupos restantes. Los horarios sin cupos no se ofrecen para reservar.
- **Requisitos:** RF-02.

## Flujo 3. Crear reserva

- **Condición:** hay un horario con cupos y el visitante tiene un correo de demostración.
- **Pasos:** elegir horario, escribir nombre y correo, indicar entre 1 y 4 visitantes y pulsar «Confirmar reserva».
- **Resultado:** la pantalla muestra un código de 16 caracteres. El visitante debe guardarlo para cancelar. El cupo visible disminuye.
- **Si no hay cupos suficientes:** aparece un mensaje y no se crea la reserva.
- **Requisitos:** RF-03, RF-04.

## Flujo 4. Cancelar reserva

- **Condición:** existe una reserva activa y se conoce su código y correo.
- **Pasos:** en «¿No puedes asistir?», escribir el código y el mismo correo; pulsar «Cancelar reserva».
- **Resultado:** aparece confirmación y el cupo regresa al horario.
- **Si los datos no coinciden o ya se canceló:** aparece un mensaje sin modificar cupos.
- **Requisito:** RF-05.

## Alcance que aún no se muestra en la interfaz

No existe registro o inicio de sesión, pago, descarga de entrada, mantenimiento administrativo, agenda de guías, control de ingreso ni reportes. Estas ideas aparecen como previstas en [requisitos.md](requisitos.md).

## Evidencia

El repositorio incluye una interfaz funcional y rutas HTTP descritas en [arquitectura.md](arquitectura.md). Las capturas que se presenten a la docente deben tomarse de la aplicación en ejecución con datos de muestra; no se incluyen imágenes simuladas como evidencia de funcionamiento.


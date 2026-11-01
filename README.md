# Sistema de reserva de canchas

¿Alguna vez quisiste jugar fútbol o baloncesto en el campus y no sabías si la cancha estaba libre? Esta app resuelve justo eso: un lugar sencillo donde cualquier estudiante puede reservar una cancha, ver qué horarios están ocupados y cambiar o cancelar su reserva si le surge algo.

La hicimos para la práctica **"Gestión de un proyecto de software asistida por IA"**. Lo importante de la práctica no era programar algo gigante, sino aprender a organizar un proyecto de software de principio a fin (backlog, sprints, riesgos, tablero en Jira). Por eso el sistema es un CRUD sencillo, pero completo y funcional.

## Qué se puede hacer

- **Crear una reserva:** eliges la cancha, la fecha, la hora y cuánto tiempo la necesitas.
- **Ver todas las reservas** en tarjetas de colores, una por deporte.
- **Buscar y filtrar** por nombre, matrícula, cancha, estado o fecha, y ordenar como prefieras.
- **Editar** una reserva si cambian los planes.
- **Cancelar** una reserva (queda guardada, pero la cancha se libera) y **reactivarla** si te arrepientes.
- **Eliminar** una reserva definitivamente.
- **Ver el detalle** de cualquier reserva.
- **Ver la demanda por cancha**, para saber cuál es la más pedida.
- **Exportar todo a CSV** y abrirlo en Excel.
- **Cargar datos de ejemplo** con un clic, útil para probar o hacer capturas.

## Las reglas que cuida el sistema

Para que nadie se pise con otro, la app no deja:

- Dejar campos obligatorios vacíos.
- Reservar en una fecha o una hora que ya pasó.
- Reservar fuera del horario de las canchas (de 7:00 a 22:00).
- Reservar una cancha que ya está ocupada, aunque los horarios solo se crucen un poco. Por ejemplo, si alguien tiene la cancha de 10:00 a 11:00, no se puede reservar de 10:30 a 11:30.

## Canchas disponibles

Fútbol, baloncesto, voleibol y tenis.

## Cómo probarlo en tu computadora

Necesitas tener **Python** instalado.

1. Descarga o clona el repositorio:

```
git clone https://github.com/yaugepedro/Sistema-de-reserva-de-canchas.git
cd Sistema-de-reserva-de-canchas
```

2. Instala Flask, que es lo único que usa:

```
pip install -r requirements.txt
```

3. Arranca la app:

```
py app.py
```

(En Mac o Linux es `python3 app.py`.)

4. Abre el navegador en **http://127.0.0.1:5000** y listo. Pulsa **Cargar ejemplos** si quieres verla con datos desde el primer momento.

Para apagarla, vuelve a la terminal y presiona **Ctrl + C**.

## Un detalle importante

Esta versión **no usa base de datos**: las reservas viven en la memoria del programa. Eso significa que cuando apagas la app, o cuando guardas un cambio en el código con la app encendida, las reservas se borran. Lo hicimos así a propósito para mantenerlo simple, ya que el foco de la práctica era la gestión del proyecto y no el almacenamiento. Si en el futuro quisiéramos que los datos se guarden, sería una de las primeras mejoras (ya la dejamos pensada en el backlog).

## Cómo está organizado el proyecto

```
├── app.py               Aquí está toda la lógica: rutas, validaciones y reglas
├── requirements.txt     Lo que hay que instalar (solo Flask)
├── templates/           Las pantallas (HTML)
│   ├── base.html        La estructura común: cabecera y mensajes
│   ├── lista.html       Pantalla principal con las reservas y filtros
│   ├── formulario.html  Formulario para crear y editar
│   └── detalle.html     Detalle de una reserva
└── static/
    └── style.css        Los colores y el diseño
```

## Con qué está hecho

- **Python** y **Flask** para el servidor.
- **HTML y CSS** para las pantallas, sin librerías extra.
- **Jira** para gestionar el backlog y los sprints.
- Apoyo de **IA** para redactar el acta, las historias de usuario y la matriz de riesgos. Todo lo que generó la IA fue revisado y corregido por el equipo; esos detalles están documentados en la entrega de la práctica.

## Lo que se queda para más adelante

- Que las reservas se guarden en una base de datos.
- Inicio de sesión para administradores.
- Envío de un correo de confirmación al reservar.
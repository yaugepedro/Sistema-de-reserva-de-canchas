# Sistema de reserva de canchas

¿Alguna vez quisiste jugar fútbol o baloncesto en el campus y no sabías si la cancha estaba libre? Esta aplicación resuelve ese problema. Es un sistema sencillo donde los estudiantes pueden reservar una cancha, consultar los horarios ocupados y modificar o cancelar sus reservas cuando lo necesiten.

Desarrollamos esta aplicación para la práctica **«Gestión de un proyecto de software asistida por IA»** del Instituto Tecnológico de las Américas (ITLA).

La actividad se concentra en aprender a organizar y administrar un proyecto de software mediante Scrum y Jira. Por eso trabajamos con un sistema CRUD que permite poner en práctica la planificación, las historias de usuario, los sprints, la gestión de riesgos y el seguimiento de las actividades.

## Qué se puede hacer

- **Crear una reserva:** seleccionar una cancha, fecha, hora y duración.
- **Consultar reservas:** visualizar las reservas registradas en tarjetas organizadas por deporte.
- **Buscar y filtrar:** encontrar reservas por nombre, matrícula, cancha, estado o fecha.
- **Ordenar reservas:** organizar los resultados por fecha, nombre o registro más reciente.
- **Editar reservas:** modificar los datos de una reserva existente.
- **Cancelar reservas:** cambiar su estado a cancelada sin eliminar la información.
- **Reactivar reservas:** volver a activar una reserva cancelada cuando el horario esté disponible.
- **Eliminar reservas:** borrar definitivamente un registro.
- **Ver detalles:** consultar la información completa de una reserva.
- **Consultar estadísticas:** visualizar la cantidad de reservas y la demanda por cancha.
- **Exportar a CSV:** descargar los registros para consultarlos en Excel.
- **Cargar datos de ejemplo:** generar reservas de prueba para conocer el funcionamiento del sistema.

## Reglas del sistema

Para mantener organizadas las reservas, la aplicación realiza varias comprobaciones antes de guardar la información.

- Los campos obligatorios deben estar completos.
- No se permiten reservas en fechas anteriores a la actual.
- No se pueden seleccionar horas que ya hayan pasado.
- Las canchas están disponibles de **7:00 a. m. a 10:00 p. m.**
- Las duraciones permitidas son **60, 90 y 120 minutos**.
- La cantidad de jugadores debe estar entre **1 y 22**.
- No se permiten dos reservas activas con horarios superpuestos en la misma cancha y fecha.
- Las reservas canceladas no bloquean los horarios disponibles.

Por ejemplo, si una cancha está reservada de 10:00 a. m. a 11:00 a. m., el sistema no permitirá registrar otra reserva para esa misma cancha de 10:30 a. m. a 11:30 a. m.

Sin embargo, sí permitirá realizar una reserva a partir de las 11:00 a. m., siempre que se cumplan las demás condiciones.

## Canchas disponibles

El sistema permite realizar reservas para cuatro deportes:

- Fútbol.
- Baloncesto.
- Voleibol.
- Tenis.

## Cómo ejecutar el proyecto

Para utilizar la aplicación en tu computadora necesitas tener instalado **Python**.

### 1. Descargar el proyecto

Abre una terminal y ejecuta:

```bash
git clone https://github.com/yaugepedro/Sistema-de-reserva-de-canchas.git
cd Sistema-de-reserva-de-canchas
```

También puedes descargar el proyecto en formato ZIP desde GitHub y extraerlo en tu computadora.

### 2. Instalar las dependencias

Dentro de la carpeta del proyecto, ejecuta:

```bash
pip install -r requirements.txt
```

El archivo `requirements.txt` contiene:

```txt
Flask>=3.0
```

### 3. Iniciar la aplicación

En Windows:

```bash
py app.py
```

En Mac o Linux:

```bash
python3 app.py
```

### 4. Abrir el sistema

Cuando el servidor esté funcionando, abre el navegador y escribe:

http://127.0.0.1:5000

Desde la pantalla principal podrás consultar las reservas o crear una nueva.

Si deseas probar el funcionamiento con información de muestra, utiliza el botón **Cargar ejemplos**.

Para detener la aplicación, regresa a la terminal y presiona `Ctrl + C`.

## Almacenamiento de la información

Esta versión no utiliza una base de datos.

Las reservas se almacenan temporalmente en la memoria del programa. Esto permite trabajar con los registros mientras la aplicación está funcionando, pero significa que la información se pierde cuando se reinicia el servidor.

Decidimos mantener este funcionamiento porque el objetivo de la práctica es administrar el proyecto de software y trabajar con las funciones del CRUD existente.

Durante la planificación analizamos la posibilidad de incorporar SQLite para guardar la información permanentemente. Esta propuesta quedó documentada en Jira mediante la incidencia **RDC-45**, pero no se incorporó al alcance de la entrega.

## Organización del proyecto

```text
Sistema-de-reserva-de-canchas/
│
├── app.py
├── requirements.txt
├── README.md
│
├── templates/
│   ├── base.html
│   ├── lista.html
│   ├── formulario.html
│   └── detalle.html
│
└── static/
    └── style.css
```

**Descripción de los archivos:**

- `app.py`: contiene las rutas, las operaciones CRUD y las validaciones del sistema.
- `requirements.txt`: indica las dependencias necesarias.
- `README.md`: explica el funcionamiento y la ejecución del proyecto.
- `templates/`: contiene las pantallas HTML de la aplicación.
- `static/style.css`: contiene los estilos y el diseño visual.

## Tecnologías utilizadas

**Python:** lenguaje utilizado para desarrollar la lógica del sistema.

**Flask:** framework que permite gestionar las rutas, recibir los datos de los formularios y mostrar las pantallas.

**HTML:** utilizado para crear la estructura de las páginas.

**CSS:** utilizado para diseñar la apariencia de la aplicación.

**Jira:** herramienta utilizada para organizar las historias de usuario, las subtareas, las asignaciones y los sprints.

**Scrum:** marco de trabajo utilizado para distribuir las responsabilidades y planificar las actividades del equipo.

**Inteligencia artificial:** utilizada como apoyo durante la planificación, la preparación de historias de usuario, las estimaciones y la identificación de riesgos. Las propuestas fueron revisadas y ajustadas por el equipo antes de incorporarlas al proyecto.

## Organización del trabajo en Jira

El proyecto se encuentra registrado en Jira con la clave **RDC**.

El Product Backlog contiene **13 historias de usuario**, organizadas en tres épicas:

1. **Gestión de reservas:** registro, consulta, edición, cancelación, reactivación y eliminación.
2. **Disponibilidad y validación de horarios:** consulta de disponibilidad, detección de horarios superpuestos y validación de duración.
3. **Búsqueda, filtros y reportes:** búsqueda de reservas, aplicación de filtros, estadísticas y exportación a CSV.

Las historias fueron estimadas mediante Story Points y las actividades se organizaron en dos sprints.

El equipo también registró riesgos, responsables, subtareas de desarrollo y QA, reuniones diarias simuladas y retrospectivas.

## Posibles mejoras

Aunque la aplicación permite realizar las operaciones previstas para esta práctica, existen características que podrían incorporarse en una versión posterior:

- Almacenamiento permanente mediante una base de datos.
- Inicio de sesión para administradores.
- Notificaciones por correo electrónico para confirmar las reservas.

Estas funciones no forman parte de la versión actual.

## Sobre el proyecto

**Institución:** Instituto Tecnológico de las Américas (ITLA).

**Asignatura:** Gestión de Proyectos de Software.

**Proyecto:** Reserva de Canchas.

**Equipo:** Grupo 3.

**Integrantes:**
- Leiron Rolando Montero Montan.
- Yauge Pedro Vólquez Terrero.
- Josteen Mayobanex Del Orbe.
- Enmanuel Alejandro Cruz Encarnación.

**Fecha:** Octubre de 2026.
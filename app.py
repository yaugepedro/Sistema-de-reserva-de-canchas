import csv
import io
from datetime import date, datetime, timedelta

from flask import Flask, Response, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = "clave-secreta"

CANCHAS = {
    "Fútbol": {"icono": "⚽", "clase": "futbol"},
    "Baloncesto": {"icono": "🏀", "clase": "baloncesto"},
    "Voleibol": {"icono": "🏐", "clase": "voleibol"},
    "Tenis": {"icono": "🎾", "clase": "tenis"},
}
DURACIONES = {60: "1 hora", 90: "1 hora 30 min", 120: "2 horas"}
CAMPOS = ("nombre_estudiante", "matricula", "cancha", "fecha", "hora",
          "duracion", "jugadores", "notas")
APERTURA = 7 * 60
CIERRE = 22 * 60
DIAS = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]

reservas = []
contador = 1


@app.template_filter("fecha_texto")
def fecha_texto(valor):
    try:
        d = date.fromisoformat(valor)
    except ValueError:
        return valor
    hoy = date.today()
    if d == hoy:
        return "Hoy"
    if d == hoy + timedelta(days=1):
        return "Mañana"
    return f"{DIAS[d.weekday()]} {d.day} {MESES[d.month - 1]}"


@app.template_filter("duracion_texto")
def duracion_texto(minutos):
    return DURACIONES.get(minutos, f"{minutos} min")


def inicio_fin(hora, duracion):
    h, m = hora.split(":")[:2]
    inicio = int(h) * 60 + int(m)
    return inicio, inicio + duracion


def calcular_hora_fin(hora, duracion):
    _, fin = inicio_fin(hora, duracion)
    return f"{fin // 60:02d}:{fin % 60:02d}"


def buscar(reserva_id):
    for r in reservas:
        if r["id"] == reserva_id:
            return r
    return None


def leer_form():
    datos = {c: request.form.get(c, "").strip() for c in CAMPOS}
    for c in ("duracion", "jugadores"):
        try:
            datos[c] = int(datos[c])
        except ValueError:
            datos[c] = 0
    return datos


def validar(datos, reserva_id=None):
    obligatorios = ("nombre_estudiante", "cancha", "fecha", "hora", "duracion", "jugadores")
    if not all(datos.get(c) for c in obligatorios):
        return ["Completa todos los campos obligatorios."]
    if datos["cancha"] not in CANCHAS:
        return ["Elige una cancha de la lista."]
    try:
        fecha = date.fromisoformat(datos["fecha"])
        inicio, fin = inicio_fin(datos["hora"], datos["duracion"])
    except ValueError:
        return ["La fecha o la hora no son válidas."]
    errores = []
    ahora = datetime.now()
    if fecha < ahora.date():
        errores.append("La fecha no puede ser anterior a hoy.")
    elif fecha == ahora.date() and inicio <= ahora.hour * 60 + ahora.minute:
        errores.append("Esa hora ya pasó. Elige una hora posterior.")
    if inicio < APERTURA or fin > CIERRE:
        errores.append("Las canchas funcionan de 7:00 a 22:00.")
    if not 1 <= datos["jugadores"] <= 22:
        errores.append("Los jugadores deben ser entre 1 y 22.")
    for r in reservas:
        if r["id"] == reserva_id or r["estado"] != "Activa":
            continue
        if r["cancha"] != datos["cancha"] or r["fecha"] != datos["fecha"]:
            continue
        r_inicio, r_fin = inicio_fin(r["hora"], r["duracion"])
        if inicio < r_fin and r_inicio < fin:
            errores.append(f"Esa cancha ya está reservada de {r['hora']} a {r['hora_fin']}.")
            break
    return errores


def agregar(datos):
    global contador
    reservas.append({
        "id": contador,
        **datos,
        "hora_fin": calcular_hora_fin(datos["hora"], datos["duracion"]),
        "estado": "Activa",
    })
    contador += 1


@app.route("/")
def listar():
    q = request.args.get("q", "").strip().lower()
    cancha = request.args.get("cancha", "")
    estado = request.args.get("estado", "")
    fecha = request.args.get("fecha", "")
    orden = request.args.get("orden", "fecha")

    lista = [
        r for r in reservas
        if (not q or q in r["nombre_estudiante"].lower() or q in r["matricula"].lower())
        and (not cancha or r["cancha"] == cancha)
        and (not estado or r["estado"] == estado)
        and (not fecha or r["fecha"] == fecha)
    ]
    if orden == "reciente":
        lista.sort(key=lambda r: r["id"], reverse=True)
    elif orden == "nombre":
        lista.sort(key=lambda r: r["nombre_estudiante"].lower())
    else:
        lista.sort(key=lambda r: (r["fecha"], r["hora"]))

    hoy = date.today().isoformat()
    activas = [r for r in reservas if r["estado"] == "Activa"]
    stats = {
        "total": len(reservas),
        "activas": len(activas),
        "canceladas": len(reservas) - len(activas),
        "hoy": len([r for r in activas if r["fecha"] == hoy]),
    }
    conteo = {n: len([r for r in activas if r["cancha"] == n]) for n in CANCHAS}
    mayor = max(conteo.values()) or 1
    demanda = {n: {"total": t, "pct": round(t * 100 / mayor)} for n, t in conteo.items()}

    return render_template(
        "lista.html", reservas=lista, canchas=CANCHAS, stats=stats, demanda=demanda,
        q=request.args.get("q", ""), cancha=cancha, estado=estado, fecha=fecha, orden=orden,
        hay_filtros=bool(q or cancha or estado or fecha),
    )


@app.route("/reservas/nueva", methods=["GET", "POST"])
def crear():
    datos = {"duracion": 60, "jugadores": 10}
    if request.method == "POST":
        datos = leer_form()
        errores = validar(datos)
        if not errores:
            agregar(datos)
            flash("Reserva creada correctamente.", "ok")
            return redirect(url_for("listar"))
        for e in errores:
            flash(e, "error")
    return render_template("formulario.html", r=datos, canchas=CANCHAS, duraciones=DURACIONES,
                           titulo="Nueva reserva", hoy=date.today().isoformat())


@app.route("/reservas/<int:reserva_id>")
def detalle(reserva_id):
    r = buscar(reserva_id)
    if r is None:
        return redirect(url_for("listar"))
    return render_template("detalle.html", r=r, canchas=CANCHAS)


@app.route("/reservas/<int:reserva_id>/editar", methods=["GET", "POST"])
def editar(reserva_id):
    r = buscar(reserva_id)
    if r is None:
        return redirect(url_for("listar"))
    datos = dict(r)
    if request.method == "POST":
        datos = leer_form()
        errores = validar(datos, reserva_id)
        if not errores:
            r.update(datos)
            r["hora_fin"] = calcular_hora_fin(r["hora"], r["duracion"])
            flash("Reserva actualizada.", "ok")
            return redirect(url_for("detalle", reserva_id=reserva_id))
        for e in errores:
            flash(e, "error")
    return render_template("formulario.html", r=datos, canchas=CANCHAS, duraciones=DURACIONES,
                           titulo=f"Editar reserva #{reserva_id}", hoy=date.today().isoformat())


@app.route("/reservas/<int:reserva_id>/cancelar", methods=["POST"])
def cancelar(reserva_id):
    r = buscar(reserva_id)
    if r:
        r["estado"] = "Cancelada"
        flash("Reserva cancelada. La cancha quedó libre.", "ok")
    return redirect(request.referrer or url_for("listar"))


@app.route("/reservas/<int:reserva_id>/reactivar", methods=["POST"])
def reactivar(reserva_id):
    r = buscar(reserva_id)
    if r:
        errores = validar(r, reserva_id)
        if errores:
            for e in errores:
                flash(e, "error")
        else:
            r["estado"] = "Activa"
            flash("Reserva reactivada.", "ok")
    return redirect(request.referrer or url_for("listar"))


@app.route("/reservas/<int:reserva_id>/eliminar", methods=["POST"])
def eliminar(reserva_id):
    r = buscar(reserva_id)
    if r:
        reservas.remove(r)
        flash("Reserva eliminada.", "ok")
    return redirect(url_for("listar"))


@app.route("/ejemplos", methods=["POST"])
def ejemplos():
    hoy = date.today()
    muestras = [
        ("Ana Martínez", "2024-0112", "Fútbol", 1, "18:00", 90, 12, "Torneo de la facultad"),
        ("Luis Peña", "2023-0458", "Baloncesto", 1, "16:00", 60, 8, ""),
        ("Carla Gómez", "2024-0987", "Voleibol", 2, "17:30", 60, 10, "Traer balones propios"),
        ("Miguel Santos", "2022-0301", "Tenis", 2, "08:00", 60, 2, ""),
        ("Daniela Ruiz", "2023-0764", "Fútbol", 3, "19:00", 120, 14, "Final interna"),
        ("José Almonte", "2024-0555", "Baloncesto", 4, "10:00", 90, 6, ""),
    ]
    creadas = 0
    for nombre, matricula, cancha, dias, hora, duracion, jugadores, notas in muestras:
        datos = {
            "nombre_estudiante": nombre, "matricula": matricula, "cancha": cancha,
            "fecha": (hoy + timedelta(days=dias)).isoformat(), "hora": hora,
            "duracion": duracion, "jugadores": jugadores, "notas": notas,
        }
        if not validar(datos):
            agregar(datos)
            creadas += 1
    flash(f"Se cargaron {creadas} reservas de ejemplo.", "ok")
    return redirect(url_for("listar"))


@app.route("/vaciar", methods=["POST"])
def vaciar():
    reservas.clear()
    flash("Se eliminaron todas las reservas.", "ok")
    return redirect(url_for("listar"))


@app.route("/exportar")
def exportar():
    salida = io.StringIO()
    escritor = csv.writer(salida)
    escritor.writerow(["ID", "Estudiante", "Matrícula", "Cancha", "Fecha", "Inicio", "Fin",
                       "Jugadores", "Estado", "Notas"])
    for r in sorted(reservas, key=lambda x: (x["fecha"], x["hora"])):
        escritor.writerow([r["id"], r["nombre_estudiante"], r["matricula"], r["cancha"],
                           r["fecha"], r["hora"], r["hora_fin"], r["jugadores"],
                           r["estado"], r["notas"]])
    return Response("\ufeff" + salida.getvalue(), mimetype="text/csv",
                    headers={"Content-Disposition": "attachment; filename=reservas.csv"})


if __name__ == "__main__":
    app.run(debug=True)
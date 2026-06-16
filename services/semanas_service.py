from datetime import datetime, timedelta


semanas = []


def crear_semana(numero, fecha_inicio_texto):

    fecha_inicio = datetime.strptime(
        fecha_inicio_texto,
        "%d/%m/%y"
    )

    fecha_fin = fecha_inicio + timedelta(days=6)

    return {
        "numero": int(numero),
        "fecha_inicio": fecha_inicio.strftime("%d/%m/%y"),
        "fecha_fin": fecha_fin.strftime("%d/%m/%y")
    }


def agregar_semana(numero, fecha_inicio_texto):

    semana = crear_semana(
        numero,
        fecha_inicio_texto
    )

    semanas.append(semana)

    return semana


def eliminar_semana(semana):

    if semana in semanas:
        semanas.remove(semana)


def listar_semanas():

    return semanas
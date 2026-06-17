import json
import os
from datetime import datetime, timedelta

from services.persistencia_json import eliminar_carpeta_semana


# !! ==========================================================
# !! SEMANAS_SERVICE.PY
# !!
# !! Administra las semanas de captura.
# !!
# !! Guarda y carga semanas desde:
# !! capturas/semanas.json
# !! ==========================================================


BASE_CAPTURAS = "capturas"
ARCHIVO_SEMANAS = os.path.join(
    BASE_CAPTURAS,
    "semanas.json"
)


semanas = []


def guardar_semanas():

    os.makedirs(
        BASE_CAPTURAS,
        exist_ok=True
    )

    with open(
        ARCHIVO_SEMANAS,
        "w",
        encoding="utf-8"
    ) as archivo:

        json.dump(
            semanas,
            archivo,
            ensure_ascii=False,
            indent=4
        )


def cargar_semanas():

    global semanas

    if not os.path.exists(ARCHIVO_SEMANAS):

        semanas = []
        return

    with open(
        ARCHIVO_SEMANAS,
        "r",
        encoding="utf-8"
    ) as archivo:

        semanas = json.load(archivo)


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

    guardar_semanas()

    return semana


def eliminar_semana(semana):

    if semana in semanas:

        semanas.remove(semana)

        guardar_semanas()

        eliminar_carpeta_semana(semana)


def listar_semanas():

    if len(semanas) == 0:
        cargar_semanas()

    return semanas
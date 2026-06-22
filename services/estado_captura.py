# !! ==========================================================
# !! ESTADO_CAPTURA.PY
# !!
# !! Estado temporal de capturas por obra.
# !!
# !! Aquí se guarda la información capturada mientras
# !! la aplicación está abierta.
# !!
# !! Futuro:
# !! - Guardar a JSON.
# !! - Guardar a SQLite.
# !! - Recuperar capturas aunque se cierre la app.
# !! ==========================================================

from services.persistencia_json import (
    cargar_captura,
    guardar_captura
)


capturas_por_semana = {}


def obtener_captura_obra(
    semana,
    clave_obra,
    nombre_obra,
    direccion_obra
):

    numero_semana = semana["numero"]

    if numero_semana not in capturas_por_semana:
        capturas_por_semana[numero_semana] = {}

    if clave_obra not in capturas_por_semana[numero_semana]:

        captura_guardada = cargar_captura(
            semana,
            clave_obra
        )

        if captura_guardada:

            capturas_por_semana[numero_semana][clave_obra] = captura_guardada

        else:

            capturas_por_semana[numero_semana][clave_obra] = {

                "semana": semana,
                "clave_obra": clave_obra,
                "nombre_obra": nombre_obra,
                "direccion_obra": direccion_obra,
                "cuadrillas": []

            }

    return capturas_por_semana[numero_semana][clave_obra]


def guardar_captura_obra(captura):

    guardar_captura(captura)


def eliminar_captura_obra(
    semana,
    clave_obra
):

    numero_semana = semana["numero"]

    if numero_semana in capturas_por_semana:

        if clave_obra in capturas_por_semana[numero_semana]:

            del capturas_por_semana[numero_semana][clave_obra]
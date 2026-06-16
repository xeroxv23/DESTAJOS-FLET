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

capturas_por_obra = {}


def obtener_captura_obra(clave_obra, nombre_obra):

    if clave_obra not in capturas_por_obra:

        capturas_por_obra[clave_obra] = {
            "clave_obra": clave_obra,
            "nombre_obra": nombre_obra,
            "cuadrillas": []
        }

    return capturas_por_obra[clave_obra]


def eliminar_captura_obra(clave_obra):

    if clave_obra in capturas_por_obra:
        del capturas_por_obra[clave_obra]
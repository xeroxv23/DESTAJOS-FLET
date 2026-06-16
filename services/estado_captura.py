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

capturas_por_semana = {}


def obtener_captura_obra(semana, clave_obra, nombre_obra):

    numero_semana = semana["numero"]

    if numero_semana not in capturas_por_semana:
        capturas_por_semana[numero_semana] = {}

    if clave_obra not in capturas_por_semana[numero_semana]:

        capturas_por_semana[numero_semana][clave_obra] = {
            "semana": semana,
            "clave_obra": clave_obra,
            "nombre_obra": nombre_obra,
            "cuadrillas": []
        }

    return capturas_por_semana[numero_semana][clave_obra]
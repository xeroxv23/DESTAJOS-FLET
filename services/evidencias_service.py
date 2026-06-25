import os
import shutil
from datetime import datetime

from services.file_manager import obtener_carpeta_evidencias_obra


#region EVIDENCIAS_SERVICE.PY

# !! ==========================================================
# !! EVIDENCIAS_SERVICE.PY
# !!
# !! Servicio para administrar evidencias fotográficas.
# !!
# !! Responsabilidades:
# !! - Guardar evidencia en carpeta de semana/obra
# !! - Listar evidencias guardadas
# !! - Eliminar evidencias
# !! - Generar nombres seguros para archivos
# !! ==========================================================


def limpiar_nombre_archivo(texto):
    """
    Convierte un texto capturado por el usuario en un nombre
    seguro para archivo.
    """

    texto = texto.strip().lower()

    reemplazos = {
        "á": "a",
        "é": "e",
        "í": "i",
        "ó": "o",
        "ú": "u",
        "ñ": "n",
        " ": "_",
        "/": "_",
        "\\": "_",
        ":": "_",
        "*": "_",
        "?": "_",
        '"': "_",
        "<": "_",
        ">": "_",
        "|": "_",
    }

    for original, nuevo in reemplazos.items():
        texto = texto.replace(original, nuevo)

    return texto


def guardar_evidencia_desde_archivo(
    semana_actual,
    clave_obra,
    ruta_origen,
    nombre_evidencia
):

    ruta_origen = ruta_origen.strip().strip('"')

    if not os.path.exists(ruta_origen):
        raise FileNotFoundError(
            f"No se encontró la imagen: {ruta_origen}"
        )

    """
    Copia una imagen seleccionada a la carpeta de evidencias
    de la semana y obra actual.
    """

    carpeta_destino = obtener_carpeta_evidencias_obra(
        semana_actual,
        clave_obra
    )

    extension = os.path.splitext(ruta_origen)[1].lower()

    if extension == "":
        extension = ".jpg"

    fecha = datetime.now().strftime("%Y%m%d_%H%M%S")

    nombre_limpio = limpiar_nombre_archivo(
        nombre_evidencia
    )

    nombre_archivo = (
        f"{clave_obra}_{fecha}_{nombre_limpio}{extension}"
    )

    ruta_destino = os.path.join(
        carpeta_destino,
        nombre_archivo
    )

    shutil.copy2(
        ruta_origen,
        ruta_destino
    )

    return ruta_destino


def listar_evidencias(
    semana_actual,
    clave_obra
):
    """
    Lista las evidencias guardadas para una semana y obra.
    """

    carpeta = obtener_carpeta_evidencias_obra(
        semana_actual,
        clave_obra
    )

    evidencias = []

    for archivo in os.listdir(carpeta):

        ruta = os.path.join(
            carpeta,
            archivo
        )

        if os.path.isfile(ruta):

            evidencias.append({
                "nombre": archivo,
                "ruta": ruta
            })

    evidencias.sort(
        key=lambda item: item["nombre"]
    )

    return evidencias


def eliminar_evidencia(ruta_evidencia):
    """
    Elimina una evidencia fotográfica.
    """

    if os.path.exists(ruta_evidencia):
        os.remove(ruta_evidencia)
        return True

    return False


#endregion
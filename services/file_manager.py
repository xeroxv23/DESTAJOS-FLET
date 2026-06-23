import os


#region FILE_MANAGER.PY

# !! ==========================================================
# !! FILE_MANAGER.PY
# !!
# !! Administrador central de carpetas del sistema.
# !!
# !! Responsabilidades:
# !! - Crear estructura base de trabajo
# !! - Administrar carpetas de capturas
# !! - Administrar evidencias fotográficas
# !! - Administrar archivos exportados
# !! - Administrar respaldos
# !!
# !! Este módulo será clave para Windows, Android y tablets.
# !! ==========================================================


APP_FOLDER = "Capturador Destajos"

CARPETA_CAPTURAS = "Capturas"
CARPETA_EVIDENCIAS = "Evidencias"
CARPETA_EXPORTADOS = "Exportados"
CARPETA_RESPALDOS = "Respaldos"


def obtener_carpeta_base():
    """
    Obtiene la carpeta principal donde vivirá la información
    operativa de la aplicación.

    En Windows:
    Documentos/Capturador Destajos

    En Android:
    Más adelante podremos adaptar esta función para usar
    almacenamiento interno disponible.
    """

    documentos = os.path.join(
        os.path.expanduser("~"),
        "Documents"
    )

    return os.path.join(
        documentos,
        APP_FOLDER
    )


def crear_estructura_base():
    """
    Crea las carpetas principales del sistema si no existen.
    """

    carpeta_base = obtener_carpeta_base()

    carpetas = [
        carpeta_base,
        os.path.join(carpeta_base, CARPETA_CAPTURAS),
        os.path.join(carpeta_base, CARPETA_EVIDENCIAS),
        os.path.join(carpeta_base, CARPETA_EXPORTADOS),
        os.path.join(carpeta_base, CARPETA_RESPALDOS),
    ]

    for carpeta in carpetas:
        os.makedirs(
            carpeta,
            exist_ok=True
        )

    return carpeta_base


def obtener_carpeta_evidencias_obra(semana_actual, clave_obra):
    """
    Obtiene o crea la carpeta de evidencias de una obra
    específica dentro de una semana.

    Ejemplo:
    Evidencias/24_A-001
    """

    carpeta_base = crear_estructura_base()

    numero_semana = str(
        semana_actual["numero"]
    )

    nombre_carpeta = f"{numero_semana}_{clave_obra}"

    ruta = os.path.join(
        carpeta_base,
        CARPETA_EVIDENCIAS,
        nombre_carpeta
    )

    os.makedirs(
        ruta,
        exist_ok=True
    )

    return ruta


def obtener_carpeta_exportados():
    """
    Obtiene la carpeta donde se guardarán los Excel generados.
    """

    carpeta_base = crear_estructura_base()

    ruta = os.path.join(
        carpeta_base,
        CARPETA_EXPORTADOS
    )

    os.makedirs(
        ruta,
        exist_ok=True
    )

    return ruta


def obtener_carpeta_capturas():
    """
    Obtiene la carpeta donde se guardarán capturas JSON.
    """

    carpeta_base = crear_estructura_base()

    ruta = os.path.join(
        carpeta_base,
        CARPETA_CAPTURAS
    )

    os.makedirs(
        ruta,
        exist_ok=True
    )

    return ruta


def obtener_carpeta_respaldos():
    """
    Obtiene la carpeta donde se guardarán respaldos.
    """

    carpeta_base = crear_estructura_base()

    ruta = os.path.join(
        carpeta_base,
        CARPETA_RESPALDOS
    )

    os.makedirs(
        ruta,
        exist_ok=True
    )

    return ruta


#endregion
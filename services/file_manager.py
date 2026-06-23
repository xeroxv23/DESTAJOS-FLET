import os


#region FILE_MANAGER.PY

# !! ==========================================================
# !! FILE_MANAGER.PY
# !!
# !! Administrador central de carpetas del sistema.
# !!
# !! Durante desarrollo en Windows:
# !! Las carpetas se crean dentro del proyecto.
# !!
# !! Cuando generemos APK Android:
# !! Solo cambiaremos obtener_carpeta_base().
# !! ==========================================================


APP_FOLDER = "Capturador Destajos"

CARPETA_CAPTURAS = "capturas"
CARPETA_EVIDENCIAS = "evidencias"
CARPETA_EXPORTADOS = "exportados"
CARPETA_RESPALDOS = "respaldos"


def obtener_carpeta_base():
    """
    Obtiene la carpeta base de trabajo del sistema.

    En desarrollo:
    Usa la carpeta actual del proyecto.

    Ejemplo:
    DESTAJOS-FLET/
    """

    return os.getcwd()


def crear_estructura_base():
    """
    Crea las carpetas principales dentro del proyecto.
    """

    carpeta_base = obtener_carpeta_base()

    carpetas = [
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
    evidencias/24_A-001
    """

    crear_estructura_base()

    numero_semana = str(
        semana_actual["numero"]
    )

    nombre_carpeta = f"{numero_semana}_{clave_obra}"

    ruta = os.path.join(
        obtener_carpeta_base(),
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

    crear_estructura_base()

    ruta = os.path.join(
        obtener_carpeta_base(),
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

    crear_estructura_base()

    ruta = os.path.join(
        obtener_carpeta_base(),
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

    crear_estructura_base()

    ruta = os.path.join(
        obtener_carpeta_base(),
        CARPETA_RESPALDOS
    )

    os.makedirs(
        ruta,
        exist_ok=True
    )

    return ruta


#endregion
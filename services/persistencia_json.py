import json
import os
import shutil

BASE_CAPTURAS = "capturas"

def obtener_ruta_captura(semana, clave_obra):

    carpeta_semana = os.path.join(
        BASE_CAPTURAS,
        f"semana_{semana['numero']}"
    )

    os.makedirs(
        carpeta_semana,
        exist_ok=True
    )

    archivo = f"{clave_obra}.json"

    return os.path.join(
        carpeta_semana,
        archivo
    )


def guardar_captura(captura):

    ruta = obtener_ruta_captura(
        captura["semana"],
        captura["clave_obra"]
    )

    if len(captura["cuadrillas"]) == 0:

        if os.path.exists(ruta):
            os.remove(ruta)

        return

    with open(
        ruta,
        "w",
        encoding="utf-8"
    ) as archivo:

        json.dump(
            captura,
            archivo,
            ensure_ascii=False,
            indent=4
        )


def cargar_captura(semana, clave_obra):

    ruta = obtener_ruta_captura(
        semana,
        clave_obra
    )

    if not os.path.exists(ruta):
        return None

    with open(
        ruta,
        "r",
        encoding="utf-8"
    ) as archivo:

        return json.load(archivo)
    

def listar_capturas_semana(semana):

    carpeta_semana = os.path.join(
        BASE_CAPTURAS,
        f"semana_{semana['numero']}"
    )

    if not os.path.exists(carpeta_semana):
        return []

    capturas = []

    for archivo in os.listdir(carpeta_semana):

        if archivo.endswith(".json"):

            ruta = os.path.join(
                carpeta_semana,
                archivo
            )

            with open(
                ruta,
                "r",
                encoding="utf-8"
            ) as f:

                capturas.append(
                    json.load(f)
                )

    return capturas

def obtener_claves_capturadas_semana(semana):

    capturas = listar_capturas_semana(semana)

    claves = []

    for captura in capturas:

        claves.append(
            captura["clave_obra"]
        )

    return claves

def eliminar_carpeta_semana(semana):

    carpeta_semana = os.path.join(
        BASE_CAPTURAS,
        f"semana_{semana['numero']}"
    )

    if os.path.exists(carpeta_semana):

        shutil.rmtree(carpeta_semana)

def eliminar_captura_json(semana, clave_obra):

    ruta = obtener_ruta_captura(
        semana,
        clave_obra
    )

    if os.path.exists(ruta):
        os.remove(ruta)
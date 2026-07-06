import xlwings as xw
import unicodedata

NOMBRE_ARCHIVO = "REGISTRO PERSONAL WATTS 2026"
NOMBRE_HOJA = "BASE DE DATOS"
FILA_INICIAL = 2
FILA_FINAL = 596
COLUMNA = "B"


def quitar_acentos(texto):
    if texto is None or texto == "":
        return texto

    texto = str(texto)

    texto_normalizado = unicodedata.normalize("NFD", texto)

    texto_sin_acentos = "".join(
        caracter for caracter in texto_normalizado
        if unicodedata.category(caracter) != "Mn"
    )

    return texto_sin_acentos


def obtener_libro_abierto(nombre_archivo):
    for app in xw.apps:
        for libro in app.books:
            if nombre_archivo.lower() in libro.name.lower():
                return libro

    return None


def main():
    wb = obtener_libro_abierto(NOMBRE_ARCHIVO)

    if wb is None:
        print(f"ERROR: El archivo '{NOMBRE_ARCHIVO}' no está abierto.")
        return

    try:
        ws = wb.sheets[NOMBRE_HOJA]
    except Exception:
        print(f"ERROR: No se encontró la hoja '{NOMBRE_HOJA}'.")
        return

    cambios = 0

    for fila in range(FILA_INICIAL, FILA_FINAL + 1):
        celda = ws.range(f"{COLUMNA}{fila}")

        valor_original = celda.value
        valor_limpio = quitar_acentos(valor_original)

        if valor_original != valor_limpio:
            celda.value = valor_limpio
            cambios += 1

        print(f"Fila {fila}: {valor_original} -> {valor_limpio}")

    print("Proceso terminado correctamente.")
    print(f"Celdas modificadas: {cambios}")
    print("Guarda el archivo manualmente si quieres conservar los cambios.")


if __name__ == "__main__":
    main()
import os
import shutil
import xlwings as xw

# !! ==========================================================
# !! EXCEL_EXPORTER.PY
# !!
# !! Exportador Excel con xlwings.
# !!
# !! Objetivo:
# !! - Copiar una plantilla .xlsm
# !! - Renombrarla con clave y nombre de obra
# !! - Abrirla con Excel
# !! - Escribir encabezados principales
# !! - Guardar respetando macros, fórmulas y formatos
# !! ==========================================================


PLANTILLA = "plantillas/plantilla de captura.xlsm"
CARPETA_EXPORTADOS = "exportados"


def limpiar_nombre_archivo(texto):

    caracteres_invalidos = [
        "\\", "/", ":", "*", "?", '"', "<", ">", "|"
    ]

    for caracter in caracteres_invalidos:
        texto = texto.replace(caracter, "")

    return texto.strip()

#region CAPTURA TRABAJADOR
# !! ==========================================================
# !! escribir_trabajador()
# !!
# !! Escribe un trabajador en una fila específica.
# !!
# !! Mapeo:
# !! A = Nómina
# !! B = Número cuadrilla
# !! P = Número cuadrilla
# !! L = Días
# !! S = Participación (solo destajo)
# !! ==========================================================
#endregion

def escribir_trabajador(
    hoja,
    fila,
    trabajador,
    tipo_cuadrilla
):

    hoja.range(f"A{fila}").value = trabajador["clave"]

    hoja.range(f"B{fila}").value = (
        trabajador["numero_cuadrilla"]
    )

    if tipo_cuadrilla == "destajo":

        # !! Destajistas NO llevan días en columna L.
        # !! Ganan por conceptos, no por días.
        hoja.range(f"L{fila}").value = None

        # !! Columna P NO se llena aquí.
        # !! En destajo, P se llenará en el último concepto capturado.
        hoja.range(f"P{fila}").value = None

        hoja.range(f"S{fila}").value = (
            trabajador["porcentaje"] / 100
        )

    else:

        # !! Por día:
        # !! L = días trabajados.
        hoja.range(f"L{fila}").value = trabajador["dias"]

        # !! Por día siempre recibe 100%.
        hoja.range(f"S{fila}").value = 1

        # !! Por ahora P cierra en la misma fila del trabajador.
        # !! FUTURO:
        # !! Si tiene horas extras, P deberá moverse
        # !! a la última fila donde se capturen esas horas extras.
        hoja.range(f"P{fila}").value = (
            trabajador["numero_cuadrilla"]
        )

def exportar_captura(
    hoja,
    captura,
    fila_inicial=15
):

    fila = fila_inicial

    for cuadrilla in captura["cuadrillas"]:

        if cuadrilla["tipo"] == "dia":

            for trabajador in cuadrilla["trabajadores"]:

                escribir_trabajador(
                    hoja,
                    fila,
                    trabajador,
                    cuadrilla["tipo"]
                )

                fila += 1

            # !! Actividades del personal por día.
            actividades = cuadrilla.get(
                "actividades",
                ""
            ).strip()

            if actividades:

                hoja.range(f"D{fila}").value = actividades

                fila += 1

            # !! Espacio entre bloques.
            fila += 1

        if cuadrilla["tipo"] == "destajo":

            for trabajador in cuadrilla["trabajadores"]:

                escribir_trabajador(
                    hoja,
                    fila,
                    trabajador,
                    cuadrilla["tipo"]
                )

                fila += 1

            ultima_fila_concepto = None

            for subtitulo in cuadrilla["subtitulos"]:

                escribir_subtitulo(
                    hoja,
                    fila,
                    subtitulo
                )

                fila += 1

                for concepto in subtitulo["conceptos"]:

                    escribir_concepto(
                        hoja,
                        fila,
                        concepto,
                        cuadrilla["numero"]
                    )

                    ultima_fila_concepto = fila

                    fila += 1

            # !! En destajo, la columna P se llena
            # !! únicamente en el último concepto capturado.
            if ultima_fila_concepto is not None:

                hoja.range(f"P{ultima_fila_concepto}").value = (
                    cuadrilla["numero"]
                )

            # !! Espacio entre cuadrillas.
            fila += 1

    return fila

def exportar_prueba_encabezado(captura):

    semana = captura["semana"]

    clave_obra = captura["clave_obra"]
    nombre_obra = captura["nombre_obra"]
    direccion_obra = captura.get(
    "direccion_obra",
    ""
)

    nombre_archivo = limpiar_nombre_archivo(
        f"{clave_obra} {nombre_obra}.xlsm"
    )

    carpeta_semana = os.path.join(
        CARPETA_EXPORTADOS,
        f"semana_{semana['numero']}"
    )

    os.makedirs(
        carpeta_semana,
        exist_ok=True
    )

    ruta_salida = os.path.join(
        carpeta_semana,
        nombre_archivo
    )

    shutil.copyfile(
        PLANTILLA,
        ruta_salida
    )

    app = xw.App(
        visible=False
    )

    try:

        libro = app.books.open(
            ruta_salida
        )

        hoja = libro.sheets[0]

        hoja.range("D6").value = clave_obra
        hoja.range("D8").value = direccion_obra

        hoja.range("B10").value = semana["numero"]
        hoja.range("E10").value = semana["fecha_inicio"]
        hoja.range("F10").value = semana["fecha_fin"]

        exportar_captura(
            hoja,
            captura,
            fila_inicial=15
        )

        libro.save()

        libro.close()

    finally:

        app.quit()

    return ruta_salida

def escribir_subtitulo(
    hoja,
    fila,
    subtitulo
):

    hoja.range(f"D{fila}").value = subtitulo["nombre"]

def escribir_concepto(
    hoja,
    fila,
    concepto,
    numero_cuadrilla
):

    nota = concepto.get(
        "notas",
        ""
    ).strip()

    hoja.range(f"A{fila}").value = concepto["clave"]
    hoja.range(f"B{fila}").value = numero_cuadrilla

    hoja.range(f"D{fila}").value = nota

    hoja.range(f"I{fila}").value = concepto.get("largo", "")
    hoja.range(f"J{fila}").value = concepto.get("ancho", "")
    hoja.range(f"K{fila}").value = concepto.get("alto", "")
    hoja.range(f"L{fila}").value = concepto.get("piezas", "")
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

        # !! Si NO tiene horas extras, P cierra aquí.
        # !! Si SÍ tiene horas extras, P se escribirá
        # !! en la fila del concepto LOTE.
        if not trabajador.get("horas_extras", ""):

            hoja.range(f"P{fila}").value = (
                trabajador["numero_cuadrilla"]
            )

        else:

            hoja.range(f"P{fila}").value = None

def escribir_horas_extras(
    hoja,
    fila,
    trabajador
):

    horas_extras = trabajador.get(
        "horas_extras",
        ""
    )

    if horas_extras == "":
        return False

    descripcion = trabajador.get(
        "descripcion_horas_extras",
        ""
    )

    salario_diario = float(
        trabajador.get(
            "salario_diario",
            0
        )
    )

    hoja.range(f"A{fila}").value = "LOTE"

    hoja.range(f"B{fila}").value = (
        trabajador["numero_cuadrilla"]
    )

    hoja.range(f"D{fila}").value = descripcion

    hoja.range(f"I{fila}").value = (
        salario_diario / 4 / 100
    )

    hoja.range(f"L{fila}").value = float(
        horas_extras
    )

    # !! En trabajadores por día con horas extras,
    # !! la columna P cierra en la fila de horas extras,
    # !! no en la fila del trabajador.
    hoja.range(f"P{fila}").value = (
        trabajador["numero_cuadrilla"]
    )

    return True

def dividir_texto_por_palabras(
    texto,
    limite=40
):

    texto = texto.strip()

    if texto == "":
        return []

    palabras = texto.split()

    lineas = []
    linea_actual = ""

    for palabra in palabras:

        if linea_actual == "":

            linea_actual = palabra

        elif len(linea_actual) + 1 + len(palabra) <= limite:

            linea_actual += " " + palabra

        else:

            lineas.append(
                linea_actual
            )

            linea_actual = palabra

    if linea_actual:

        lineas.append(
            linea_actual
        )

    return lineas

def escribir_actividades(
    hoja,
    fila,
    actividades,
    limite=40
):

    lineas = dividir_texto_por_palabras(
        actividades,
        limite
    )

    for linea in lineas:

        hoja.range(f"D{fila}").value = linea

        fila += 1

    return fila

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

                tiene_horas_extras = escribir_horas_extras(
                    hoja,
                    fila,
                    trabajador
                )

                if tiene_horas_extras:

                    fila += 1

            # !! Actividades del personal por día.
            actividades = cuadrilla.get(
                "actividades",
                ""
            ).strip()

            if actividades:

                fila = escribir_actividades(
                    hoja,
                    fila,
                    actividades,
                    limite=40
                )

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

def exportar_destajo(
    captura,
    residentes=None,
    porcentaje_maestreada=None
):

    # !! Si no se enviaron residentes,
    # !! trabajamos con una lista vacía.

    if residentes is None:

        residentes = []

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

        # !! ----------------------------------------------------------
        # !! Sección fija de destajista
        # !! ----------------------------------------------------------
        
        escribir_destajista_base(
            hoja
        )

        ultima_fila_residente = escribir_residentes(
            hoja,
            residentes,
            fila_inicial=355,
            numero_inicial=61
        )

        escribir_maestreada(
            hoja,
            porcentaje_maestreada
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

    celda = hoja.range(
        f"D{fila}"
    )

    celda.value = subtitulo["nombre"]

    # !! Aplicar negrita
    celda.api.Font.Bold = True

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

def escribir_destajista_base(hoja):

    # !! Fila fija del destajista
    hoja.range("A353").value = 34
    hoja.range("B353").value = 60
    hoja.range("S353").value = 1

    # !! Fila fija del concepto destajista
    hoja.range("A354").value = "destaj"
    hoja.range("B354").value = 60
    hoja.range("H354").value = 0.04
    hoja.range("L354").value = 1
    hoja.range("P354").value = 60

def escribir_residentes(
    hoja,
    residentes,
    fila_inicial=355,
    numero_inicial=61
):

    fila = fila_inicial
    numero_cuadrilla = numero_inicial

    for residente in residentes:

        residente["numero_cuadrilla"] = numero_cuadrilla

        # !! Fila del residente
        escribir_trabajador(
            hoja,
            fila,
            residente,
            "dia"
        )

        fila_residente = fila

        fila += 1

        # !! Fila debajo del residente:
        # !! Columna D = puesto
        hoja.range(f"D{fila}").value = residente.get(
            "puesto",
            ""
        )

        fila_puesto = fila

        fila += 1

        # !! Horas extras, si existen.
        # !! Se capturan después del puesto.
        tiene_horas_extras = escribir_horas_extras(
            hoja,
            fila,
            residente
        )

        if tiene_horas_extras:

            # !! Si existen horas extras,
            # !! la columna P debe cerrar en la fila de HE.
            hoja.range(f"P{fila_residente}").value = None
            hoja.range(f"P{fila_puesto}").value = None

            fila += 1

        else:

            # !! Si NO existen horas extras,
            # !! la columna P queda en la fila del residente.
            hoja.range(f"P{fila_residente}").value = numero_cuadrilla

        # !! Espacio entre residentes
        fila += 1

        numero_cuadrilla += 1

    return fila

def escribir_maestreada(
    hoja,
    porcentaje_maestreada
):

    if porcentaje_maestreada is None:
        return

    hoja.range("A393").value = "lote"
    hoja.range("B393").value = 75
    hoja.range("D393").value = "MANDOS INTERMEDIOS"
    hoja.range("H393").value = porcentaje_maestreada / 100
    hoja.range("L393").value = 1
    hoja.range("P393").value = 75


#END
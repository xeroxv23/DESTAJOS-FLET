# !! ==========================================================
# !! CUADRILLA_SERVICE.PY
# !!
# !! Lógica de negocio relacionada con cuadrillas.
# !!
# !! Responsabilidades:
# !! - Evaluar fórmulas matemáticas.
# !! - Calcular puntos.
# !! - Calcular porcentajes de participación.
# !!
# !! Este módulo NO contiene Flet.
# !! Este módulo NO contiene SQLite.
# !!
# !! Solamente realiza cálculos.
# !!
# !! ==========================================================


# !! ----------------------------------------------------------
# !! calcular_valor()
# !!
# !! Permite capturar fórmulas para días trabajados.
# !!
# !! Ejemplos válidos:
# !!
# !! 5
# !! =7/6*5
# !! =6+1
# !! =5.5
# !!
# !! Retorna:
# !! float
# !!
# !! Ejemplo:
# !!
# !! =7/6*5
# !! resultado = 5.833333
# !!
# !! ----------------------------------------------------------
def calcular_valor(texto):

    texto = texto.strip()

    if texto.startswith("="):
        texto = texto[1:]

    try:

        return float(
            eval(
                texto,
                {"__builtins__": {}},
                {}
            )
        )

    except:

        return None


# !! ----------------------------------------------------------
# !! recalcular_cuadrilla()
# !!
# !! Calcula automáticamente:
# !!
# !! - Ponderación
# !! - Puntos
# !! - Participación %
# !!
# !! Reglas actuales:
# !!
# !! OF = 60
# !! Cualquier otro puesto = 40
# !!
# !! Fórmula:
# !!
# !! puntos = ponderacion × dias
# !!
# !! porcentaje =
# !! puntos_individuales / puntos_totales
# !!
# !! Ejemplo:
# !!
# !! OF 6 días
# !! 60 × 6 = 360
# !!
# !! PEON 6 días
# !! 40 × 6 = 240
# !!
# !! Total:
# !! 600
# !!
# !! OF = 60%
# !! PEON = 40%
# !!
# !! ----------------------------------------------------------
def recalcular_cuadrilla(cuadrilla):

    total_puntos = 0

    # ! Primera pasada:
    # ! calcular puntos individuales
    for trabajador in cuadrilla["trabajadores"]:

        if trabajador["puesto"] == "OF":
            ponderacion = 60
        else:
            ponderacion = 40

        trabajador["ponderacion"] = ponderacion

        trabajador["puntos"] = (
            ponderacion *
            trabajador["dias"]
        )

        total_puntos += trabajador["puntos"]

    # ! Segunda pasada:
    # ! calcular porcentaje de participación
    if total_puntos > 0:

        for trabajador in cuadrilla["trabajadores"]:

            trabajador["porcentaje"] = (

                trabajador["puntos"]
                /
                total_puntos

            ) * 100

    else:

        for trabajador in cuadrilla["trabajadores"]:

            trabajador["porcentaje"] = 0
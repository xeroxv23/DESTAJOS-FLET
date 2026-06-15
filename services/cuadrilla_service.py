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


def recalcular_cuadrilla(cuadrilla):

    total_puntos = 0

    for trabajador in cuadrilla["trabajadores"]:

        if trabajador["puesto"] == "OF":
            ponderacion = 60
        else:
            ponderacion = 40

        trabajador["ponderacion"] = ponderacion
        trabajador["puntos"] = ponderacion * trabajador["dias"]

        total_puntos += trabajador["puntos"]

    for trabajador in cuadrilla["trabajadores"]:

        if total_puntos > 0:
            trabajador["porcentaje"] = (
                trabajador["puntos"] / total_puntos
            ) * 100
        else:
            trabajador["porcentaje"] = 0
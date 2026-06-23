# !! ==========================================================
# !! CAPTURA_SERVICE.PY
# !!
# !! Constructor de estructuras de captura.
# !!
# !! Responsabilidades:
# !! - Crear cuadrillas.
# !! - Crear trabajadores.
# !! - Crear subtítulos.
# !! - Crear conceptos.
# !!
# !! Este módulo NO contiene:
# !! - Flet
# !! - SQLite
# !! - Exportación Excel
# !!
# !! Solamente construye objetos de trabajo.
# !!
# !! ==========================================================


# !! ----------------------------------------------------------
# !! crear_cuadrilla()
# !!
# !! Crea una nueva cuadrilla vacía.
# !!
# !! Tipos:
# !! - dia
# !! - destajo
# !!
# !! Ejemplo:
# !!
# !! Cuadrilla 1
# !! Cuadrilla 2
# !! Cuadrilla 3
# !!
# !! ----------------------------------------------------------
def crear_cuadrilla(numero, tipo):

    return {

        "numero": numero,

        "tipo": tipo,

        "trabajadores": [],

        "subtitulos": [],

        "conceptos": [],

        "actividades": ""

    }


# !! ----------------------------------------------------------
# !! crear_trabajador()
# !!
# !! Construye un trabajador para una cuadrilla.
# !!
# !! Datos obtenidos desde SQLite:
# !!
# !! clave
# !! nombre
# !! puesto
# !! salario_diario
# !!
# !! Posteriormente se calculan:
# !!
# !! ponderacion
# !! puntos
# !! porcentaje
# !!
# !! ----------------------------------------------------------

def crear_trabajador(
    trabajador_bd,
    dias,
    numero_cuadrilla=None,
    horas_extras="",
    descripcion_horas_extras=""
):

    return {

        "clave": trabajador_bd[0],
        "nombre": trabajador_bd[1],
        "puesto": trabajador_bd[2],
        "salario_diario": float(trabajador_bd[3]),
        "dias": dias,

        "numero_cuadrilla": numero_cuadrilla,

        "horas_extras": horas_extras,
        "descripcion_horas_extras": descripcion_horas_extras,

        "ponderacion": 0,
        "puntos": 0,
        "porcentaje": 0

    }

# !! ----------------------------------------------------------
# !! crear_subtitulo()
# !!
# !! Representa una ubicación física dentro
# !! de la obra.
# !!
# !! Ejemplos:
# !!
# !! RECAMARA 01
# !! RECAMARA 02
# !! BAÑO PRINCIPAL
# !! COCINA
# !!
# !! Cada subtítulo puede contener
# !! múltiples conceptos.
# !!
# !! ----------------------------------------------------------

def crear_subtitulo(nombre):

    return {

        "nombre": nombre,

        "conceptos": [],

        "actividades": ""

    }


# !! ----------------------------------------------------------
# !! crear_concepto()
# !!
# !! Representa una captura de destajo.
# !!
# !! Datos provenientes de SQLite:
# !!
# !! clave
# !! descripcion
# !! unidad
# !!
# !! Datos capturados por usuario:
# !!
# !! largo
# !! ancho
# !! alto
# !! piezas
# !! notas
# !!
# !! Ejemplo:
# !!
# !! EXC01
# !! Excavación en cepa
# !! 2.00
# !! 0.50
# !! 0.40
# !! 1
# !! Excavación complicada en raíces
# !!
# !! ----------------------------------------------------------
def crear_concepto(
    concepto_bd,
    largo,
    ancho,
    alto,
    piezas,
    notas
):

    return {

        "clave": str(concepto_bd[0]).lower(),

        "descripcion": concepto_bd[1],

        "unidad": concepto_bd[2],

        "largo": largo,

        "ancho": ancho,

        "alto": alto,

        "piezas": piezas,

        "notas": notas

    }

# !! ----------------------------------------------------------
# !! obtener_siguiente_numero_cuadrilla()
# !!
# !! Calcula el siguiente número disponible para exportación.
# !!
# !! Revisa:
# !! - Cuadrillas de destajo
# !! - Trabajadores por día
# !!
# !! Esto es necesario porque:
# !!
# !! Destajo:
# !!   Cuadrilla 1 → todos comparten número 1
# !!
# !! Por día:
# !!   Cada trabajador tiene su propio número
# !!
# !! ----------------------------------------------------------
def obtener_siguiente_numero_cuadrilla(cuadrillas):

    numeros_usados = []

    for cuadrilla in cuadrillas:

        if cuadrilla["tipo"] == "destajo":

            if cuadrilla.get("numero") is not None:

                numeros_usados.append(
                    cuadrilla["numero"]
                )

        if cuadrilla["tipo"] == "dia":

            for trabajador in cuadrilla["trabajadores"]:

                if trabajador.get("numero_cuadrilla") is not None:

                    numeros_usados.append(
                        trabajador["numero_cuadrilla"]
                    )

    if len(numeros_usados) == 0:

        return 1

    return max(numeros_usados) + 1
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
def crear_trabajador(trabajador_bd, dias):

    return {

        "clave": trabajador_bd[0],

        "nombre": trabajador_bd[1],

        "puesto": trabajador_bd[2],

        "salario_diario": float(
            trabajador_bd[3]
        ),

        "dias": dias,

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

        "conceptos": []

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

        "clave": concepto_bd[0],

        "descripcion": concepto_bd[1],

        "unidad": concepto_bd[2],

        "largo": largo,

        "ancho": ancho,

        "alto": alto,

        "piezas": piezas,

        "notas": notas

    }
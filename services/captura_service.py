def crear_cuadrilla(numero, tipo):

    return {
        "numero": numero,
        "tipo": tipo,
        "trabajadores": [],
        "subtitulos": [],
        "conceptos": []
    }


def crear_trabajador(trabajador_bd, dias):

    return {
        "clave": trabajador_bd[0],
        "nombre": trabajador_bd[1],
        "puesto": trabajador_bd[2],
        "salario_diario": float(trabajador_bd[3]),
        "dias": dias,
        "ponderacion": 0,
        "puntos": 0,
        "porcentaje": 0
    }


def crear_subtitulo(nombre):

    return {
        "nombre": nombre,
        "conceptos": []
    }


def crear_concepto(concepto_bd, largo, ancho, alto, piezas, notas):

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
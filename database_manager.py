import sqlite3

DB = "data/nomina.db"


def conectar():
    return sqlite3.connect(DB)


def listar_obras():

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT clave_inter, nombre_obra
        FROM obras
        ORDER BY clave_inter
    """)

    obras = cursor.fetchall()

    conn.close()

    return obras


def listar_trabajadores():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT clave, nombre, puesto
        FROM trabajadores
        ORDER BY nombre
    """)

    datos = cursor.fetchall()

    conn.close()

    return datos


def buscar_trabajador(clave):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM trabajadores
        WHERE clave = ?
    """, (clave,))

    trabajador = cursor.fetchone()

    conn.close()

    return trabajador


def buscar_concepto(clave):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM conceptos
        WHERE clave = ?
    """, (clave,))

    concepto = cursor.fetchone()

    conn.close()

    return concepto


def listar_conceptos():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT clave, concepto, unidad
        FROM conceptos
        ORDER BY clave
    """)

    datos = cursor.fetchall()

    conn.close()

    return datos

def validar_usuario(usuario, password):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM usuarios
        WHERE usuario = ?
        AND password = ?
    """, (usuario, password))

    resultado = cursor.fetchone()

    conn.close()

    return resultado

def obtener_usuario(usuario):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM usuarios
        WHERE usuario = ?
    """, (usuario,))

    resultado = cursor.fetchone()

    conn.close()

    return resultado

def buscar_obras(texto):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT clave_inter, nombre_obra
        FROM obras
        WHERE UPPER(clave_inter) LIKE ?
        ORDER BY clave_inter
    """, (
        f"%{texto.upper()}%",
    ))

    obras = cursor.fetchall()

    conn.close()

    return obras
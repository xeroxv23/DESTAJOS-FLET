import sqlite3


# !! ==========================================================
# !! DATABASE_MANAGER.PY
# !!
# !! Capa de acceso a datos (SQLite).
# !!
# !! Responsabilidades:
# !! - Abrir conexión con SQLite.
# !! - Consultar obras.
# !! - Consultar trabajadores.
# !! - Consultar conceptos.
# !! - Validar usuarios.
# !!
# !! Este módulo NO contiene interfaz gráfica.
# !! Este módulo NO contiene lógica de Flet.
# !!
# !! Todas las vistas deben consultar la base de datos
# !! utilizando las funciones definidas aquí.
# !!
# !! Base de datos principal:
# !! data/nomina.db
# !!
# !! ==========================================================


# !! ==========================================================
# !! UBICACIÓN DE LA BASE DE DATOS
# !!
# !! Estructura actual:
# !!
# !! data/
# !! └── nomina.db
# !!
# !! ==========================================================
DB = "data/nomina.db"


# !! ==========================================================
# !! conectar()
# !!
# !! Función central para abrir SQLite.
# !!
# !! Todas las consultas utilizan esta función.
# !!
# !! Retorna:
# !! sqlite3.Connection
# !!
# !! ==========================================================
def conectar():
    return sqlite3.connect(DB)


# !! ==========================================================
# !! TABLA: obras
# !!
# !! Columnas principales:
# !! - clave_inter
# !! - direccion_obra
# !! - nombre_obra
# !!
# !! ==========================================================


# !! ----------------------------------------------------------
# !! listar_obras()
# !!
# !! Obtiene todas las obras.
# !!
# !! Retorna:
# !!
# !! [
# !!   ('A-001', 'CASA HABITACION'),
# !!   ('A-002', 'DEPARTAMENTO')
# !! ]
# !!
# !! Utilizado principalmente para pruebas.
# !! ----------------------------------------------------------
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

#region BUSCAR OBRA
# !! ----------------------------------------------------------
# !! buscar_obras()
# !!
# !! Utilizado por:
# !! obras_view.py
# !!
# !! Permite filtrar obras por clave.
# !!
# !! Ejemplos:
# !! A
# !! A-001
# !! ID-1211
# !!
# !! ----------------------------------------------------------
#endregion

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

#region !! TABLA: trabajadores
# !! ==========================================================
# !!
# !! Columnas:
# !! - clave
# !! - nombre
# !! - puesto
# !! - salario_diario
# !!
# !! Ejemplo:
# !!
# !! 3516
# !! ABARCA BARRAGAN JOSE
# !! PEON
# !! 307.25
# !!
# !! ==========================================================


# !! ----------------------------------------------------------
# !! listar_trabajadores()
# !!
# !! Devuelve catálogo completo de trabajadores.
# !!
# !! Utilizado para pruebas y validaciones.
# !! ----------------------------------------------------------
#endregion

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

#region BUSCAR TRABAJADOR
# !! ----------------------------------------------------------
# !! buscar_trabajador()
# !!
# !! Utilizado por:
# !! obra_view.py
# !!
# !! Busca un trabajador por número de nómina.
# !!
# !! Ejemplo:
# !! buscar_trabajador(3516)
# !!
# !! Retorna:
# !! (
# !!   3516,
# !!   'ABARCA BARRAGAN JOSE',
# !!   'PEON',
# !!   '307.25'
# !! )
# !!
# !! ----------------------------------------------------------
#endregion

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

#region TABLA CONCEPTOS
# !! ==========================================================
# !! TABLA: conceptos
# !!
# !! Columnas:
# !! - clave
# !! - concepto
# !! - unidad
# !!
# !! Ejemplo:
# !!
# !! ABB01
# !! Abrir caja para amarre en boveda
# !! ML
# !!
# !! ==========================================================


# !! ----------------------------------------------------------
# !! listar_conceptos()
# !!
# !! Devuelve catálogo completo de conceptos.
# !!
# !! Utilizado principalmente para pruebas.
# !! ----------------------------------------------------------
#endregion

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

#region BUSCAR CONCEPTO
# !! ----------------------------------------------------------
# !! buscar_concepto()
# !!
# !! Utilizado por:
# !! obra_view.py
# !!
# !! Busca una clave de destajo.
# !!
# !! Ejemplo:
# !! ABB01
# !!
# !! Retorna:
# !!
# !! (
# !!   'ABB01',
# !!   'Abrir caja para amarre en boveda',
# !!   'ML'
# !! )
# !!
# !! ----------------------------------------------------------
#endregion

def buscar_concepto(clave):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM conceptos
        WHERE UPPER(clave) = ?
    """, (clave.upper(),))

    concepto = cursor.fetchone()

    conn.close()

    return concepto

#region USUARIOS
# !! ==========================================================
# !! TABLA: usuarios
# !!
# !! Columnas:
# !! - usuario
# !! - password
# !! - nombre
# !! - rol
# !!
# !! Utilizada para Login.
# !!
# !! ==========================================================


# !! ----------------------------------------------------------
# !! validar_usuario()
# !!
# !! Utilizado por:
# !! login_view.py
# !!
# !! Verifica usuario y contraseña.
# !!
# !! Retorna:
# !! Usuario completo si existe.
# !! None si no existe.
# !!
# !! ----------------------------------------------------------
#endregion

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

#region OBTENER USUARIO
# !! ----------------------------------------------------------
# !! obtener_usuario()
# !!
# !! Obtiene la información completa de un usuario.
# !!
# !! Futuro:
# !! - Mostrar nombre del capturista.
# !! - Registrar quién realizó la captura.
# !! - Bitácora de modificaciones.
# !!
# !! ----------------------------------------------------------
#endregion

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

def obtener_obra(clave_inter):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT clave_inter, direccion_obra, nombre_obra
        FROM obras
        WHERE clave_inter = ?
    """, (clave_inter,))

    obra = cursor.fetchone()

    conn.close()

    return obra

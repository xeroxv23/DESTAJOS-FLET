import pandas as pd
import sqlite3

conn = sqlite3.connect("nomina.db")

# =====================
# TRABAJADORES
# =====================

trabajadores = pd.read_excel("TRABAJADORES BD.xlsx")

trabajadores.columns = [
    "clave",
    "nombre",
    "puesto",
    "salario_diario"
]

trabajadores.to_sql(
    "trabajadores",
    conn,
    if_exists="replace",
    index=False
)

print("✓ Trabajadores importados")


# =====================
# OBRAS
# =====================

obras = pd.read_excel("OBRAS BD.xlsx")

obras.columns = [
    "clave_inter",
    "direccion_obra",
    "nombre_obra"
]

obras.to_sql(
    "obras",
    conn,
    if_exists="replace",
    index=False
)

print("✓ Obras importadas")


# =====================
# CONCEPTOS
# =====================

conceptos = pd.read_excel("CONCEPTOS BD.xlsx")

conceptos.columns = [
    "clave",
    "concepto",
    "unidad",
    "precio_unitario"
]

conceptos.to_sql(
    "conceptos",
    conn,
    if_exists="replace",
    index=False
)

print("✓ Conceptos importados")


# =====================
# USUARIOS
# =====================

usuarios = pd.read_excel("LOGIN BD.xlsx")

usuarios.columns = [
    "usuario",
    "password",
    "nombre",
    "rol"
]

usuarios.to_sql(
    "usuarios",
    conn,
    if_exists="replace",
    index=False
)

print("✓ Usuarios importados")

conn.close()

print("\n✓ Base de datos actualizada correctamente")
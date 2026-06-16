# CAPTURADOR DESTAJOS

## Descripción General

Capturador Destajos es una aplicación desarrollada en Python utilizando Flet y SQLite para capturar información de destajos en obras de construcción.

El objetivo principal es permitir la captura en campo de:

* Cuadrillas
* Trabajadores
* Subtítulos (ubicaciones dentro de la obra)
* Conceptos de destajo
* Evidencias futuras
* Exportación final a Excel

La aplicación está diseñada para funcionar inicialmente en PC Windows y posteriormente ser adaptada para tablets Android.

---

# Objetivo del Proyecto

Actualmente la captura de destajos se realiza manualmente.

El objetivo es construir una herramienta que permita:

1. Seleccionar una obra.
2. Crear cuadrillas.
3. Registrar trabajadores.
4. Capturar conceptos ejecutados.
5. Calcular participación de trabajadores.
6. Exportar el resultado a un formato Excel final.

---

# Flujo General

Login

↓

Listado de Obras

↓

Obra Seleccionada

↓

Captura de Cuadrillas

↓

Captura de Trabajadores

↓

Captura de Subtítulos

↓

Captura de Conceptos

↓

Cerrar Cuadrilla

↓

Cerrar Destajo

↓

Exportar Excel

---

# Arquitectura Actual

```text
main.py
│
├── views
│   ├── login_view.py
│   ├── obras_view.py
│   └── obra_view.py
│
├── database_manager.py
│
├── services
│   ├── captura_service.py
│   └── cuadrilla_service.py
│
├── components
│   ├── dialogs.py
│   └── cuadrilla_card.py
│
├── data
│   └── nomina.db
│
└── assets
    └── logo.jpg
```

---

# Base de Datos

Ubicación:

```text
data/nomina.db
```

Motor:

```text
SQLite
```

---

# Tabla Usuarios

Campos:

```text
usuario
password
nombre
rol
```

Uso:

* Login
* Control de acceso
* Auditoría futura

---

# Tabla Obras

Campos:

```text
clave_inter
direccion_obra
nombre_obra
```

Uso:

* Selección de obra
* Inicio de captura

---

# Tabla Trabajadores

Campos:

```text
clave
nombre
puesto
salario_diario
```

Uso:

* Integración automática de datos de nómina
* Cálculo de participación

---

# Tabla Conceptos

Campos:

```text
clave
concepto
unidad
```

Uso:

* Catálogo de destajos
* Captura de conceptos

---

# Estructura de una Cuadrilla

Ejemplo:

Cuadrilla 1

Trabajadores:

```text
3950 JUAN PEREZ 60%
1990 MARTIN GUARDADO 40%
```

Subtítulo:

```text
RECAMARA 01
```

Concepto:

```text
EXC01

Largo: 2.00
Ancho: 0.50
Alto: 0.40
Piezas: 1

Nota:
Excavación complicada en raíces
```

---

# Cálculo de Participaciones

Reglas actuales:

```text
OF = 60 puntos
Cualquier otro puesto = 40 puntos
```

Fórmula:

```text
puntos = ponderacion × dias
```

Ejemplo:

```text
OF
6 días

60 × 6 = 360
```

```text
PEON
6 días

40 × 6 = 240
```

Total:

```text
600 puntos
```

Participaciones:

```text
360 / 600 = 60%
240 / 600 = 40%
```

---

# Estructura Interna de Datos

Cuadrilla:

```python
{
    "numero": 1,
    "tipo": "destajo",
    "trabajadores": [],
    "subtitulos": []
}
```

Trabajador:

```python
{
    "clave": 3950,
    "nombre": "JUAN PEREZ",
    "puesto": "OF",
    "dias": 6,
    "ponderacion": 60,
    "puntos": 360,
    "porcentaje": 60
}
```

Subtítulo:

```python
{
    "nombre": "RECAMARA 01",
    "conceptos": []
}
```

Concepto:

```python
{
    "clave": "EXC01",
    "descripcion": "Excavación",
    "unidad": "M3",
    "largo": 2.0,
    "ancho": 0.5,
    "alto": 0.4,
    "piezas": 1,
    "notas": "Excavación complicada"
}
```

---

# Funcionalidades Terminadas

* Login de usuarios.
* Validación SQLite.
* Búsqueda de obras.
* Apertura de obra.
* Creación de cuadrillas.
* Captura de trabajadores.
* Cálculo de porcentajes.
* Captura de subtítulos.
* Captura de conceptos.
* Consulta de conceptos desde BD.
* Arquitectura modular.
* Documentación de código.

---

# Funcionalidades Pendientes

## Captura

* Editar trabajadores.
* Eliminar trabajadores.
* Editar subtítulos.
* Eliminar subtítulos.
* Editar conceptos.
* Eliminar conceptos.

## Cuadrillas

* Cerrar cuadrilla.
* Bloquear edición al cerrar.

## Destajo

* Cerrar destajo completo.
* Resumen general.

## Exportación

* Generar Excel final.
* Formato corporativo.
* Integración con nómina.

## Evidencias

* Fotografías.
* Firmas digitales.

---

# Control de Versiones

Repositorio Git.

Comando para respaldo:

```bash
git add .
git commit -m "Descripcion del avance"
```

Ejemplo:

```bash
git commit -m "Cuadrillas, trabajadores y conceptos funcionando"
```

---

# Futuro del Proyecto

Versión 1.0

* Captura completa.
* Exportación Excel.

Versión 2.0

* Evidencias fotográficas.
* Firma digital.

Versión 3.0

* Sincronización en red.
* Dashboard administrativo.
* Reportes de productividad.
* Control histórico de obras.

---

# Autor

CARLOS ROBERTO VIDAL GARCIA

Desarrollado en:

* Python
* Flet
* SQLite

Estado actual:

En desarrollo activo.

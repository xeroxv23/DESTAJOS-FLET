# Capturador Destajos - Design System

## 1. Objetivo visual

La aplicación debe sentirse:

- Profesional
- Limpia
- Cómoda para tablet
- Fácil de usar en obra
- Consistente entre pantallas

No debe sentirse como:

- Una hoja de Excel
- Un sistema antiguo
- Una pantalla saturada
- Una app improvisada

---

## 2. Paleta de colores

### Principal

- Verde corporativo: `#5B6357`
- Verde oscuro: `#4B5447`
- Verde claro: `#7A8574`

### Fondos

- Fondo general: `#F4F5F2`
- Superficie / tarjetas: `#FFFFFF`

### Texto

- Texto principal: `#2F352D`
- Texto secundario: `#6D7569`

### Bordes

- Borde suave: `#D7DDD3`

### Estados

- Éxito: `#4CAF50`
- Advertencia: `#F4A62A`
- Error / eliminar: `#D9534F`
- Información: `#4A90E2`

---

## 3. Tamaños base

- Padding de página: `24`
- Padding de tarjeta: `20`
- Radio de tarjeta: `16`
- Altura de botón: `52`
- Altura de input: `56`

---

## 4. Componentes reutilizables

### app_header.py

Uso:
- Encabezado principal de una vista.
- Debe mostrar contexto del usuario.
- Puede incluir botón de regreso.

Ejemplo:
- Semana actual
- Obra actual
- Módulo actual

---

### app_actions.py

Uso:
- Barra de acciones principales.
- Se usa para botones importantes de una pantalla.

Ejemplo:
- Nueva cuadrilla
- Tomar fotografía
- Cerrar destajo

---

### app_card.py

Uso:
- Tarjetas individuales.
- Elementos de listas.
- Estados vacíos.

Ejemplo:
- Semana
- Evidencia
- Obra
- Trabajador

---

### app_panel.py

Uso:
- Secciones grandes de contenido.

Ejemplo:
- Resultados de búsqueda
- Cuadrillas capturadas
- Evidencias guardadas

---

### app_sidebar.py

Uso:
- Panel lateral corto.
- Lista secundaria con scroll.

Ejemplo:
- Obras capturadas
- Historial
- Resumen lateral

---

### app_search.py

Uso:
- Campos de búsqueda.
- Debe evitar ocupar todo el ancho si no es necesario.

Ejemplo:
- Buscar obra por clave
- Buscar trabajador
- Buscar concepto

---

## 5. Regla principal

Si un diseño se repite dos veces, debe evaluarse si conviene convertirlo en componente reutilizable.

---

## 6. Prioridad visual por pantalla

### obra_view.py

Prioridad:
1. Cuadrillas capturadas
2. Gestión de captura
3. Evidencias
4. Exportación

### obras_view.py

Prioridad:
1. Búsqueda de obra
2. Resultados
3. Obras capturadas

### evidencias_view.py

Prioridad:
1. Agregar evidencia
2. Evidencias guardadas
3. Eliminar evidencia

---

## 7. Reglas para tablet

- Botones grandes
- Campos cómodos
- Poco texto por pantalla
- Evitar saturación visual
- Usar scroll interno cuando sea necesario
- Priorizar lectura rápida
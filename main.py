import flet as ft
from services.file_manager import crear_estructura_base

# ==========================================================
# IMPORTACIÓN DE ESTILOS GLOBALES
#
# Se importan los colores, tamaños y configuraciones
# visuales definidos en styles.py para mantener una
# identidad visual consistente en toda la aplicación.
# ==========================================================

from styles import (
    COLOR_BACKGROUND,
    COLOR_PRIMARY,
    PAGE_PADDING,
    APP_TITLE,
)

# ==========================================================
# IMPORTACIÓN DE VISTAS
#
# login_view es la primera pantalla del sistema.
# Desde aquí se validan usuarios y posteriormente
# se navega al resto de módulos.
# ==========================================================

from views.login_view import login_view



#region MAIN.PY

# ==========================================================
# FUNCIÓN PRINCIPAL
#
# Punto de entrada de la aplicación.
#
# Responsabilidades:
# - Configurar apariencia general
# - Configurar tamaño inicial de ventana
# - Aplicar tema corporativo
# - Cargar la primera vista
#
# Flujo:
#
# ft.run(main)
#        ↓
#     main(page)
#        ↓
# Configura interfaz
#        ↓
# Carga Login
#        ↓
# Usuario inicia sesión
# ==========================================================

def main(page: ft.Page):

    # ======================================================
    # CONFIGURACIÓN GENERAL DE LA APLICACIÓN
    # ======================================================

    # Título mostrado en la ventana
    page.title = APP_TITLE

    # ======================================================
    # CONFIGURACIÓN INICIAL PARA TABLET
    #
    # Estos valores sirven principalmente durante el
    # desarrollo en PC simulando una tablet horizontal.
    #
    # En Android o iPad se adaptará automáticamente al
    # tamaño real del dispositivo.
    # ======================================================

    page.window_width = 1200
    page.window_height = 800

    # ======================================================
    # ESTILO VISUAL GLOBAL
    #
    # Se aplica el color de fondo definido en styles.py
    # para toda la aplicación.
    # ======================================================

    page.bgcolor = COLOR_BACKGROUND

    # Espaciado general alrededor de todas las vistas
    page.padding = PAGE_PADDING

    # ======================================================
    # TEMA GLOBAL
    #
    # Utiliza el color corporativo principal como base
    # para botones, controles y elementos visuales.
    # ======================================================

    page.theme = ft.Theme(
        color_scheme_seed=COLOR_PRIMARY,
    )

    # ======================================================
    # CARGA DE LA PRIMERA PANTALLA
    #
    # Se limpia cualquier vista existente y se agrega
    # la pantalla de Login como punto inicial.
    # ======================================================

    page.views.clear()
    page.views.append(login_view(page))

    # Refresca la interfaz para mostrar los cambios
    page.update()


# ==========================================================
# INICIO DE LA APLICACIÓN
#
# Ejecuta la función principal y crea la ventana
# de la aplicación.
# ==========================================================

ft.run(main)

#endregion
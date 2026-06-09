import flet as ft

from views.vacaciones_view import vacaciones_view

# =====================================
# FLUJO DE LA APLICACION
# =====================================
#
# Login
#   ↓
# Listado de Obras
#   ↓
# Obra Seleccionada
#   ↓
# Captura de Destajos
#   ↓
# Exportar Obra
#
# =====================================

def main(page: ft.Page):

    page.title = "Consulta de vacaciones"

    # =====================================
    # CONFIGURACION PARA DESARROLLO EN PC
    # =====================================

    page.window.width = 1200
    page.window.height = 800

    page.padding = 20

    # =====================================
    # CONFIGURACION FUTURA PARA TABLET
    # =====================================
    #
    # Cuando la aplicación sea desplegada
    # en tablets Android:
    #
    # page.window.maximized = True
    #
    # o
    #
    # page.window.full_screen = True
    #
    # Revisar compatibilidad según el
    # método final de empaquetado.
    #
    # =====================================

    page.views.append(
        vacaciones_view(page)
    )

    page.update()


ft.run(
    main,
    assets_dir="assets"
)
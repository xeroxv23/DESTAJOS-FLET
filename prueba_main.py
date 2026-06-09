import flet as ft

from views.obras_view import obras_view


def main(page: ft.Page):

    page.title = "Capturador Destajos"

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
    # page.window.maximized = True
    #
    # o
    #
    # page.window.full_screen = True
    #
    # =====================================

    page.views.append(
        obras_view(page)
    )

    page.update()


ft.run(
    main,
    assets_dir="assets"
)
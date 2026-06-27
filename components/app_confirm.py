import flet as ft

from styles import (
    COLOR_TEXT,
    COLOR_MUTED,
    COLOR_DANGER,
    SUBTITLE_SIZE,
    TEXT_SIZE,
    SMALL_TEXT_SIZE,
)

from components.app_button import crear_app_button


def abrir_app_confirm(
    page,
    titulo,
    mensaje,
    on_confirmar,
    texto_confirmar="Eliminar",
    texto_cancelar="Cancelar",
):

    def confirmar(e):
        dialog.open = False
        page.update()
        on_confirmar()

    def cancelar(e):
        dialog.open = False
        page.update()

    dialog = ft.AlertDialog(
        modal=True,

        title=ft.Text(
            titulo,
            size=SUBTITLE_SIZE,
            weight=ft.FontWeight.BOLD,
            color=COLOR_TEXT,
        ),

        content=ft.Text(
            mensaje,
            size=TEXT_SIZE,
            color=COLOR_MUTED,
        ),

        actions=[
            ft.TextButton(
                texto_cancelar,
                on_click=cancelar,
            ),

            crear_app_button(
                texto=texto_confirmar,
                on_click=confirmar,
                tipo="danger",
            ),
        ],
    )

    page.overlay.append(dialog)
    dialog.open = True
    page.update()
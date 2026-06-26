import flet as ft

from styles import (
    COLOR_BACKGROUND,
    COLOR_TEXT,
    COLOR_MUTED,
    CARD_RADIUS,
    TEXT_SIZE,
    SMALL_TEXT_SIZE,
)


def crear_app_empty(
    titulo,
    descripcion="",
):

    return ft.Container(
        padding=20,
        bgcolor=COLOR_BACKGROUND,
        border_radius=CARD_RADIUS,

        content=ft.Column(
            spacing=8,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    titulo,
                    size=TEXT_SIZE,
                    weight=ft.FontWeight.BOLD,
                    color=COLOR_TEXT,
                    text_align=ft.TextAlign.CENTER,
                ),

                ft.Text(
                    descripcion,
                    size=SMALL_TEXT_SIZE,
                    color=COLOR_MUTED,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
        ),
    )
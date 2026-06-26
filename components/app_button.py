import flet as ft

from styles import (
    COLOR_PRIMARY,
    COLOR_PRIMARY_DARK,
    COLOR_SUCCESS,
    COLOR_DANGER,
    COLOR_WARNING,
    COLOR_SURFACE,
    BUTTON_HEIGHT,
    TEXT_SIZE,
)


def crear_app_button(
    texto,
    on_click,
    tipo="primary",
    width=None,
):

    if tipo == "success":
        bgcolor = COLOR_SUCCESS
        color = "white"

    elif tipo == "danger":
        bgcolor = COLOR_DANGER
        color = "white"

    elif tipo == "warning":
        bgcolor = COLOR_WARNING
        color = "white"

    elif tipo == "secondary":
        bgcolor = COLOR_SURFACE
        color = COLOR_PRIMARY_DARK

    else:
        bgcolor = COLOR_PRIMARY
        color = "white"

    return ft.ElevatedButton(
        height=BUTTON_HEIGHT,
        width=width,
        bgcolor=bgcolor,
        color=color,
        content=ft.Text(
            texto,
            size=TEXT_SIZE,
            weight=ft.FontWeight.BOLD,
        ),
        on_click=on_click,
    )
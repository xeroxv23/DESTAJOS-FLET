import flet as ft

from styles import (
    COLOR_SURFACE,
    COLOR_BACKGROUND,
    COLOR_TEXT,
    COLOR_MUTED,
    COLOR_BORDER,
    CARD_RADIUS,
    CARD_PADDING,
    SUBTITLE_SIZE,
    TEXT_SIZE,
    SMALL_TEXT_SIZE,
)

#COMPONENTES
from components.app_empty import crear_app_empty

#region APP_CARD.PY

# !! ==========================================================
# !! APP_CARD.PY
# !!
# !! Componente reutilizable para tarjetas visuales.
# !!
# !! Responsabilidades:
# !! - Mantener mismo borde, padding y fondo
# !! - Mostrar título opcional
# !! - Mostrar subtítulo opcional
# !! - Recibir contenido personalizado
# !!
# !! Beneficio:
# !! Evita repetir ft.Container(...) en todas las vistas.
# !! ==========================================================


def crear_app_card(
    contenido,
    titulo="",
    subtitulo="",
    expand=False,
    padding=CARD_PADDING,
    bgcolor=COLOR_SURFACE,
):

    controles = []

    if titulo:
        controles.append(
            ft.Text(
                titulo,
                size=SUBTITLE_SIZE,
                weight=ft.FontWeight.BOLD,
                color=COLOR_TEXT,
            )
        )

    if subtitulo:
        controles.append(
            ft.Text(
                subtitulo,
                size=SMALL_TEXT_SIZE,
                color=COLOR_MUTED,
            )
        )

    if titulo or subtitulo:
        controles.append(
            ft.Container(height=4)
        )

    controles.append(contenido)

    return ft.Container(
        expand=expand,
        padding=padding,
        bgcolor=bgcolor,
        border_radius=CARD_RADIUS,
        border=ft.Border(
            left=ft.BorderSide(1, COLOR_BORDER),
            top=ft.BorderSide(1, COLOR_BORDER),
            right=ft.BorderSide(1, COLOR_BORDER),
            bottom=ft.BorderSide(1, COLOR_BORDER),
        ),

        content=ft.Column(
            expand=expand,
            spacing=10,
            controls=controles,
        ),
    )


def crear_app_empty_card(
    titulo,
    descripcion="",
):

    return crear_app_card(
        contenido=crear_app_empty(
            titulo=titulo,
            descripcion=descripcion,
        ),
        bgcolor=COLOR_BACKGROUND,
    )

#endregion
import flet as ft

from styles import (
    COLOR_SURFACE,
    COLOR_TEXT,
    COLOR_MUTED,
    COLOR_BORDER,
    CARD_RADIUS,
    SUBTITLE_SIZE,
    SMALL_TEXT_SIZE,
)


#region APP_PANEL.PY

# !! ==========================================================
# !! APP_PANEL.PY
# !!
# !! Panel reutilizable para secciones grandes.
# !!
# !! Uso recomendado:
# !! - Resultados de búsqueda
# !! - Obras capturadas
# !! - Listados principales
# !! - Módulos con contenido expandible
# !! ==========================================================


def crear_app_panel(
    titulo,
    contenido,
    subtitulo="",
    expand=False,
    width=None,
    padding=16,
):

    controles = [
        ft.Text(
            titulo,
            size=SUBTITLE_SIZE,
            weight=ft.FontWeight.BOLD,
            color=COLOR_TEXT,
        )
    ]

    if subtitulo:
        controles.append(
            ft.Text(
                subtitulo,
                size=SMALL_TEXT_SIZE,
                color=COLOR_MUTED,
            )
        )

    controles.append(contenido)

    return ft.Container(
        expand=expand,
        width=width,
        padding=padding,
        bgcolor=COLOR_SURFACE,
        border_radius=CARD_RADIUS,
        border=ft.Border(
            left=ft.BorderSide(1, COLOR_BORDER),
            top=ft.BorderSide(1, COLOR_BORDER),
            right=ft.BorderSide(1, COLOR_BORDER),
            bottom=ft.BorderSide(1, COLOR_BORDER),
        ),

        content=ft.Column(
            expand=expand,
            spacing=12,
            controls=controles,
        ),
    )


#endregion
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


#region APP_SIDEBAR.PY

# !! ==========================================================
# !! APP_SIDEBAR.PY
# !!
# !! Componente reutilizable para paneles laterales.
# !!
# !! Uso recomendado:
# !! - Obras capturadas
# !! - Historial
# !! - Menús laterales
# !! - Listas pequeñas con scroll
# !! ==========================================================


def crear_app_sidebar(
    titulo,
    contenido,
    subtitulo="",
    width=360,
    height=420,
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

    controles.append(
        ft.Container(
            expand=True,
            content=contenido,
        )
    )

    return ft.Container(
        width=width,
        height=height,
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
            expand=True,
            spacing=12,
            controls=controles,
        ),
    )


#endregion
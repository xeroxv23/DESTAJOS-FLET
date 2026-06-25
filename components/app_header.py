import flet as ft

from styles import (
    COLOR_PRIMARY_DARK,
    COLOR_SURFACE,
    CARD_RADIUS,
    BUTTON_HEIGHT,
    TITLE_SIZE,
    TEXT_SIZE,
    SMALL_TEXT_SIZE,
)


#region APP_HEADER.PY

# !! ==========================================================
# !! APP_HEADER.PY
# !!
# !! Encabezado reutilizable para vistas principales.
# !!
# !! Responsabilidades:
# !! - Mostrar título principal
# !! - Mostrar subtítulo
# !! - Mostrar botón de regreso opcional
# !! - Mantener navegación visual consistente
# !! ==========================================================


def crear_app_header(
    titulo,
    subtitulo="",
    descripcion="",
    texto_boton="Regresar",
    on_regresar=None
):

    controles_texto = [
        ft.Text(
            titulo,
            size=TITLE_SIZE,
            weight=ft.FontWeight.BOLD,
            color="white",
        )
    ]

    if subtitulo:
        controles_texto.append(
            ft.Text(
                subtitulo,
                size=TEXT_SIZE,
                color="white",
            )
        )

    if descripcion:
        controles_texto.append(
            ft.Text(
                descripcion,
                size=SMALL_TEXT_SIZE,
                color="#E5E7EB",
            )
        )

    controles_header = [
        ft.Column(
            spacing=5,
            expand=True,
            controls=controles_texto,
        )
    ]

    if on_regresar is not None:

        controles_header.append(
            ft.ElevatedButton(
                height=BUTTON_HEIGHT,
                bgcolor=COLOR_SURFACE,
                color=COLOR_PRIMARY_DARK,
                content=ft.Text(
                    texto_boton,
                    size=TEXT_SIZE,
                    weight=ft.FontWeight.BOLD,
                ),
                on_click=on_regresar,
            )
        )

    return ft.Container(
        padding=20,
        bgcolor=COLOR_PRIMARY_DARK,
        border_radius=CARD_RADIUS,

        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=controles_header,
        ),
    )


#endregion

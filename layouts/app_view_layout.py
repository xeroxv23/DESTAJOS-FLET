import flet as ft

from styles import (
    COLOR_BACKGROUND,
    PAGE_PADDING,
)


#region APP_VIEW_LAYOUT.PY

# !! ==========================================================
# !! APP_VIEW_LAYOUT.PY
# !!
# !! Layout base para vistas principales.
# !!
# !! Responsabilidades:
# !! - Aplicar fondo general
# !! - Aplicar padding estándar
# !! - Envolver contenido en una columna principal
# !! - Evitar repetir estructura en cada view
# !! ==========================================================


def crear_app_view(
    route,
    controls,
    spacing=16,
):

    return ft.View(
        route=route,
        bgcolor=COLOR_BACKGROUND,
        padding=PAGE_PADDING,

        controls=[
            ft.Column(
                expand=True,
                spacing=spacing,
                controls=controls,
            )
        ],
    )


#endregion
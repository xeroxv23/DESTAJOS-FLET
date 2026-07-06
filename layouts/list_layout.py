import flet as ft

from components.app_header import crear_app_header
from components.app_actions import crear_app_actions

from layouts.app_view_layout import crear_app_view

from styles import (
    COLOR_TEXT,
    COLOR_MUTED,
    TITLE_SIZE,
    TEXT_SIZE,
)


#region LIST_LAYOUT.PY

# !! ==========================================================
# !! LIST_LAYOUT.PY
# !!
# !! Layout especializado para pantallas tipo listado.
# !!
# !! Responsabilidades:
# !! - Crear estructura estándar para vistas de listado
# !! - Mostrar header superior reutilizable
# !! - Mostrar panel de acciones opcional
# !! - Mostrar título y descripción del listado
# !! - Insertar contenido principal dinámico
# !!
# !! Ejemplos de uso:
# !! - semanas_view.py
# !! - obras_view.py
# !! - futuras vistas administrativas
# !! ==========================================================


def crear_list_layout(
    route,
    header_titulo,
    header_subtitulo,
    titulo,
    descripcion,
    contenido,
    acciones_titulo=None,
    acciones_descripcion=None,
    acciones=None,
    spacing=16,
):
    controls = [

        crear_app_header(
            titulo=header_titulo,
            subtitulo=header_subtitulo,
        ),
    ]

    if acciones is not None:
        controls.append(
            crear_app_actions(
                titulo=acciones_titulo,
                descripcion=acciones_descripcion,
                acciones=acciones,
            )
        )

    controls.extend(
        [
            ft.Container(height=18),

            ft.Text(
                titulo,
                size=TITLE_SIZE,
                weight=ft.FontWeight.BOLD,
                color=COLOR_TEXT,
            ),

            ft.Text(
                descripcion,
                size=TEXT_SIZE,
                color=COLOR_MUTED,
            ),

            ft.Container(height=10),

            contenido,
        ]
    )

    return crear_app_view(
        route=route,
        controls=controls,
        spacing=spacing,
    )


#endregion
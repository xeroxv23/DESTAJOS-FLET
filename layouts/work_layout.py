import flet as ft

from components.app_header import crear_app_header

from layouts.app_view_layout import crear_app_view

from styles import (
    COLOR_TEXT,
    COLOR_MUTED,
    TITLE_SIZE,
    TEXT_SIZE,
)


#region WORK_LAYOUT.PY

# !! ==========================================================
# !! WORK_LAYOUT.PY
# !!
# !! Layout especializado para pantallas de trabajo.
# !!
# !! Responsabilidades:
# !! - Crear estructura estándar para vistas de operación/captura
# !! - Mostrar header superior reutilizable
# !! - Mostrar título y descripción opcionales
# !! - Insertar contenido principal dinámico
# !!
# !! Ejemplos de uso:
# !! - obras_view.py
# !! - obra_view.py
# !! - evidencias_view.py
# !! - preview_view.py
# !! ==========================================================


def crear_work_layout(
    route,
    header_titulo,
    header_subtitulo,
    controls,
    titulo=None,
    descripcion=None,
    header_descripcion=None,
    texto_boton=None,
    on_regresar=None,
    spacing=16,
):
    controls_view = [
        crear_app_header(
            titulo=header_titulo,
            subtitulo=header_subtitulo,
            descripcion=header_descripcion,
            texto_boton=texto_boton,
            on_regresar=on_regresar,
        ),
    ]

    # El bloque de título y descripción es opcional.
    if titulo is not None or descripcion is not None:

        controls_view.append(
            ft.Container(height=18)
        )

        if titulo is not None:
            controls_view.append(
                ft.Text(
                    titulo,
                    size=TITLE_SIZE,
                    weight=ft.FontWeight.BOLD,
                    color=COLOR_TEXT,
                )
            )

        if descripcion is not None:
            controls_view.append(
                ft.Text(
                    descripcion,
                    size=TEXT_SIZE,
                    color=COLOR_MUTED,
                )
            )

        controls_view.append(
            ft.Container(height=10)
        )

    controls_view.extend(controls)

    return crear_app_view(
        route=route,
        controls=controls_view,
        spacing=spacing,
    )


#endregion
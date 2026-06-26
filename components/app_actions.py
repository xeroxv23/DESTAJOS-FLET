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

#COMPONENTES
from components.app_button import crear_app_button

#region APP_ACTIONS.PY

# !! ==========================================================
# !! APP_ACTIONS.PY
# !!
# !! Componente reutilizable para barras de acciones.
# !!
# !! Responsabilidades:
# !! - Mostrar título de sección
# !! - Mostrar descripción corta
# !! - Mostrar botones de acción
# !! - Mantener diseño consistente en módulos principales
# !!
# !! Ejemplo:
# !! Gestión de captura
# !! Agrega cuadrillas, evidencias o cierra el destajo.
# !! [Nueva cuadrilla] [Tomar fotografía] [Cerrar destajo]
# !! ==========================================================

def crear_app_actions(
    titulo,
    descripcion="",
    acciones=None,
):

    if acciones is None:
        acciones = []

    botones = []

    for accion in acciones:

        botones.append(
            crear_app_button(
                texto=accion["texto"],
                on_click=accion["on_click"],
                tipo=accion.get("tipo", "primary"),
            )
        )

    return ft.Container(
        padding=16,
        bgcolor=COLOR_SURFACE,
        border_radius=CARD_RADIUS,
        border=ft.Border(
            left=ft.BorderSide(1, COLOR_BORDER),
            top=ft.BorderSide(1, COLOR_BORDER),
            right=ft.BorderSide(1, COLOR_BORDER),
            bottom=ft.BorderSide(1, COLOR_BORDER),
        ),

        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,

            controls=[

                ft.Column(
                    spacing=4,
                    expand=True,
                    controls=[

                        ft.Text(
                            titulo,
                            size=SUBTITLE_SIZE,
                            weight=ft.FontWeight.BOLD,
                            color=COLOR_TEXT,
                        ),

                        ft.Text(
                            descripcion,
                            size=SMALL_TEXT_SIZE,
                            color=COLOR_MUTED,
                        ),
                    ],
                ),

                ft.Row(
                    spacing=10,
                    controls=botones,
                ),
            ],
        ),
    )


#endregion
import flet as ft

from styles import (
    COLOR_PRIMARY,
    COLOR_SUCCESS,
    COLOR_DANGER,
    COLOR_SURFACE,
    COLOR_PRIMARY_DARK,
    COLOR_TEXT,
    COLOR_MUTED,
    COLOR_BORDER,
    CARD_RADIUS,
    BUTTON_HEIGHT,
    SUBTITLE_SIZE,
    TEXT_SIZE,
    SMALL_TEXT_SIZE,
)


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


def crear_boton_accion(
    texto,
    on_click,
    tipo="primary",
):

    if tipo == "success":
        bgcolor = COLOR_SUCCESS
        color = "white"

    elif tipo == "danger":
        bgcolor = COLOR_DANGER
        color = "white"

    elif tipo == "secondary":
        bgcolor = COLOR_SURFACE
        color = COLOR_PRIMARY_DARK

    else:
        bgcolor = COLOR_PRIMARY
        color = "white"

    return ft.ElevatedButton(
        height=BUTTON_HEIGHT,
        bgcolor=bgcolor,
        color=color,
        content=ft.Text(
            texto,
            size=TEXT_SIZE,
            weight=ft.FontWeight.BOLD,
        ),
        on_click=on_click,
    )


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
            crear_boton_accion(
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
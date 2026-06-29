import flet as ft

from styles import (
    COLOR_TEXT,
    COLOR_MUTED,
    SUBTITLE_SIZE,
    TEXT_SIZE,
    SMALL_TEXT_SIZE,
)

from components.app_button import crear_app_button


#region APP_DIALOG.PY

# !! ==========================================================
# !! APP_DIALOG.PY
# !!
# !! Componente reutilizable para diálogos corporativos.
# !!
# !! Uso:
# !! - Formularios emergentes
# !! - Capturas rápidas
# !! - Ventanas de confirmación avanzada
# !! - Procesos de guardado
# !! ==========================================================


def crear_app_dialog(
    titulo,
    contenido,
    on_guardar=None,
    on_cancelar=None,
    texto_guardar="Guardar",
    texto_cancelar="Cancelar",
    descripcion="",
    width=420,
    modal=True,
):

    controles = []

    if descripcion:
        controles.append(
            ft.Text(
                descripcion,
                size=SMALL_TEXT_SIZE,
                color=COLOR_MUTED,
            )
        )

    if isinstance(contenido, list):
        controles.extend(contenido)
    else:
        controles.append(contenido)

    acciones = []

    if on_cancelar is not None:
        acciones.append(
            ft.TextButton(
                texto_cancelar,
                on_click=on_cancelar,
            )
        )

    if on_guardar is not None:
        acciones.append(
            crear_app_button(
                texto=texto_guardar,
                on_click=on_guardar,
                tipo="primary",
            )
        )

    return ft.AlertDialog(
        modal=modal,

        title=ft.Text(
            titulo,
            size=SUBTITLE_SIZE,
            weight=ft.FontWeight.BOLD,
            color=COLOR_TEXT,
        ),

        content=ft.Container(
            width=width,
            content=ft.Column(
                spacing=14,
                tight=True,
                controls=controles,
            ),
        ),

        actions=acciones,
    )


#endregion
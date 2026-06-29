import flet as ft

from styles import (
    COLOR_PRIMARY,
    COLOR_BORDER,
    TEXT_SIZE,
    INPUT_HEIGHT,
)


#region APP_FORM.PY

# !! ==========================================================
# !! APP_FORM.PY
# !!
# !! Componentes reutilizables para formularios.
# !!
# !! Uso:
# !! - Diálogos
# !! - Captura de trabajadores
# !! - Captura de conceptos
# !! - Evidencias
# !! - Configuración
# !! ==========================================================


def crear_app_textfield(
    label,
    value="",
    hint_text="",
    multiline=False,
    width=None,
    autofocus=False,
    on_change=None,
    on_submit=None,
    color=None,
    focused_border_color=None,
):

    return ft.TextField(
        label=label,
        value=value,
        hint_text=hint_text,
        multiline=multiline,
        width=width,
        height=90 if multiline else INPUT_HEIGHT,
        border_color=COLOR_BORDER,
        focused_border_color=focused_border_color or COLOR_PRIMARY,
        text_size=TEXT_SIZE,
        autofocus=autofocus,
        on_change=on_change,
        on_submit=on_submit,
        color=color,
    )


def crear_app_numberfield(
    label,
    value="",
    hint_text="",
    width=None,
    autofocus=False,
    on_change=None,
    on_submit=None,
):

    return crear_app_textfield(
        label=label,
        value=value,
        hint_text=hint_text,
        width=width,
        autofocus=autofocus,
        on_change=on_change,
        on_submit=on_submit,
    )


def crear_app_multiline(
    label,
    value="",
    hint_text="",
    width=None,
    autofocus=False,
    on_change=None,
):

    return crear_app_textfield(
        label=label,
        value=value,
        hint_text=hint_text,
        multiline=True,
        width=width,
        autofocus=autofocus,
        on_change=on_change,
    )


#endregion
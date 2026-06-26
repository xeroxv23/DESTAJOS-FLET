import flet as ft

from styles import (
    COLOR_PRIMARY,
    COLOR_BORDER,
    TEXT_SIZE,
)


#region APP_SEARCH.PY

# !! ==========================================================
# !! APP_SEARCH.PY
# !!
# !! Campo reutilizable de búsqueda.
# !!
# !! Uso recomendado:
# !! - Buscar obras
# !! - Buscar trabajadores
# !! - Buscar conceptos
# !! - Buscar semanas
# !! ==========================================================


def crear_app_search(
    label,
    hint_text="",
    on_change=None,
    width=420,
    autofocus=False,
):

    return ft.TextField(
        label=label,
        hint_text=hint_text,
        width=width,
        height=56,
        text_size=TEXT_SIZE,
        border_color=COLOR_BORDER,
        focused_border_color=COLOR_PRIMARY,
        autofocus=autofocus,
        on_change=on_change,
    )


#endregion
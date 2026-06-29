import flet as ft

from styles import (
    COLOR_TEXT,
    COLOR_MUTED,
    SUBTITLE_SIZE,
    TEXT_SIZE,
)


#region APP_LOADING.PY

# !! ==========================================================
# !! APP_LOADING.PY
# !!
# !! Componente reutilizable para mostrar procesos en curso.
# !!
# !! Uso:
# !! - Exportar Excel
# !! - Generar respaldos
# !! - Sincronizar
# !! - Procesar evidencias
# !! ==========================================================


def crear_app_loading_dialog(
    titulo="Procesando",
    mensaje="Por favor espere..."
):

    return ft.AlertDialog(
        modal=True,

        title=ft.Text(
            titulo,
            size=SUBTITLE_SIZE,
            weight=ft.FontWeight.BOLD,
            color=COLOR_TEXT,
        ),

        content=ft.Column(
            tight=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=14,
            controls=[
                ft.ProgressRing(),

                ft.Text(
                    mensaje,
                    size=TEXT_SIZE,
                    color=COLOR_MUTED,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
        ),
    )


#endregion
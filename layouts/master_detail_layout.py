import flet as ft


#region MASTER_DETAIL_LAYOUT.PY

# !! ==========================================================
# !! MASTER_DETAIL_LAYOUT.PY
# !!
# !! Layout especializado para pantallas maestro-detalle.
# !!
# !! Responsabilidades:
# !! - Organizar un panel principal de navegación
# !! - Organizar un panel de detalle
# !! - Mantener separación y proporciones consistentes
# !! - No contener lógica específica de negocio
# !!
# !! Ejemplos de uso:
# !! - selección de cuadrillas y detalle de captura
# !! - futuros catálogos administrativos
# !! - trabajadores, conceptos, residentes o usuarios
# !! ==========================================================


def crear_master_detail_layout(
    master,
    detail,
    master_width=420,
    spacing=16,
):
    return ft.Row(
        expand=True,
        spacing=spacing,
        vertical_alignment=ft.CrossAxisAlignment.START,

        controls=[
            ft.Container(
                width=master_width,
                content=master,
            ),

            ft.Container(
                expand=True,
                content=detail,
            ),
        ],
    )


#endregion
import flet as ft


def obra_view(
    page,
    clave_obra,
    nombre_obra
):

    return ft.View(
        route="/obra",

        controls=[

            ft.Text(
                "OBRA SELECCIONADA",
                size=28,
                weight=ft.FontWeight.BOLD
            ),

            ft.Divider(),

            ft.Text(
                f"Clave: {clave_obra}",
                size=18
            ),

            ft.Text(
                f"Obra: {nombre_obra}",
                size=18
            ),

            ft.Divider(),

            ft.ElevatedButton(
                content=ft.Text(
                    "Agregar trabajadores"
                )
            ),

            ft.ElevatedButton(
                content=ft.Text(
                    "Agregar subtitulo"
                )
            ),

            ft.ElevatedButton(
                content=ft.Text(
                    "Agregar concepto"
                )
            ),

            ft.ElevatedButton(
                content=ft.Text(
                    "Cerrar destajo"
                )
            ),

            ft.ElevatedButton(
                content=ft.Text(
                    "Exportar obra"
                )
            )

        ]
    )
import flet as ft


def obra_view(page, clave_obra, nombre_obra):

    def nueva_cuadrilla(e):

        tipo = ft.RadioGroup(

            content=ft.Column(

                controls=[

                    ft.Radio(
                        value="dia",
                        label="Por Día"
                    ),

                    ft.Radio(
                        value="destajo",
                        label="Destajo"
                    )

                ]

            )

        )

        def guardar(ev):

            print("TIPO SELECCIONADO:", tipo.value)

            dialog.open = False

            page.update()

        def cancelar(ev):

            dialog.open = False

            page.update()

        dialog = ft.AlertDialog(

            title=ft.Text(
                "Nueva Cuadrilla"
            ),

            content=tipo,

            actions=[

                ft.TextButton(
                    "Cancelar",
                    on_click=cancelar
                ),

                ft.TextButton(
                    "Guardar",
                    on_click=guardar
                )

            ]

        )

        page.overlay.append(dialog)

        dialog.open = True

        page.update()

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
                    "Nueva Cuadrilla"
                ),
                on_click=nueva_cuadrilla
            ),

            ft.ElevatedButton(
                content=ft.Text(
                    "Cerrar Destajo"
                )
            )

        ]

    )
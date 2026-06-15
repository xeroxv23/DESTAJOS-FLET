import flet as ft


def abrir_dialogo_nueva_cuadrilla(
    page,
    cuadrillas,
    crear_cuadrilla,
    actualizar_cuadrillas
):

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

        if not tipo.value:
            return

        numero = len(cuadrillas) + 1

        cuadrillas.append(
            crear_cuadrilla(
                numero,
                tipo.value
            )
        )

        dialog.open = False

        actualizar_cuadrillas()

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
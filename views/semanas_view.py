import flet as ft

from views.obras_view import obras_view

from services.semanas_service import (
    agregar_semana,
    eliminar_semana,
    listar_semanas
)


def semanas_view(page):

    lista_semanas = ft.Column(
        spacing=10
    )

    def actualizar_semanas():

        lista_semanas.controls.clear()

        if len(listar_semanas()) == 0:

            lista_semanas.controls.append(
                ft.Text("No hay semanas creadas")
            )

        else:

            for semana in listar_semanas():

                def abrir_semana(e, semana=semana):

                    page.views.append(
                        obras_view(
                            page,
                            semana
                        )
                    )

                    page.update()

                def borrar_semana(e, semana=semana):

                    eliminar_semana(semana)

                    actualizar_semanas()

                lista_semanas.controls.append(

                    ft.Card(
                        content=ft.Container(
                            padding=15,
                            content=ft.Column(
                                controls=[

                                    ft.Text(
                                        f"Semana {semana['numero']}",
                                        size=20,
                                        weight=ft.FontWeight.BOLD
                                    ),

                                    ft.Text(
                                        f"Inicio: {semana['fecha_inicio']}"
                                    ),

                                    ft.Text(
                                        f"Cierre: {semana['fecha_fin']}"
                                    ),

                                    ft.Row(
                                        controls=[

                                            ft.ElevatedButton(
                                                content=ft.Text(
                                                    "Abrir Semana"
                                                ),
                                                on_click=abrir_semana
                                            ),

                                            ft.TextButton(
                                                "Eliminar",
                                                on_click=borrar_semana
                                            )

                                        ]
                                    )

                                ]
                            )
                        )
                    )

                )

        page.update()

    def nueva_semana(e):

        numero_input = ft.TextField(
            label="Número de semana"
        )

        inicio_input = ft.TextField(
            label="Fecha inicio lunes (dd/mm/aa)"
        )

        def guardar(ev):

            if numero_input.value.strip() == "":
                return

            if inicio_input.value.strip() == "":
                return

            agregar_semana(
                numero_input.value.strip(),
                inicio_input.value.strip()
            )

            dialog.open = False

            actualizar_semanas()

        def cancelar(ev):

            dialog.open = False

            page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("Nueva Semana"),

            content=ft.Column(
                controls=[
                    numero_input,
                    inicio_input,
                    ft.Text(
                        "La fecha de cierre se calculará automáticamente +6 días."
                    )
                ],
                tight=True
            ),

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

    actualizar_semanas()

    return ft.View(
        route="/semanas",

        controls=[

            ft.Text(
                "SEMANAS DE CAPTURA",
                size=28,
                weight=ft.FontWeight.BOLD
            ),

            ft.ElevatedButton(
                content=ft.Text("Nueva Semana"),
                on_click=nueva_semana
            ),

            ft.Divider(),

            lista_semanas

        ]
    )
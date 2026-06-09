import flet as ft

from database_manager import (
    listar_obras,
    buscar_obras
)


def obras_view(page):

    lista_view = ft.ListView(
        expand=True,
        spacing=10
    )

    def cargar_obras(obras):

        lista_view.controls.clear()

        for clave, nombre in obras:

            lista_view.controls.append(

                ft.Card(
                    content=ft.Container(
                        padding=15,

                        content=ft.Column(
                            controls=[

                                ft.Text(
                                    clave,
                                    size=18,
                                    weight=ft.FontWeight.BOLD
                                ),

                                ft.Text(
                                    nombre
                                ),

                                ft.ElevatedButton(
                                    content=ft.Text(
                                        "Abrir"
                                    )
                                )
                            ]
                        )
                    )
                )
            )

        page.update()

    def filtrar_obras(e):

        texto = e.control.value.strip()

        if texto == "":

            lista_view.controls.clear()

            lista_view.controls.append(

                ft.Text(
                    "Escriba una clave de obra."
                )

            )

            page.update()

            return

        resultados = buscar_obras(texto)

        cargar_obras(resultados)

    buscador = ft.TextField(
        label="Buscar obra por clave",
        width=400,
        on_change=filtrar_obras
    )

    lista_view.controls.append(

        ft.Text(
            "Escriba una clave de obra."
        )

    )

    return ft.View(
        route="/obras",

        controls=[

            ft.Text(
                "LISTADO DE OBRAS",
                size=28,
                weight=ft.FontWeight.BOLD
            ),

            buscador,

            ft.Divider(),

            lista_view

        ]
    )
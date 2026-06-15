import flet as ft

from database_manager import buscar_trabajador

def calcular_valor(texto):

    texto = texto.strip()

    if texto.startswith("="):
        texto = texto[1:]

    try:

        return float(
            eval(
                texto,
                {"__builtins__": {}},
                {}
            )
        )

    except:

        return None

def obra_view(page, clave_obra, nombre_obra):

    cuadrillas = []

    lista_cuadrillas = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=False
    )

    def actualizar_cuadrillas():

        lista_cuadrillas.controls.clear()

        if len(cuadrillas) == 0:

            lista_cuadrillas.controls.append(

                ft.Text(
                    "No hay cuadrillas capturadas"
                )

            )

        else:

            for cuadrilla in cuadrillas:

                trabajadores_controls = []

                for trabajador in cuadrilla["trabajadores"]:

                    trabajadores_controls.append(

                        ft.Text(
                            f"{trabajador['clave']} - "
                            f"{trabajador['nombre']} "
                            f"({trabajador['dias']} días)"
                        )

                    )

                lista_cuadrillas.controls.append(

                    ft.Card(

                        content=ft.Container(

                            padding=15,

                            content=ft.Column(

                                controls=[

                                    ft.Text(
                                        f"Cuadrilla {cuadrilla['numero']}",
                                        size=18,
                                        weight=ft.FontWeight.BOLD
                                    ),

                                    ft.Text(
                                        f"Tipo: {cuadrilla['tipo']}"
                                    ),

                                    ft.Text(
                                        f"Trabajadores: "
                                        f"{len(cuadrilla['trabajadores'])}"
                                    ),

                                    ft.ElevatedButton(
                                        content=ft.Text(
                                            "Agregar Trabajador"
                                        ),
                                        on_click=lambda e,
                                        c=cuadrilla:
                                        agregar_trabajador(c)
                                    )

                                ] + trabajadores_controls

                            )

                        )

                    )

                )

        page.update()

    def agregar_trabajador(cuadrilla):

        clave_input = ft.TextField(
            label="Número de nómina"
        )

        dias_input = ft.TextField(
            label="Días trabajados"
        )

        def guardar(ev):

            trabajador = buscar_trabajador(
                clave_input.value
            )

            if not trabajador:

                print(
                    "Trabajador no encontrado"
                )
                return

            dias = calcular_valor(
                dias_input.value
            )

            if dias is None:

                print(
                    "Fórmula inválida"
                )
                return

            cuadrilla["trabajadores"].append({

                "clave": trabajador[0],
                "nombre": trabajador[1],
                "puesto": trabajador[2],
                "salario_diario": float(
                    trabajador[3]
                ),
                "dias": dias

            })

            dialog.open = False

            actualizar_cuadrillas()

        def cancelar(ev):

            dialog.open = False

            page.update()

        dialog = ft.AlertDialog(

            title=ft.Text(
                "Agregar Trabajador"
            ),

            content=ft.Column(

                controls=[

                    clave_input,

                    dias_input

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

            if not tipo.value:
                return

            numero = len(cuadrillas) + 1

            cuadrillas.append({

                "numero": numero,
                "tipo": tipo.value,
                "trabajadores": [],
                "subtitulos": [],
                "conceptos": []

            })

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

    actualizar_cuadrillas()

    return ft.View(

        route="/obra",

        controls=[

            ft.Column(

                expand=True,

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

                    ft.Text(
                        "CUADRILLAS",
                        size=22,
                        weight=ft.FontWeight.BOLD
                    ),

                    ft.Container(
                        content=lista_cuadrillas,
                        expand=True
                    ),

                    ft.Divider(),

                    ft.Row(

                        controls=[

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

                ]

            )

        ]

    )
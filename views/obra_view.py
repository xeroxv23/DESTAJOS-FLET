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
    
def recalcular_cuadrilla(cuadrilla):

    total_puntos = 0

    for trabajador in cuadrilla["trabajadores"]:

        if trabajador["puesto"] == "OF":
            ponderacion = 60
        else:
            ponderacion = 40

        trabajador["ponderacion"] = ponderacion

        trabajador["puntos"] = (
            ponderacion *
            trabajador["dias"]
        )

        total_puntos += trabajador["puntos"]

    if total_puntos > 0:

        for trabajador in cuadrilla["trabajadores"]:

            trabajador["porcentaje"] = (

                trabajador["puntos"]
                /
                total_puntos

            ) * 100

    else:

        for trabajador in cuadrilla["trabajadores"]:

            trabajador["porcentaje"] = 0

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

                    trabajadores_controls.extend([

                        ft.Text(
                            f"{trabajador['clave']} - "
                            f"{trabajador['nombre']}"
                        ),

                        ft.Text(
                            f"Puesto: {trabajador['puesto']}"
                        ),

                        ft.Text(
                            f"Días: {trabajador['dias']:.2f}"
                        ),

                        ft.Text(
                            f"Puntos: {trabajador['puntos']:.2f}"
                        ),

                        ft.Text(
                            f"Participación: "
                            f"{trabajador['porcentaje']:.2f}%"
                        ),

                        ft.Divider()

                    ])
                
                for subtitulo in cuadrilla["subtitulos"]:

                    trabajadores_controls.extend([

                        ft.Text(
                            f"📁 {subtitulo['nombre']}",
                            size=16,
                            weight=ft.FontWeight.BOLD
                        ),

                        ft.ElevatedButton(
                            "Agregar Concepto",
                            on_click=lambda e,
                            s=subtitulo:
                            agregar_concepto(s)
                        )
                    ])
                
                for concepto in subtitulo["conceptos"]:

                    trabajadores_controls.append(

                        ft.Text(
                            f"• {concepto['clave']}"
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
                                    ),

                                    ft.ElevatedButton(
                                        content=ft.Text(
                                            "Agregar Subtítulo"
                                        ),
                                        on_click=lambda e,
                                        c=cuadrilla:
                                        agregar_subtitulo(c)
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
                "dias": dias,
                "ponderacion": 0,
                "puntos": 0,
                "porcentaje": 0

            })

            recalcular_cuadrilla(
                cuadrilla
            )

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

    def agregar_subtitulo(cuadrilla):

        nombre_input = ft.TextField(
            label="Nombre del subtítulo"
        )

        def guardar(ev):

            nombre = nombre_input.value.strip()

            if nombre == "":
                return

            cuadrilla["subtitulos"].append({

                "nombre": nombre,
                "conceptos": []

            })

            dialog.open = False

            actualizar_cuadrillas()

        def cancelar(ev):

            dialog.open = False

            page.update()

        dialog = ft.AlertDialog(

            title=ft.Text(
                "Nuevo Subtítulo"
            ),

            content=nombre_input,

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

    def agregar_concepto(subtitulo):

        clave_input = ft.TextField(
            label="Clave Concepto"
        )

        largo_input = ft.TextField(
            label="Largo"
        )

        ancho_input = ft.TextField(
            label="Ancho"
        )

        alto_input = ft.TextField(
            label="Alto"
        )

        piezas_input = ft.TextField(
            label="Piezas"
        )

        notas_input = ft.TextField(
            label="Notas",
            multiline=True
        )

        def guardar(ev):

            subtitulo["conceptos"].append({

                "clave": clave_input.value,
                "largo": largo_input.value,
                "ancho": ancho_input.value,
                "alto": alto_input.value,
                "piezas": piezas_input.value,
                "notas": notas_input.value

            })

            dialog.open = False

            actualizar_cuadrillas()

        def cancelar(ev):

            dialog.open = False

            page.update()

        dialog = ft.AlertDialog(

            title=ft.Text(
                "Nuevo Concepto"
            ),

            content=ft.Column(

                controls=[

                    clave_input,
                    largo_input,
                    ancho_input,
                    alto_input,
                    piezas_input,
                    notas_input

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
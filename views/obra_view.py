import flet as ft

from database_manager import (
    buscar_trabajador,
    buscar_concepto
)

from services.captura_service import (
    crear_cuadrilla,
    crear_trabajador,
    crear_subtitulo,
    crear_concepto
)

from services.cuadrilla_service import (
    calcular_valor,
    recalcular_cuadrilla
)

from components.cuadrilla_card import crear_cuadrilla_card

from components.dialogs import abrir_dialogo_nueva_cuadrilla
    
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
                            f"({trabajador['porcentaje']:.2f}%)"
                        )

                    )
                
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

                        nota = concepto.get("notas", "").strip()

                        if nota:
                            descripcion = nota
                        else:
                            descripcion = concepto.get("descripcion", "")

                        trabajadores_controls.append(

                            ft.Text(
                                f"{concepto['clave']} : {descripcion} | "
                                f"{concepto.get('largo', '')} | "
                                f"{concepto.get('ancho', '')} | "
                                f"{concepto.get('alto', '')} | "
                                f"{concepto.get('piezas', '')} | "
                                f"{descripcion}"
                            )

                        )
                              
                lista_cuadrillas.controls.append(
                    crear_cuadrilla_card(
                        cuadrilla,
                        agregar_trabajador,
                        agregar_subtitulo,
                        agregar_concepto
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

            cuadrilla["trabajadores"].append(
                crear_trabajador(
                    trabajador,
                    dias
                )
            )

            recalcular_cuadrilla(cuadrilla)

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

            cuadrilla["subtitulos"].append(
                crear_subtitulo(nombre)
            )

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

        concepto_info = ft.Text("")

        def consultar_concepto(e):

            concepto_bd = buscar_concepto(
                clave_input.value.strip()
            )

            if concepto_bd:
                concepto_info.value = (
                    f"{concepto_bd[1]} | Unidad: {concepto_bd[2]}"
                )
            else:
                concepto_info.value = "Concepto no encontrado"

            page.update()

        clave_input.on_change = consultar_concepto

        def guardar(ev):

            concepto_bd = buscar_concepto(
                clave_input.value.strip()
            )

            if not concepto_bd:
                print("Concepto no encontrado")
                return

            subtitulo["conceptos"].append(
                crear_concepto(
                    concepto_bd,
                    largo_input.value.strip(),
                    ancho_input.value.strip(),
                    alto_input.value.strip(),
                    piezas_input.value.strip(),
                    notas_input.value.strip()
                )
            )

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
                    concepto_info,
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

        abrir_dialogo_nueva_cuadrilla(
            page,
            cuadrillas,
            crear_cuadrilla,
            actualizar_cuadrillas
        )

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
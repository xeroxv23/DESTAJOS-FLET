import flet as ft


# !! ==========================================================
# !! CUADRILLA_CARD.PY
# !!
# !! Componente visual reutilizable.
# !!
# !! Responsabilidades:
# !! - Mostrar una cuadrilla completa.
# !! - Mostrar trabajadores.
# !! - Mostrar subtítulos.
# !! - Mostrar conceptos.
# !! - Mostrar botones de captura.
# !!
# !! Este módulo NO consulta SQLite.
# !! Este módulo NO calcula porcentajes.
# !!
# !! Solamente muestra información.
# !!
# !! ==========================================================


# !! ----------------------------------------------------------
# !! crear_cuadrilla_card()
# !!
# !! Construye visualmente una cuadrilla.
# !!
# !! Ejemplo:
# !!
# !! Cuadrilla 1
# !! Tipo: destajo
# !!
# !! 3950 Juan Perez (60%)
# !! 1990 Martin Guardado (40%)
# !!
# !! RECAMARA 01
# !! EXC01 | 2.00 | 0.50 | 0.40 | 1
# !!
# !! ----------------------------------------------------------
def crear_cuadrilla_card(
    cuadrilla,
    agregar_trabajador,
    agregar_subtitulo,
    agregar_concepto,
    eliminar_trabajador,
    eliminar_subtitulo,
    eliminar_concepto
):

    # ! Lista dinámica de controles visuales.
    controles = [

        # ! Número de cuadrilla
        ft.Text(
            f"Cuadrilla {cuadrilla['numero']}",
            size=18,
            weight=ft.FontWeight.BOLD
        ),

        # ! Tipo de cuadrilla
        ft.Text(
            f"Tipo: {cuadrilla['tipo']}"
        ),

        # ! Cantidad de trabajadores
        ft.Text(
            f"Trabajadores: {len(cuadrilla['trabajadores'])}"
        ),

        # ! Agregar trabajador
        ft.ElevatedButton(
            content=ft.Text(
                "Agregar Trabajador"
            ),
            on_click=lambda e:
            agregar_trabajador(cuadrilla)
        ),

        # ! Agregar subtítulo
        ft.ElevatedButton(
            content=ft.Text(
                "Agregar Subtítulo"
            ),
            on_click=lambda e:
            agregar_subtitulo(cuadrilla)
        ),

    ]

    # !! =======================================================
    # !! SECCIÓN TRABAJADORES
    # !! =======================================================
    for trabajador in cuadrilla["trabajadores"]:

        controles.append(

            ft.Row(
                controls=[

                    ft.Text(
                        f"{trabajador['clave']} - "
                        f"{trabajador['nombre']} "
                        f"({trabajador['porcentaje']:.2f}%)"
                    ),

                    ft.TextButton(
                        "Eliminar",
                        on_click=lambda e,
                        t=trabajador:
                        eliminar_trabajador(cuadrilla, t)
                    )

                ]
            )

        )

    # !! =======================================================
    # !! SECCIÓN SUBTÍTULOS
    # !! =======================================================
    
    for subtitulo in cuadrilla["subtitulos"]:

        controles.extend([

            ft.Divider(),

            ft.Row(

                controls=[

                    ft.Text(
                        f"📁 {subtitulo['nombre']}",
                        size=16,
                        weight=ft.FontWeight.BOLD
                    ),

                    ft.TextButton(
                        "Eliminar",
                        on_click=lambda e,
                        s=subtitulo:
                        eliminar_subtitulo(
                            cuadrilla,
                            s
                        )
                    )

                ]

            ),

            # ! Agregar concepto al subtítulo
            ft.ElevatedButton(
                content=ft.Text(
                    "Agregar Concepto"
                ),
                on_click=lambda e,
                s=subtitulo:
                agregar_concepto(s)
            )

        ])

        # !! ===================================================
        # !! SECCIÓN CONCEPTOS
        # !! ===================================================
        for concepto in subtitulo["conceptos"]:

            nota = concepto.get(
                "notas",
                ""
            ).strip()

            # ! Si existe nota
            # ! mostrar nota
            if nota:

                descripcion = nota

            # ! Si no existe nota
            # ! mostrar descripción BD
            else:

                descripcion = concepto.get(
                    "descripcion",
                    ""
                )

            controles.append(

                ft.Row(
                    controls=[

                        ft.Text(
                            f"{concepto['clave']} | "
                            f"{concepto.get('largo', '')} | "
                            f"{concepto.get('ancho', '')} | "
                            f"{concepto.get('alto', '')} | "
                            f"{concepto.get('piezas', '')} | "
                            f"{descripcion}",
                            expand=True
                        ),

                        ft.TextButton(
                            "Eliminar",
                            on_click=lambda e,
                            s=subtitulo,
                            c=concepto:
                            eliminar_concepto(s, c)
                        )

                    ]

                )

            )

    # !! =======================================================
    # !! TARJETA FINAL
    # !! =======================================================
    return ft.Card(

        content=ft.Container(

            padding=15,

            content=ft.Column(
                controls=controles
            )

        )

    )
import flet as ft

from styles import (
    COLOR_PRIMARY,
    COLOR_BACKGROUND,
    COLOR_SURFACE,
    COLOR_TEXT,
    COLOR_MUTED,
    COLOR_SUCCESS,
    COLOR_DANGER,
    COLOR_BORDER,
    CARD_RADIUS,
    CARD_PADDING,
    BUTTON_HEIGHT,
    SUBTITLE_SIZE,
    TEXT_SIZE,
    SMALL_TEXT_SIZE,
)


#region CUADRILLA_CARD.PY

def crear_cuadrilla_card(
    cuadrilla,
    agregar_trabajador,
    agregar_subtitulo,
    agregar_concepto,
    eliminar_trabajador,
    eliminar_subtitulo,
    eliminar_concepto,
    agregar_actividades
):

    controles = []

    # ======================================================
    # ENCABEZADO DE CUADRILLA
    # ======================================================

    controles.append(
        ft.Container(
            padding=16,
            bgcolor=COLOR_BACKGROUND,
            border_radius=CARD_RADIUS,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[

                    ft.Column(
                        spacing=4,
                        controls=[
                            ft.Text(
                                f"Cuadrilla {cuadrilla['numero']}",
                                size=SUBTITLE_SIZE,
                                weight=ft.FontWeight.BOLD,
                                color=COLOR_TEXT,
                            ),
                            ft.Text(
                                f"Tipo: {cuadrilla['tipo'].upper()}  |  "
                                f"Trabajadores: {len(cuadrilla['trabajadores'])}",
                                size=SMALL_TEXT_SIZE,
                                color=COLOR_MUTED,
                            ),
                        ],
                    ),

                    ft.Row(
                        spacing=8,
                        controls=[
                            ft.ElevatedButton(
                                height=BUTTON_HEIGHT,
                                bgcolor=COLOR_PRIMARY,
                                color="white",
                                content=ft.Text(
                                    "Agregar trabajador",
                                    size=SMALL_TEXT_SIZE,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                on_click=lambda e: agregar_trabajador(cuadrilla),
                            ),

                            ft.ElevatedButton(
                                height=BUTTON_HEIGHT,
                                bgcolor=COLOR_SURFACE,
                                color=COLOR_PRIMARY,
                                content=ft.Text(
                                    "Agregar subtítulo",
                                    size=SMALL_TEXT_SIZE,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                on_click=lambda e: agregar_subtitulo(cuadrilla),
                            ),
                        ],
                    ),
                ],
            ),
        )
    )

    # ======================================================
    # SECCIÓN TRABAJADORES
    # ======================================================

    controles.append(
        ft.Text(
            "Trabajadores",
            size=TEXT_SIZE,
            weight=ft.FontWeight.BOLD,
            color=COLOR_TEXT,
        )
    )

    if len(cuadrilla["trabajadores"]) == 0:

        controles.append(
            ft.Container(
                padding=12,
                bgcolor=COLOR_BACKGROUND,
                border_radius=CARD_RADIUS,
                content=ft.Text(
                    "Sin trabajadores agregados",
                    size=SMALL_TEXT_SIZE,
                    color=COLOR_MUTED,
                ),
            )
        )

    else:

        for trabajador in cuadrilla["trabajadores"]:

            if cuadrilla["tipo"] == "destajo":
                detalle = f"{trabajador['porcentaje']:.2f}%"
            else:
                detalle = f"{trabajador['dias']:.2f} días"

            controles.append(
                ft.Container(
                    padding=12,
                    bgcolor=COLOR_BACKGROUND,
                    border_radius=CARD_RADIUS,
                    border=ft.Border(
                        left=ft.BorderSide(1, COLOR_BORDER),
                        top=ft.BorderSide(1, COLOR_BORDER),
                        right=ft.BorderSide(1, COLOR_BORDER),
                        bottom=ft.BorderSide(1, COLOR_BORDER),
                    ),
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[

                            ft.Column(
                                spacing=2,
                                expand=True,
                                controls=[
                                    ft.Text(
                                        f"{trabajador['clave']} - {trabajador['nombre']}",
                                        size=TEXT_SIZE,
                                        weight=ft.FontWeight.BOLD,
                                        color=COLOR_TEXT,
                                    ),
                                    ft.Text(
                                        detalle,
                                        size=SMALL_TEXT_SIZE,
                                        color=COLOR_MUTED,
                                    ),
                                ],
                            ),

                            ft.TextButton(
                                content=ft.Text(
                                    "Eliminar",
                                    size=SMALL_TEXT_SIZE,
                                    color=COLOR_DANGER,
                                ),
                                on_click=lambda e, t=trabajador:
                                eliminar_trabajador(cuadrilla, t),
                            ),
                        ],
                    ),
                )
            )

    # ======================================================
    # ACTIVIDADES DE CUADRILLA POR DÍA
    # ======================================================

    actividades_cuadrilla = cuadrilla.get("actividades", "").strip()

    if cuadrilla["tipo"] == "dia" and actividades_cuadrilla:

        controles.extend([
            ft.Divider(),

            ft.Text(
                "Actividades generales",
                size=TEXT_SIZE,
                weight=ft.FontWeight.BOLD,
                color=COLOR_TEXT,
            ),

            ft.Container(
                padding=12,
                bgcolor=COLOR_BACKGROUND,
                border_radius=CARD_RADIUS,
                content=ft.Text(
                    actividades_cuadrilla,
                    size=TEXT_SIZE,
                    color=COLOR_TEXT,
                ),
            )
        ])

    # ======================================================
    # SECCIÓN SUBTÍTULOS
    # ======================================================

    controles.append(ft.Divider())

    controles.append(
        ft.Text(
            "Subtítulos / Actividades",
            size=TEXT_SIZE,
            weight=ft.FontWeight.BOLD,
            color=COLOR_TEXT,
        )
    )

    if len(cuadrilla["subtitulos"]) == 0:

        controles.append(
            ft.Container(
                padding=12,
                bgcolor=COLOR_BACKGROUND,
                border_radius=CARD_RADIUS,
                content=ft.Text(
                    "Sin subtítulos agregados",
                    size=SMALL_TEXT_SIZE,
                    color=COLOR_MUTED,
                ),
            )
        )

    for subtitulo in cuadrilla["subtitulos"]:

        controles.append(
            ft.Container(
                padding=14,
                bgcolor=COLOR_BACKGROUND,
                border_radius=CARD_RADIUS,
                border=ft.Border(
                    left=ft.BorderSide(1, COLOR_BORDER),
                    top=ft.BorderSide(1, COLOR_BORDER),
                    right=ft.BorderSide(1, COLOR_BORDER),
                    bottom=ft.BorderSide(1, COLOR_BORDER),
                ),

                content=ft.Column(
                    spacing=10,
                    controls=[

                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[

                                ft.Text(
                                    subtitulo["nombre"],
                                    size=TEXT_SIZE,
                                    weight=ft.FontWeight.BOLD,
                                    color=COLOR_TEXT,
                                    expand=True,
                                ),

                                ft.Row(
                                    spacing=4,
                                    controls=[
                                        ft.TextButton(
                                            content=ft.Text(
                                                "Eliminar",
                                                size=SMALL_TEXT_SIZE,
                                                color=COLOR_DANGER,
                                            ),
                                            on_click=lambda e, s=subtitulo:
                                            eliminar_subtitulo(cuadrilla, s),
                                        ),
                                    ],
                                ),
                            ],
                        ),

                        ft.ElevatedButton(
                            height=BUTTON_HEIGHT,
                            bgcolor=COLOR_PRIMARY,
                            color="white",
                            content=ft.Text(
                                "Agregar actividades"
                                if cuadrilla["tipo"] == "dia"
                                else "Agregar concepto",
                                size=SMALL_TEXT_SIZE,
                                weight=ft.FontWeight.BOLD,
                            ),
                            on_click=lambda e, s=subtitulo:
                            agregar_actividades(s)
                            if cuadrilla["tipo"] == "dia"
                            else agregar_concepto(s),
                        ),
                    ],
                ),
            )
        )

        # ==================================================
        # ACTIVIDADES POR DÍA DENTRO DEL SUBTÍTULO
        # ==================================================

        if cuadrilla["tipo"] == "dia":

            actividades = subtitulo.get(
                "actividades",
                ""
            ).strip()

            if actividades:

                controles.append(
                    ft.Container(
                        padding=12,
                        bgcolor=COLOR_SURFACE,
                        border_radius=CARD_RADIUS,
                        border=ft.Border(
                            left=ft.BorderSide(1, COLOR_BORDER),
                            top=ft.BorderSide(1, COLOR_BORDER),
                            right=ft.BorderSide(1, COLOR_BORDER),
                            bottom=ft.BorderSide(1, COLOR_BORDER),
                        ),
                        content=ft.Text(
                            actividades,
                            size=TEXT_SIZE,
                            color=COLOR_TEXT,
                        ),
                    )
                )

        # ==================================================
        # CONCEPTOS
        # ==================================================

        if cuadrilla["tipo"] != "dia":

            if len(subtitulo["conceptos"]) == 0:

                controles.append(
                    ft.Container(
                        padding=12,
                        bgcolor=COLOR_SURFACE,
                        border_radius=CARD_RADIUS,
                        content=ft.Text(
                            "Sin conceptos agregados",
                            size=SMALL_TEXT_SIZE,
                            color=COLOR_MUTED,
                        ),
                    )
                )

            for concepto in subtitulo["conceptos"]:

                nota = concepto.get("notas", "").strip()

                if nota:
                    descripcion = nota
                else:
                    descripcion = concepto.get("descripcion", "")

                controles.append(
                    ft.Container(
                        padding=12,
                        bgcolor=COLOR_SURFACE,
                        border_radius=CARD_RADIUS,
                        border=ft.Border(
                            left=ft.BorderSide(1, COLOR_BORDER),
                            top=ft.BorderSide(1, COLOR_BORDER),
                            right=ft.BorderSide(1, COLOR_BORDER),
                            bottom=ft.BorderSide(1, COLOR_BORDER),
                        ),

                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,

                            controls=[

                                ft.Column(
                                    spacing=4,
                                    expand=True,
                                    controls=[

                                        ft.Text(
                                            concepto["clave"],
                                            size=TEXT_SIZE,
                                            weight=ft.FontWeight.BOLD,
                                            color=COLOR_TEXT,
                                        ),

                                        ft.Text(
                                            descripcion,
                                            size=SMALL_TEXT_SIZE,
                                            color=COLOR_MUTED,
                                        ),

                                        ft.Text(
                                            f"Largo: {concepto.get('largo', '')}  |  "
                                            f"Ancho: {concepto.get('ancho', '')}  |  "
                                            f"Alto: {concepto.get('alto', '')}  |  "
                                            f"Piezas: {concepto.get('piezas', '')}",
                                            size=SMALL_TEXT_SIZE,
                                            color=COLOR_MUTED,
                                        ),
                                    ],
                                ),

                                ft.TextButton(
                                    content=ft.Text(
                                        "Eliminar",
                                        size=SMALL_TEXT_SIZE,
                                        color=COLOR_DANGER,
                                    ),
                                    on_click=lambda e, s=subtitulo, c=concepto:
                                    eliminar_concepto(s, c),
                                ),
                            ],
                        ),
                    )
                )

    # ======================================================
    # TARJETA FINAL
    # ======================================================

    return ft.Container(
        padding=CARD_PADDING,
        bgcolor=COLOR_SURFACE,
        border_radius=CARD_RADIUS,
        border=ft.Border(
            left=ft.BorderSide(1, COLOR_BORDER),
            top=ft.BorderSide(1, COLOR_BORDER),
            right=ft.BorderSide(1, COLOR_BORDER),
            bottom=ft.BorderSide(1, COLOR_BORDER),
        ),

        content=ft.Column(
            spacing=12,
            controls=controles,
        ),
    )

def crear_cuadrilla_resumen(
    cuadrilla,
    seleccionada=False,
    on_click=None,
):

    trabajadores = cuadrilla["trabajadores"]

    resumen_trabajadores = []

    for trabajador in trabajadores[:3]:

        if cuadrilla["tipo"] == "destajo":
            detalle = f"{trabajador['porcentaje']:.0f}%"
        else:
            detalle = f"{trabajador['dias']:.1f} días"

        resumen_trabajadores.append(
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Text(
                        f"{trabajador['clave']} - {trabajador['nombre']}",
                        size=SMALL_TEXT_SIZE,
                        color=COLOR_TEXT,
                        expand=True,
                    ),

                    ft.Text(
                        detalle,
                        size=SMALL_TEXT_SIZE,
                        color=COLOR_MUTED,
                    ),
                ],
            )
        )

    if len(trabajadores) > 3:

        resumen_trabajadores.append(
            ft.Text(
                f"+ {len(trabajadores) - 3} trabajadores más",
                size=SMALL_TEXT_SIZE,
                color=COLOR_MUTED,
            )
        )

    return ft.Container(
        padding=16,

        bgcolor=(
            COLOR_BACKGROUND
            if seleccionada
            else COLOR_SURFACE
        ),

        border_radius=CARD_RADIUS,

        border=ft.Border(
            left=ft.BorderSide(
                2 if seleccionada else 1,
                COLOR_PRIMARY if seleccionada else COLOR_BORDER,
            ),
            top=ft.BorderSide(
                2 if seleccionada else 1,
                COLOR_PRIMARY if seleccionada else COLOR_BORDER,
            ),
            right=ft.BorderSide(
                2 if seleccionada else 1,
                COLOR_PRIMARY if seleccionada else COLOR_BORDER,
            ),
            bottom=ft.BorderSide(
                2 if seleccionada else 1,
                COLOR_PRIMARY if seleccionada else COLOR_BORDER,
            ),
        ),

        ink=True,

        on_click=on_click,

        content=ft.Column(
            spacing=8,
            controls=[

                ft.Text(
                    f"Cuadrilla {cuadrilla['numero']}",
                    size=TEXT_SIZE,
                    weight=ft.FontWeight.BOLD,
                    color=COLOR_TEXT,
                ),

                ft.Text(
                    cuadrilla["tipo"].upper(),
                    size=SMALL_TEXT_SIZE,
                    color=COLOR_PRIMARY,
                ),

                *resumen_trabajadores,

                ft.Divider(),

                ft.Text(
                    (
                        f"{len(trabajadores)} trabajadores · "
                        f"{len(cuadrilla['subtitulos'])} subtítulos"
                    ),
                    size=SMALL_TEXT_SIZE,
                    color=COLOR_MUTED,
                ),
            ],
        ),
    )

#endregion
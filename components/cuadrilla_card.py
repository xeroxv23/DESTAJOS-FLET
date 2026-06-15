import flet as ft


def crear_cuadrilla_card(
    cuadrilla,
    agregar_trabajador,
    agregar_subtitulo,
    agregar_concepto
):

    controles = [

        ft.Text(
            f"Cuadrilla {cuadrilla['numero']}",
            size=18,
            weight=ft.FontWeight.BOLD
        ),

        ft.Text(
            f"Tipo: {cuadrilla['tipo']}"
        ),

        ft.Text(
            f"Trabajadores: {len(cuadrilla['trabajadores'])}"
        ),

        ft.ElevatedButton(
            content=ft.Text("Agregar Trabajador"),
            on_click=lambda e: agregar_trabajador(cuadrilla)
        ),

        ft.ElevatedButton(
            content=ft.Text("Agregar Subtítulo"),
            on_click=lambda e: agregar_subtitulo(cuadrilla)
        ),

    ]

    for trabajador in cuadrilla["trabajadores"]:

        controles.append(
            ft.Text(
                f"{trabajador['clave']} - "
                f"{trabajador['nombre']} "
                f"({trabajador['porcentaje']:.2f}%)"
            )
        )

    for subtitulo in cuadrilla["subtitulos"]:

        controles.extend([

            ft.Divider(),

            ft.Text(
                f"📁 {subtitulo['nombre']}",
                size=16,
                weight=ft.FontWeight.BOLD
            ),

            ft.ElevatedButton(
                content=ft.Text("Agregar Concepto"),
                on_click=lambda e, s=subtitulo: agregar_concepto(s)
            )

        ])

        for concepto in subtitulo["conceptos"]:

            nota = concepto.get("notas", "").strip()

            if nota:
                descripcion = nota
            else:
                descripcion = concepto.get("descripcion", "")

            controles.append(
                ft.Text(
                    f"{concepto['clave']} | "
                    f"{concepto.get('largo', '')} | "
                    f"{concepto.get('ancho', '')} | "
                    f"{concepto.get('alto', '')} | "
                    f"{concepto.get('piezas', '')} | "
                    f"{descripcion}"
                )
            )

    return ft.Card(
        content=ft.Container(
            padding=15,
            content=ft.Column(
                controls=controles
            )
        )
    )
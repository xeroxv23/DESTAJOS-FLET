import flet as ft

from services.persistencia_json import cargar_captura


def preview_view(page, semana_actual, clave_obra):

    captura = cargar_captura(
        semana_actual,
        clave_obra
    )

    contenido = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=False
    )

    def regresar(e):

        page.views.pop()
        page.update()

    if not captura:

        contenido.controls.append(
            ft.Text(
                "No existe captura para esta obra."
            )
        )

    else:

        contenido.controls.append(
            ft.Text(
                f"OBRA: {captura['clave_obra']}",
                size=24,
                weight=ft.FontWeight.BOLD
            )
        )

        contenido.controls.append(
            ft.Text(
                captura["nombre_obra"],
                size=18
            )
        )

        contenido.controls.append(
            ft.Text(
                f"Semana {semana_actual['numero']} "
                f"({semana_actual['fecha_inicio']} - {semana_actual['fecha_fin']})"
            )
        )

        contenido.controls.append(
            ft.Divider()
        )

        for cuadrilla in captura["cuadrillas"]:

            contenido.controls.append(
                ft.Text(
                    f"Cuadrilla {cuadrilla['numero']} - {cuadrilla['tipo']}",
                    size=20,
                    weight=ft.FontWeight.BOLD
                )
            )

            for trabajador in cuadrilla["trabajadores"]:

                if cuadrilla["tipo"] == "destajo":

                    texto_trabajador = (
                        f"{trabajador['clave']} - "
                        f"{trabajador['nombre']} "
                        f"({trabajador['porcentaje']:.2f}%)"
                    )

                else:

                    horas_extras = trabajador.get(
                        "horas_extras",
                        ""
                    )

                    if horas_extras:

                        texto_trabajador = (
                            f"{trabajador['clave']} - "
                            f"{trabajador['nombre']} "
                            f"({trabajador['dias']:.2f} días)"
                            f" / {float(horas_extras):.2f} Horas Extras"
                        )

                    else:

                        texto_trabajador = (
                            f"{trabajador['clave']} - "
                            f"{trabajador['nombre']} "
                            f"({trabajador['dias']:.2f} días)"
                        )

                contenido.controls.append(
                    ft.Text(
                        texto_trabajador
                    )
                )

            if cuadrilla["tipo"] == "dia":

                actividades = cuadrilla.get(
                    "actividades",
                    ""
                )

                if actividades:

                    contenido.controls.append(
                        ft.Text(
                            "ACTIVIDADES",
                            weight=ft.FontWeight.BOLD
                        )
                    )

                    contenido.controls.append(
                        ft.Text(
                            actividades
                        )
                    )

            for subtitulo in cuadrilla["subtitulos"]:

                contenido.controls.append(
                    ft.Text(
                        f"📁 {subtitulo['nombre']}",
                        size=18,
                        weight=ft.FontWeight.BOLD
                    )
                )

                for concepto in subtitulo["conceptos"]:

                    nota = concepto.get(
                        "notas",
                        ""
                    ).strip()

                    if nota:
                        descripcion = nota
                    else:
                        descripcion = concepto.get(
                            "descripcion",
                            ""
                        )

                    contenido.controls.append(
                        ft.Text(
                            f"{concepto['clave']} | "
                            f"{concepto.get('largo', '')} | "
                            f"{concepto.get('ancho', '')} | "
                            f"{concepto.get('alto', '')} | "
                            f"{concepto.get('piezas', '')} | "
                            f"{descripcion}"
                        )
                    )

            contenido.controls.append(
                ft.Divider()
            )

    return ft.View(
        route="/preview",

        controls=[

            ft.Text(
                "VISTA PREVIA DE CAPTURA",
                size=28,
                weight=ft.FontWeight.BOLD
            ),

            ft.ElevatedButton(
                content=ft.Text(
                    "Regresar"
                ),
                on_click=regresar
            ),

            ft.Divider(),

            contenido

        ]
    )
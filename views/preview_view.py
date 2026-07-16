import flet as ft

from services.persistencia_json import cargar_captura

from layouts import crear_work_layout

from styles import (
    COLOR_TEXT,
    COLOR_MUTED,
    SUBTITLE_SIZE,
    TEXT_SIZE,
)


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
                "No existe captura para esta obra.",
                size=TEXT_SIZE,
                color=COLOR_MUTED,
            )
        )

    else:

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

    return crear_work_layout(
        route="/preview",

        header_titulo="Vista previa de captura",
        header_subtitulo=(
            captura["nombre_obra"]
            if captura
            else clave_obra
        ),
        header_descripcion=(
            f"Semana {semana_actual['numero']} "
            f"({semana_actual['fecha_inicio']} - "
            f"{semana_actual['fecha_fin']})"
        ),
        header_detalle=(
            captura["clave_obra"]
            if captura
            else None
        ),

        texto_boton="Regresar",
        on_regresar=regresar,

        controls=[
            contenido,
        ],
    )
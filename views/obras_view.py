import flet as ft

from database_manager import (
    buscar_obras
)

from views.obra_view import obra_view


# !! ==========================================================
# !! OBRAS_VIEW.PY
# !!
# !! Segunda pantalla del sistema.
# !!
# !! Flujo:
# !!
# !! login_view.py
# !!       ↓
# !! obras_view.py
# !!       ↓
# !! obra_view.py
# !!
# !! Funciones principales:
# !! - Buscar obras por clave
# !! - Mostrar resultados encontrados
# !! - Permitir abrir una obra
# !!
# !! Esta pantalla NO captura destajos.
# !! Solamente permite seleccionar una obra.
# !!
# !! Las consultas se realizan mediante:
# !! database_manager.py
# !!
# !! La captura de cuadrillas se realiza en:
# !! obra_view.py
# !! ==========================================================


def obras_view(page, semana_actual):

    # ! Lista visual donde se mostrarán
    # ! las obras encontradas.
    lista_view = ft.ListView(
        expand=True,
        spacing=10
    )

    # !! ----------------------------------------------------------
    # !! cargar_obras()
    # !!
    # !! Recibe una lista de obras desde SQLite
    # !! y construye visualmente las tarjetas.
    # !!
    # !! Cada tarjeta contiene:
    # !! - Clave de obra
    # !! - Nombre de obra
    # !! - Botón Abrir
    # !!
    # !! Ejemplo:
    # !!
    # !! A-001
    # !! CASA HABITACION
    # !! [ Abrir ]
    # !! ----------------------------------------------------------
    def cargar_obras(obras):

        lista_view.controls.clear()

        for clave, nombre in obras:

            # !! --------------------------------------------------
            # !! abrir_obra()
            # !!
            # !! Abre la pantalla de captura de la obra.
            # !!
            # !! Envía:
            # !! - clave
            # !! - nombre
            # !!
            # !! a obra_view.py
            # !! --------------------------------------------------
            def abrir_obra(
                e,
                clave=clave,
                nombre=nombre
            ):

                page.views.append(

                    obra_view(
                        page,
                        clave,
                        nombre,
                        semana_actual
                    )

                )

                page.update()

            # ! Tarjeta visual de cada obra
            lista_view.controls.append(

                ft.Card(
                    content=ft.Container(
                        padding=15,

                        content=ft.Column(
                            controls=[

                                # ! Clave de obra
                                ft.Text(
                                    clave,
                                    size=18,
                                    weight=ft.FontWeight.BOLD
                                ),

                                # ! Nombre de obra
                                ft.Text(
                                    nombre
                                ),

                                # ! Abrir captura
                                ft.ElevatedButton(
                                    content=ft.Text(
                                        "Abrir"
                                    ),
                                    on_click=abrir_obra
                                )

                            ]
                        )
                    )
                )

            )

        page.update()

    # !! ----------------------------------------------------------
    # !! filtrar_obras()
    # !!
    # !! Se ejecuta cada vez que el usuario escribe.
    # !!
    # !! Busca coincidencias por:
    # !! clave_inter
    # !!
    # !! Ejemplos:
    # !!
    # !! A
    # !! A-001
    # !! ID-1211
    # !! ----------------------------------------------------------
    def filtrar_obras(e):

        texto = e.control.value.strip()

        # ! Si no hay texto
        # ! mostrar mensaje inicial
        if texto == "":

            lista_view.controls.clear()

            lista_view.controls.append(

                ft.Text(
                    "Escriba una clave de obra."
                )

            )

            page.update()

            return

        # ! Consulta a SQLite
        resultados = buscar_obras(texto)

        # ! Mostrar resultados
        cargar_obras(resultados)

    def regresar_semanas(e):

        page.views.pop()
        page.update()

    # !! ----------------------------------------------------------
    # !! Buscador principal
    # !!
    # !! Filtra en tiempo real conforme
    # !! el usuario escribe.
    # !! ----------------------------------------------------------

    buscador = ft.TextField(
        label="Buscar obra por clave",
        width=400,
        on_change=filtrar_obras
    )

    # ! Mensaje inicial antes de buscar
    lista_view.controls.append(

        ft.Text(
            "Escriba una clave de obra."
        )

    )

    # !! ==========================================================
    # !! RETURN DE LA VISTA
    # !!
    # !! Pantalla:
    # !!
    # !! LISTADO DE OBRAS
    # !!
    # !! [ Buscar obra ]
    # !!
    # !! Resultado 1
    # !! Resultado 2
    # !! Resultado 3
    # !!
    # !! ==========================================================
    return ft.View(
        route="/obras",

        controls=[

            ft.Text(
                "LISTADO DE OBRAS",
                size=28,
                weight=ft.FontWeight.BOLD
            ),

            ft.Text(
                f"Semana {semana_actual['numero']} "
                f"({semana_actual['fecha_inicio']} - {semana_actual['fecha_fin']})"
            ),

            ft.ElevatedButton(
                content=ft.Text("Regresar a Semanas"),
                on_click=regresar_semanas
            ),

            buscador,

            ft.Divider(),

            lista_view

        ]
    )
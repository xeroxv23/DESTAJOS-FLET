import flet as ft

from database_manager import (
    buscar_obras
)

from views.obra_view import obra_view

from services.persistencia_json import (
    obtener_claves_capturadas_semana,
    eliminar_captura_json
)

from views.preview_view import preview_view

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

    lista_capturadas = ft.Column(
        spacing=5
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

    def actualizar_obras_capturadas():

        lista_capturadas.controls.clear()

        claves_capturadas = obtener_claves_capturadas_semana(
            semana_actual
        )

        if len(claves_capturadas) == 0:

            lista_capturadas.controls.append(
                ft.Text(
                    "Sin obras capturadas"
                )
            )

        else:

            for clave_capturada in claves_capturadas:

                def abrir_capturada(
                    e,
                    clave=clave_capturada
                ):

                    # ! Buscamos la obra por clave para obtener también su nombre
                    resultado = buscar_obras(clave)

                    if len(resultado) == 0:
                        return

                    clave_obra, nombre_obra = resultado[0]

                    page.views.append(
                        obra_view(
                            page,
                            clave_obra,
                            nombre_obra,
                            semana_actual
                        )
                    )

                    page.update()

                def vista_previa(
                    e,
                    clave=clave_capturada
                ):

                    page.views.append(
                        preview_view(
                            page,
                            semana_actual,
                            clave
                        )
                    )

                    page.update()

                def eliminar_captura(
                    e,
                    clave=clave_capturada
                ):

                    eliminar_captura_json(
                        semana_actual,
                        clave
                    )

                    actualizar_obras_capturadas()

                    lista_view.controls.clear()

                    lista_view.controls.append(
                        ft.Text(
                            "Escriba una clave de obra."
                        )
                    )

                    page.update()

                lista_capturadas.controls.append(

                    ft.Row(
                        controls=[

                            ft.Container(
                                width=90,
                                content=ft.Text(
                                    clave_capturada,
                                    weight=ft.FontWeight.BOLD
                                )
                            ),

                            ft.TextButton(
                                "Abrir",
                                on_click=abrir_capturada
                            ),

                            ft.TextButton(
                                "Vista",
                                on_click=vista_previa
                            ),

                            ft.TextButton(
                                "Eliminar",
                                on_click=eliminar_captura
                            )
                        ]
                    )

                )

    def cargar_obras(obras):

        claves_capturadas = obtener_claves_capturadas_semana(
            semana_actual
        )

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
                                    size=15,
                                    weight=ft.FontWeight.BOLD
                                ),

                                # ! Nombre de obra
                                ft.Text(
                                    nombre
                                ),

                                ft.Text(
                                    "CAPTURADA"
                                    if clave in claves_capturadas
                                    else "SIN CAPTURA"
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

        texto = e.control.value.strip().upper()

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
        text_size=18,
        autofocus=True,
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

    actualizar_obras_capturadas()

    return ft.View(
        route="/obras",

        controls=[

            ft.Text(
                "LISTADO DE OBRAS",
                size=25,
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

            ft.Row(
                expand=True,
                controls=[

                    ft.Container(
                        content=lista_view,
                        width=850
                    ),

                    ft.Container(
                        width=420,
                        padding=10,
                        content=ft.Column(
                            controls=[

                                ft.Text(
                                    "OBRAS CAPTURADAS",
                                    size=15,
                                    weight=ft.FontWeight.BOLD
                                ),

                                lista_capturadas

                            ]
                        )
                    )

                ]
            )

        ]
    )
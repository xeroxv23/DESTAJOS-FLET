import flet as ft

from database_manager import (
    buscar_trabajador,
    buscar_concepto,
    obtener_obra
)

from services.cuadrilla_service import (
    calcular_valor,
    recalcular_cuadrilla
)

from services.captura_service import (
    crear_cuadrilla,
    crear_trabajador,
    crear_subtitulo,
    crear_concepto,
    obtener_siguiente_numero_cuadrilla
)

from components.cuadrilla_card import crear_cuadrilla_card

from components.dialogs import (
    abrir_dialogo_nueva_cuadrilla,
    abrir_dialogo_agregar_subtitulo,
    abrir_dialogo_agregar_trabajador,
    abrir_dialogo_agregar_concepto,
    abrir_dialogo_agregar_actividades
)


# !! ==========================================================
# !! OBRA_VIEW.PY
# !! Pantalla principal de captura de destajos por obra.
# !!
# !! Flujo general:
# !! Login -> Listado de Obras -> Obra Seleccionada
# !!
# !! Esta vista administra:
# !! - Cuadrillas
# !! - Trabajadores
# !! - Subtítulos
# !! - Conceptos
# !!
# !! Aquí NO se conecta directamente a SQLite.
# !! Las consultas se mandan a database_manager.py.
# !! La creación de estructuras se manda a captura_service.py.
# !! Los cálculos de cuadrilla se mandan a cuadrilla_service.py.
# !! La parte visual de cada cuadrilla se manda a cuadrilla_card.py.
# !! Los formularios emergentes se mandan a dialogs.py.
# !! ==========================================================


def obra_view(
        page, 
        clave_obra, 
        nombre_obra, 
        semana_actual
    ):

    # ! Lista temporal en memoria.
    # ! Aquí se guardan las cuadrillas capturadas mientras el usuario trabaja.
    # ! Más adelante esta información será la base para exportar a Excel.

    from services.estado_captura import (
        obtener_captura_obra,
        guardar_captura_obra
    )

    obra_bd = obtener_obra(
        clave_obra
    )

    direccion_obra = ""

    if obra_bd:
        direccion_obra = obra_bd[1]

    captura = obtener_captura_obra(
        semana_actual,
        clave_obra,
        nombre_obra,
        direccion_obra
    )

    cuadrillas = captura["cuadrillas"]

    # ! ListView permite scroll cuando hay muchas cuadrillas.
    lista_cuadrillas = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=False
    )

    # !! ----------------------------------------------------------
    # !! actualizar_cuadrillas()
    # !! Redibuja en pantalla todas las cuadrillas capturadas.
    # !!
    # !! Se ejecuta cada vez que:
    # !! - Se crea una nueva cuadrilla.
    # !! - Se agrega un trabajador.
    # !! - Se agrega un subtítulo.
    # !! - Se agrega un concepto.
    # !! ----------------------------------------------------------
    def actualizar_cuadrillas():

        lista_cuadrillas.controls.clear()

        if len(cuadrillas) == 0:

            lista_cuadrillas.controls.append(
                ft.Text("No hay cuadrillas capturadas")
            )

        else:

            for cuadrilla in cuadrillas:

                # ! La tarjeta visual de cada cuadrilla se construye en:
                # ! components/cuadrilla_card.py
                lista_cuadrillas.controls.append(
                    crear_cuadrilla_card(
                        cuadrilla,
                        agregar_trabajador,
                        agregar_subtitulo,
                        agregar_concepto,
                        eliminar_trabajador,
                        eliminar_subtitulo,
                        eliminar_concepto,
                        agregar_actividades
                    )
                )

        guardar_captura_obra(captura)
        
        page.update()

    # !! ----------------------------------------------------------
    # !! nueva_cuadrilla()
    # !! Abre el diálogo para crear una cuadrilla nueva.
    # !!
    # !! El diálogo pregunta:
    # !! - Por Día
    # !! - Destajo
    # !!
    # !! La estructura base se crea en:
    # !! services/captura_service.py
    # !! ----------------------------------------------------------

    def nueva_cuadrilla(e):

        abrir_dialogo_nueva_cuadrilla(
            page,
            cuadrillas,
            crear_cuadrilla,
            obtener_siguiente_numero_cuadrilla,
            actualizar_cuadrillas
        )

    # !! ----------------------------------------------------------
    # !! agregar_trabajador(cuadrilla)
    # !! Abre el diálogo para agregar un trabajador a una cuadrilla.
    # !!
    # !! Usa:
    # !! - buscar_trabajador() desde database_manager.py
    # !! - calcular_valor() para permitir fórmulas como =7/6*5
    # !! - crear_trabajador() para crear la estructura del trabajador
    # !! - recalcular_cuadrilla() para calcular porcentajes
    # !! ----------------------------------------------------------
    def agregar_trabajador(cuadrilla):

        abrir_dialogo_agregar_trabajador(
        page,
        cuadrillas,
        cuadrilla,
        buscar_trabajador,
        calcular_valor,
        crear_trabajador,
        recalcular_cuadrilla,
        obtener_siguiente_numero_cuadrilla,
        actualizar_cuadrillas
    )

    # !! ----------------------------------------------------------
    # !! agregar_subtitulo(cuadrilla)
    # !! Abre el diálogo para agregar un subtítulo dentro de una cuadrilla.
    # !!
    # !! Ejemplos:
    # !! - RECAMARA 01
    # !! - BAÑO PRINCIPAL
    # !! - COCINA
    # !! ----------------------------------------------------------
    def agregar_subtitulo(cuadrilla):

        abrir_dialogo_agregar_subtitulo(
            page,
            cuadrilla,
            crear_subtitulo,
            actualizar_cuadrillas
        )

    # !! ----------------------------------------------------------
    # !! agregar_concepto(subtitulo)
    # !! Abre el diálogo para agregar un concepto dentro de un subtítulo.
    # !!
    # !! Usa:
    # !! - buscar_concepto() para consultar la clave en SQLite
    # !! - crear_concepto() para guardar clave, medidas y notas
    # !!
    # !! Campos capturados:
    # !! - Clave
    # !! - Largo
    # !! - Ancho
    # !! - Alto
    # !! - Piezas
    # !! - Notas
    # !! ----------------------------------------------------------
    def agregar_concepto(subtitulo):

        abrir_dialogo_agregar_concepto(
            page,
            subtitulo,
            buscar_concepto,
            crear_concepto,
            actualizar_cuadrillas
        )

    def eliminar_trabajador(cuadrilla, trabajador):

        cuadrilla["trabajadores"].remove(trabajador)

        recalcular_cuadrilla(cuadrilla)

        actualizar_cuadrillas()


    def eliminar_subtitulo(cuadrilla, subtitulo):

        cuadrilla["subtitulos"].remove(subtitulo)

        actualizar_cuadrillas()


    def eliminar_concepto(subtitulo, concepto):

        subtitulo["conceptos"].remove(concepto)

        actualizar_cuadrillas()

    # !! ----------------------------------------------------------
    # !! regresar_obras()
    # !!
    # !! Regresa al listado de obras.
    # !!
    # !! No elimina información capturada.
    # !! Solamente vuelve a la vista anterior.
    # !!
    # !! ----------------------------------------------------------
    def regresar_obras(e):

        page.views.pop()

        page.update()

    def agregar_actividades(cuadrilla):

        abrir_dialogo_agregar_actividades(
            page,
            cuadrilla,
            actualizar_cuadrillas
        )

    # ! Primera carga visual de la lista.
    actualizar_cuadrillas()

    # !! ==========================================================
    # !! RETURN DE LA VISTA
    # !! Aquí se construye visualmente la pantalla Obra Seleccionada.
    # !! ==========================================================
    return ft.View(
        route="/obra",
        controls=[
            ft.Column(
                expand=True,
                controls=[

                    # ! Encabezado principal
                    ft.Text(
                        "OBRA SELECCIONADA",
                        size=28,
                        weight=ft.FontWeight.BOLD
                    ),

                    ft.Divider(),

                    # ! Información recibida desde obras_view.py
                    ft.Text(
                        f"Clave: {clave_obra}",
                        size=18
                    ),

                    ft.Text(
                        f"Obra: {nombre_obra}",
                        size=18
                    ),

                    ft.Text(
                        f"Semana: {semana_actual['numero']} "
                        f"({semana_actual['fecha_inicio']} - {semana_actual['fecha_fin']})",
                        size=16
                    ),

                    ft.Divider(),

                    # ! Sección principal de cuadrillas
                    ft.Text(
                        "CUADRILLAS",
                        size=22,
                        weight=ft.FontWeight.BOLD
                    ),

                    # ! Contenedor con scroll para muchas cuadrillas
                    ft.Container(
                        content=lista_cuadrillas,
                        expand=True
                    ),

                    ft.Divider(),

                    # ! Botones principales de la pantalla
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
                                    "Regresar a Obras"
                                ),
                                on_click=regresar_obras
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


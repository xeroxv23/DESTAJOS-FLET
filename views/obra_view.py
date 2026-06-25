import flet as ft
import os
import threading
import pythoncom

from database_manager import (
    buscar_trabajador,
    buscar_concepto,
    obtener_obra
)

#IMPORTE DE SERVICES
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

# IMPORTES DE COMPONENTES
from components.cuadrilla_card import crear_cuadrilla_card

from components.dialogs import (
    abrir_dialogo_nueva_cuadrilla,
    abrir_dialogo_agregar_subtitulo,
    abrir_dialogo_agregar_trabajador,
    abrir_dialogo_agregar_concepto,
    abrir_dialogo_agregar_actividades
)

from components.app_actions import crear_app_actions

from export.excel_exporter import exportar_destajo

from views.evidencias_view import evidencias_view

from styles import (
    COLOR_PRIMARY,
    COLOR_PRIMARY_DARK,
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
    TITLE_SIZE,
    SUBTITLE_SIZE,
    TEXT_SIZE,
    SMALL_TEXT_SIZE,
    PAGE_PADDING,
)


#region OBRA_VIEW.PY

def obra_view(page, clave_obra, nombre_obra, semana_actual):

    from services.estado_captura import (
        obtener_captura_obra,
        guardar_captura_obra
    )

    obra_bd = obtener_obra(clave_obra)

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

    lista_cuadrillas = ft.ListView(
        expand=True,
        spacing=12,
        auto_scroll=False,
        padding=0,
    )

    def mensaje_sin_cuadrillas():

        return ft.Container(
            padding=24,
            bgcolor=COLOR_BACKGROUND,
            border_radius=CARD_RADIUS,
            border=ft.Border(
                left=ft.BorderSide(1, COLOR_BORDER),
                top=ft.BorderSide(1, COLOR_BORDER),
                right=ft.BorderSide(1, COLOR_BORDER),
                bottom=ft.BorderSide(1, COLOR_BORDER),
            ),
            content=ft.Column(
                spacing=8,
                controls=[
                    ft.Text(
                        "No hay cuadrillas capturadas",
                        size=SUBTITLE_SIZE,
                        weight=ft.FontWeight.BOLD,
                        color=COLOR_TEXT,
                    ),
                    ft.Text(
                        "Agrega una nueva cuadrilla para comenzar la captura de destajos.",
                        size=TEXT_SIZE,
                        color=COLOR_MUTED,
                    ),
                ],
            ),
        )

    def actualizar_cuadrillas():

        lista_cuadrillas.controls.clear()

        if len(cuadrillas) == 0:

            lista_cuadrillas.controls.append(
                mensaje_sin_cuadrillas()
            )

        else:

            for cuadrilla in cuadrillas:

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

    def nueva_cuadrilla(e):

        abrir_dialogo_nueva_cuadrilla(
            page,
            cuadrillas,
            crear_cuadrilla,
            obtener_siguiente_numero_cuadrilla,
            actualizar_cuadrillas
        )

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

    def agregar_subtitulo(cuadrilla):

        abrir_dialogo_agregar_subtitulo(
            page,
            cuadrilla,
            crear_subtitulo,
            actualizar_cuadrillas
        )

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

    def regresar_obras(e):

        page.views.pop()
        page.update()
    
    def abrir_evidencias(e):

        page.views.append(
            evidencias_view(
                page,
                semana_actual,
                clave_obra,
                nombre_obra
            )
        )

        page.update()

    def cerrar_destajo(e):

        try:

            guardar_captura_obra(captura)

            residentes = []

            def exportar_con_residentes():

                def hay_trabajadores_capturados():

                    for cuadrilla in captura["cuadrillas"]:

                        if len(cuadrilla["trabajadores"]) > 0:
                            return True

                    return False

                if not hay_trabajadores_capturados():

                    porcentaje_maestreada = None

                    ruta = exportar_destajo(
                        captura,
                        residentes,
                        porcentaje_maestreada
                    )

                    nombre_archivo = os.path.basename(ruta)

                    dialog_resultado = ft.AlertDialog(
                        title=ft.Text("Destajo exportado"),
                        content=ft.Text(nombre_archivo),
                        actions=[
                            ft.TextButton(
                                "Aceptar",
                                on_click=lambda ev: cerrar_resultado(ev)
                            )
                        ]
                    )

                    def cerrar_resultado(ev):

                        dialog_resultado.open = False
                        page.update()

                    page.overlay.append(dialog_resultado)
                    dialog_resultado.open = True
                    page.update()

                    return

                porcentaje_input = ft.TextField(
                    label="Porcentaje de maestreada"
                )

                def exportar_final(ev):

                    porcentaje_maestreada = calcular_valor(
                        porcentaje_input.value
                    )

                    if porcentaje_maestreada is None:
                        print("Porcentaje de maestreada inválido")
                        return

                    dialog_maestreada.open = False
                    page.update()

                    dialog_cargando = ft.AlertDialog(
                        modal=True,
                        title=ft.Text("Generando archivo"),
                        content=ft.Column(
                            controls=[
                                ft.ProgressRing(),
                                ft.Text("Creando archivo Excel, por favor espere...")
                            ],
                            tight=True
                        )
                    )

                    page.overlay.append(dialog_cargando)
                    dialog_cargando.open = True
                    page.update()

                    def proceso_exportacion():

                        pythoncom.CoInitialize()

                        try:

                            ruta = exportar_destajo(
                                captura,
                                residentes,
                                porcentaje_maestreada
                            )

                            nombre_archivo = os.path.basename(ruta)

                            dialog_cargando.open = False

                            dialog_resultado = ft.AlertDialog(
                                title=ft.Text("Destajo exportado"),
                                content=ft.Text(nombre_archivo),
                                actions=[
                                    ft.TextButton(
                                        "Aceptar",
                                        on_click=lambda ev: cerrar_resultado(ev)
                                    )
                                ]
                            )

                            def cerrar_resultado(ev):

                                dialog_resultado.open = False
                                page.update()

                            page.overlay.append(dialog_resultado)
                            dialog_resultado.open = True
                            page.update()

                        except Exception as error:

                            dialog_cargando.open = False

                            dialog_error = ft.AlertDialog(
                                title=ft.Text("Error al exportar"),
                                content=ft.Text(str(error)),
                                actions=[
                                    ft.TextButton(
                                        "Aceptar",
                                        on_click=lambda ev: cerrar_error(ev)
                                    )
                                ]
                            )

                            def cerrar_error(ev):

                                dialog_error.open = False
                                page.update()

                            page.overlay.append(dialog_error)
                            dialog_error.open = True
                            page.update()

                        finally:

                            pythoncom.CoUninitialize()

                    threading.Thread(
                        target=proceso_exportacion,
                        daemon=True
                    ).start()

                def cancelar(ev):

                    dialog_maestreada.open = False
                    page.update()

                dialog_maestreada = ft.AlertDialog(
                    title=ft.Text("Maestreada"),
                    content=ft.Column(
                        controls=[
                            ft.Text("Ingresa el porcentaje de maestreada de esta obra."),
                            porcentaje_input
                        ],
                        tight=True
                    ),
                    actions=[
                        ft.TextButton("Cancelar", on_click=cancelar),
                        ft.TextButton("Exportar", on_click=exportar_final)
                    ]
                )

                page.overlay.append(dialog_maestreada)
                dialog_maestreada.open = True
                page.update()

            def no_capturar_residente(ev):

                dialog_residente.open = False
                page.update()
                exportar_con_residentes()

            def capturar_residente(ev):

                dialog_residente.open = False
                page.update()

                clave_input = ft.TextField(label="Número de nómina")
                dias_input = ft.TextField(label="Días trabajados")
                horas_extras_input = ft.TextField(label="Horas extras")

                actividades_input = ft.TextField(
                    label="Actividades del residente",
                    multiline=True
                )

                descripcion_horas_extras_input = ft.TextField(
                    label="Descripción horas extras",
                    multiline=True
                )

                def guardar_residente(ev_guardar):

                    trabajador_bd = buscar_trabajador(
                        clave_input.value.strip()
                    )

                    if not trabajador_bd:
                        print("Residente no encontrado")
                        return

                    dias = calcular_valor(
                        dias_input.value
                    )

                    if dias is None:
                        print("Días inválidos")
                        return

                    residentes.append({
                        "clave": trabajador_bd[0],
                        "nombre": trabajador_bd[1],
                        "puesto": trabajador_bd[2],
                        "salario_diario": float(trabajador_bd[3]),
                        "dias": dias,
                        "horas_extras": horas_extras_input.value.strip(),
                        "descripcion_horas_extras": descripcion_horas_extras_input.value.strip(),
                        "actividades": actividades_input.value.strip(),
                        "ponderacion": 0,
                        "puntos": 0,
                        "porcentaje": 100
                    })

                    dialog_captura.open = False
                    page.update()

                    preguntar_otro_residente()

                def cancelar_residente(ev_cancelar):

                    dialog_captura.open = False
                    page.update()

                    preguntar_otro_residente()

                dialog_captura = ft.AlertDialog(
                    title=ft.Text("Capturar Residente"),
                    content=ft.Column(
                        controls=[
                            clave_input,
                            dias_input,
                            horas_extras_input,
                            descripcion_horas_extras_input,
                            actividades_input
                        ],
                        tight=True
                    ),
                    actions=[
                        ft.TextButton(
                            "Cancelar",
                            on_click=cancelar_residente
                        ),
                        ft.TextButton(
                            "Guardar",
                            on_click=guardar_residente
                        )
                    ]
                )

                page.overlay.append(dialog_captura)
                dialog_captura.open = True
                page.update()

            def preguntar_otro_residente():

                def si_otro(ev):

                    dialog_otro.open = False
                    page.update()

                    capturar_residente(ev)

                def no_otro(ev):

                    dialog_otro.open = False
                    page.update()

                    exportar_con_residentes()

                dialog_otro = ft.AlertDialog(
                    title=ft.Text("Captura de Residente"),
                    content=ft.Text("¿Desea capturar otro residente?"),
                    actions=[
                        ft.TextButton(
                            "No",
                            on_click=no_otro
                        ),
                        ft.TextButton(
                            "Sí",
                            on_click=si_otro
                        )
                    ]
                )

                page.overlay.append(dialog_otro)
                dialog_otro.open = True
                page.update()

            dialog_residente = ft.AlertDialog(
                title=ft.Text("Captura de Residente"),
                content=ft.Text("¿Desea capturar residente?"),
                actions=[
                    ft.TextButton(
                        "No",
                        on_click=no_capturar_residente
                    ),
                    ft.TextButton(
                        "Sí",
                        on_click=lambda ev: capturar_residente(ev)
                    )
                ]
            )

            page.overlay.append(dialog_residente)
            dialog_residente.open = True
            page.update()

            return

        except Exception as error:

            dialog = ft.AlertDialog(
                title=ft.Text("Error al exportar"),
                content=ft.Text(str(error)),
                actions=[
                    ft.TextButton(
                        "Aceptar",
                        on_click=lambda ev: cerrar_error(ev)
                    )
                ]
            )

            def cerrar_error(ev):

                dialog.open = False
                page.update()

            page.overlay.append(dialog)
            dialog.open = True
            page.update()

    def agregar_actividades(subtitulo):

        abrir_dialogo_agregar_actividades(
            page,
            subtitulo,
            actualizar_cuadrillas
        )


    actualizar_cuadrillas()

    return ft.View(
        route="/obra",
        bgcolor=COLOR_BACKGROUND,
        padding=PAGE_PADDING,

        controls=[

            ft.Column(
                expand=True,
                spacing=16,

                controls=[

                    ft.Container(
                        padding=20,
                        bgcolor=COLOR_PRIMARY_DARK,
                        border_radius=CARD_RADIUS,

                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,

                            controls=[

                                ft.Column(
                                    spacing=5,
                                    expand=True,
                                    controls=[

                                        ft.Text(
                                            clave_obra,
                                            size=TITLE_SIZE,
                                            weight=ft.FontWeight.BOLD,
                                            color="white",
                                        ),

                                        ft.Text(
                                            nombre_obra,
                                            size=TEXT_SIZE,
                                            color="white",
                                        ),

                                        ft.Text(
                                            f"Semana {semana_actual['numero']} "
                                            f"({semana_actual['fecha_inicio']} - {semana_actual['fecha_fin']})",
                                            size=SMALL_TEXT_SIZE,
                                            color="#E5E7EB",
                                        ),

                                        ft.Text(
                                            direccion_obra,
                                            size=SMALL_TEXT_SIZE,
                                            color="#E5E7EB",
                                        ),
                                    ],
                                ),

                                ft.ElevatedButton(
                                    height=BUTTON_HEIGHT,
                                    bgcolor=COLOR_SURFACE,
                                    color=COLOR_PRIMARY_DARK,
                                    content=ft.Text(
                                        "Regresar a obras",
                                        size=TEXT_SIZE,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                    on_click=regresar_obras,
                                ),
                            ],
                        ),
                    ),

                    crear_app_actions(
                        titulo="Gestión de captura",
                        descripcion="Agrega cuadrillas, evidencias fotográficas o cierra el destajo.",
                        acciones=[
                            {
                                "texto": "Nueva cuadrilla",
                                "on_click": nueva_cuadrilla,
                                "tipo": "primary",
                            },
                            {
                                "texto": "Tomar fotografía",
                                "on_click": abrir_evidencias,
                                "tipo": "primary",
                            },
                            {
                                "texto": "Cerrar destajo",
                                "on_click": cerrar_destajo,
                                "tipo": "success",
                            },
                        ],
                    ),

                    ft.Container(
                        expand=True,
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
                            expand=True,
                            spacing=12,

                            controls=[

                                ft.Row(
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    controls=[

                                        ft.Text(
                                            "Cuadrillas capturadas",
                                            size=SUBTITLE_SIZE,
                                            weight=ft.FontWeight.BOLD,
                                            color=COLOR_TEXT,
                                        ),

                                        ft.Text(
                                            f"Total: {len(cuadrillas)}",
                                            size=SMALL_TEXT_SIZE,
                                            color=COLOR_MUTED,
                                        ),
                                    ],
                                ),

                                lista_cuadrillas,
                            ],
                        ),
                    ),
                ],
            )
        ],
    )

#endregion
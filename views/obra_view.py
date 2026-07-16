import flet as ft
import os
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

from components import (
    crear_app_actions,
    crear_app_loading_dialog,
    crear_app_dialog,
    crear_app_numberfield,
    crear_app_multiline,
    abrir_app_confirm,
)

from components.app_confirm import abrir_app_confirm

from export.excel_exporter import exportar_destajo

from views.evidencias_view import evidencias_view

from styles import (
    COLOR_BACKGROUND,
    COLOR_SURFACE,
    COLOR_TEXT,
    COLOR_MUTED,
    COLOR_SUCCESS,
    COLOR_DANGER,
    COLOR_BORDER,
    CARD_RADIUS,
    CARD_PADDING,
    SUBTITLE_SIZE,
    TEXT_SIZE,
    SMALL_TEXT_SIZE,
)

from layouts import (
    crear_work_layout,
    crear_master_detail_layout,
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

    cuadrilla_seleccionada = {
        "data": (
            cuadrillas[0]
            if len(cuadrillas) > 0
            else None
        )
    }

    lista_cuadrillas = ft.ListView(
        expand=True,
        spacing=12,
        auto_scroll=False,
        padding=0,
    )

    detalle_cuadrilla = ft.Column(
        expand=True,
        spacing=12,
        controls=[
            ft.Text(
                "Selecciona una cuadrilla",
                size=SUBTITLE_SIZE,
                weight=ft.FontWeight.BOLD,
                color=COLOR_TEXT,
            ),

            ft.Text(
                (
                    "Elige una cuadrilla del panel izquierdo para "
                    "consultar sus actividades, subtítulos y conceptos."
                ),
                size=TEXT_SIZE,
                color=COLOR_MUTED,
            ),
        ],
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
        
        if (
            cuadrilla_seleccionada["data"]
            not in cuadrillas
        ):
            cuadrilla_seleccionada["data"] = (
                cuadrillas[0]
                if len(cuadrillas) > 0
                else None
            )

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

    def eliminar_cuadrilla(cuadrilla):

        def confirmar_eliminacion():

            if cuadrilla not in cuadrillas:
                return

            indice = cuadrillas.index(cuadrilla)

            cuadrillas.remove(cuadrilla)

            if len(cuadrillas) == 0:

                cuadrilla_seleccionada["data"] = None

            else:

                nuevo_indice = min(
                    indice,
                    len(cuadrillas) - 1,
                )

                cuadrilla_seleccionada["data"] = (
                    cuadrillas[nuevo_indice]
                )

            actualizar_cuadrillas()

        abrir_app_confirm(
            page=page,
            titulo="Eliminar cuadrilla",
            mensaje=(
                f"¿Deseas eliminar la cuadrilla "
                f"{cuadrilla['numero']}? "
                "También se eliminarán sus trabajadores, "
                "actividades, subtítulos y conceptos."
            ),
            on_confirmar=confirmar_eliminacion,
            texto_confirmar="Eliminar",
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

                porcentaje_input = crear_app_numberfield(
                    label="Porcentaje de mandos intermedios",
                )

                def exportar_final(ev):

                    porcentaje_maestreada = calcular_valor(
                        porcentaje_input.value
                    )

                    if porcentaje_maestreada is None:
                        print("Porcentaje de mandos intermedios inválido")
                        return

                    dialog_maestreada.open = False
                    page.update()

                    dialog_cargando = crear_app_loading_dialog(
                        titulo="Generando archivo",
                        mensaje="Creando archivo Excel, por favor espere..."
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


                    page.run_thread(proceso_exportacion)

                def cancelar(ev):

                    dialog_maestreada.open = False
                    page.update()

                dialog_maestreada = crear_app_dialog(
                    titulo="Mandos intermedios",
                    descripcion="Ingresa el porcentaje de mandos intermedios de esta obra.",
                    contenido=[
                        porcentaje_input,

                        ft.Text(
                            "Mantto-7, Residencial-10 y 5 C/R , Industrial-12",
                            size=SMALL_TEXT_SIZE,
                            color=COLOR_MUTED,
                        )
                    ],
                    on_cancelar=cancelar,
                    on_guardar=exportar_final,
                    texto_guardar="Exportar",
                    width=420,
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

                mensaje_residente = ft.Text(
                    "",
                    size=SMALL_TEXT_SIZE,
                    color=COLOR_DANGER,
                )

                info_residente = ft.Text(
                    "Escribe un número de nómina.",
                    size=SMALL_TEXT_SIZE,
                    color=COLOR_MUTED,
                )

                info_dias_residente = ft.Text(
                    "",
                    size=SMALL_TEXT_SIZE,
                    color=COLOR_MUTED,
                )

                residente_encontrado = {
                    "data": None
                }

                def validar_residente(e):

                    clave = clave_input.value.strip()

                    if clave == "":
                        residente_encontrado["data"] = None
                        info_residente.value = "Escribe un número de nómina."
                        info_residente.color = COLOR_MUTED
                        page.update()
                        return

                    trabajador_bd = buscar_trabajador(clave)

                    if trabajador_bd:
                        residente_encontrado["data"] = trabajador_bd
                        info_residente.value = f"{trabajador_bd[1]} | {trabajador_bd[2]}"
                        info_residente.color = COLOR_SUCCESS
                    else:
                        residente_encontrado["data"] = None
                        info_residente.value = "Residente no encontrado"
                        info_residente.color = COLOR_DANGER

                    page.update()

                def validar_dias_residente(e):

                    if dias_input.value.strip() == "":
                        info_dias_residente.value = ""
                        page.update()
                        return

                    dias = calcular_valor(
                        dias_input.value
                    )

                    if dias is None:
                        info_dias_residente.value = "Fórmula inválida"
                        info_dias_residente.color = COLOR_DANGER
                    else:
                        info_dias_residente.value = f"Resultado: {dias:.2f} días"
                        info_dias_residente.color = COLOR_SUCCESS

                    page.update()

                clave_input = crear_app_numberfield(
                    label="Número de nómina",
                    autofocus=True,
                    on_change=validar_residente,
                )

                dias_input = crear_app_numberfield(
                    label="Días trabajados",
                    on_change=validar_dias_residente,
                )

                horas_extras_input = crear_app_numberfield(
                    label="Horas extras",
                )

                descripcion_horas_extras_input = crear_app_multiline(
                    label="Descripción horas extras",
                )

                actividades_input = crear_app_multiline(
                    label="Actividades del residente",
                )

                def guardar_residente(ev_guardar):

                    trabajador_bd = residente_encontrado["data"]

                    if trabajador_bd is None:
                        trabajador_bd = buscar_trabajador(
                            clave_input.value.strip()
                        )

                    if not trabajador_bd:
                        mensaje_residente.value = "Residente no encontrado"
                        page.update()
                        return

                    dias = calcular_valor(
                        dias_input.value
                    )

                    if dias is None:
                        mensaje_residente.value = "Días inválidos"
                        page.update()
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

                dialog_captura = crear_app_dialog(
                    titulo="Capturar residente",
                    descripcion="Captura los datos del residente para incluirlo en la exportación.",
                    contenido=[
                        clave_input,
                        info_residente,
                        dias_input,
                        info_dias_residente,
                        horas_extras_input,
                        descripcion_horas_extras_input,
                        actividades_input,
                        mensaje_residente,
                    ],
                    on_cancelar=cancelar_residente,
                    on_guardar=guardar_residente,
                    width=520,
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

                dialog_otro = crear_app_dialog(
                    titulo="Captura de residente",
                    descripcion="¿Deseas capturar otro residente?",
                    contenido=[],
                    on_cancelar=no_otro,
                    on_guardar=si_otro,
                    texto_cancelar="No",
                    texto_guardar="Sí",
                    width=420,
                )

                page.overlay.append(dialog_otro)
                dialog_otro.open = True
                page.update()

            dialog_residente = crear_app_dialog(
                titulo="Captura de residente",
                descripcion="¿Deseas capturar residente para este destajo?",
                contenido=[],
                on_cancelar=no_capturar_residente,
                on_guardar=lambda ev: capturar_residente(ev),
                texto_cancelar="No",
                texto_guardar="Sí",
                width=420,
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

    return crear_work_layout(
        route="/obra",

        header_titulo=clave_obra,
        header_subtitulo=nombre_obra,
        header_descripcion=(
            f"Semana {semana_actual['numero']} "
            f"({semana_actual['fecha_inicio']} - "
            f"{semana_actual['fecha_fin']})"
        ),
        header_detalle=direccion_obra,

        texto_boton="Regresar a obras",
        on_regresar=regresar_obras,

        controls=[
            crear_app_actions(
                titulo="Gestión de captura",
                descripcion=(
                    "Agrega cuadrillas, evidencias fotográficas "
                    "o cierra el destajo."
                ),
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

            crear_master_detail_layout(
                master=ft.Container(
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
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
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

                detail=ft.Container(
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
                    content=detalle_cuadrilla,
                ),

                master_width=420,
                spacing=16,
            ),
        ],
    )

#endregion
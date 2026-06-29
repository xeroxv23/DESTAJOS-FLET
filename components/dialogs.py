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
    BUTTON_HEIGHT,
    SUBTITLE_SIZE,
    TEXT_SIZE,
    SMALL_TEXT_SIZE,
)


#COMPONENTS
from components.app_dialog import crear_app_dialog
from components.app_form import (
    crear_app_textfield,
    crear_app_numberfield,
    crear_app_multiline
)

#region DIALOGS.PY

def campo_texto(label, multiline=False, value=""):
    return ft.TextField(
        label=label,
        value=value,
        multiline=multiline,
        height=90 if multiline else 56,
        border_color=COLOR_BORDER,
        focused_border_color=COLOR_PRIMARY,
        text_size=TEXT_SIZE,
    )


def texto_error():
    return ft.Text(
        "",
        color=COLOR_DANGER,
        size=SMALL_TEXT_SIZE,
    )


def abrir_dialogo_nueva_cuadrilla(
    page,
    cuadrillas,
    crear_cuadrilla,
    obtener_siguiente_numero_cuadrilla,
    actualizar_cuadrillas
):

    mensaje = texto_error()

    tipo = ft.RadioGroup(
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Radio(value="dia", label="Por día"),
                ft.Radio(value="destajo", label="Destajo"),
            ],
        )
    )

    def guardar(ev):

        if not tipo.value:
            mensaje.value = "Selecciona el tipo de cuadrilla"
            page.update()
            return

        if tipo.value == "destajo":
            numero = obtener_siguiente_numero_cuadrilla(cuadrillas)
        else:
            numero = None

        cuadrillas.append(
            crear_cuadrilla(numero, tipo.value)
        )

        dialog.open = False
        actualizar_cuadrillas()

    def cancelar(ev):
        dialog.open = False
        page.update()

    dialog = ft.AlertDialog(
        modal=True,

        title=ft.Text(
            "Nueva cuadrilla",
            size=SUBTITLE_SIZE,
            weight=ft.FontWeight.BOLD,
            color=COLOR_TEXT,
        ),

        content=ft.Container(
            width=380,
            content=ft.Column(
                spacing=14,
                tight=True,
                controls=[
                    ft.Text(
                        "Selecciona cómo se capturará el trabajo.",
                        size=TEXT_SIZE,
                        color=COLOR_MUTED,
                    ),
                    tipo,
                    mensaje,
                ],
            ),
        ),

        actions=[
            ft.TextButton(
                "Cancelar",
                on_click=cancelar,
            ),
            ft.ElevatedButton(
                height=BUTTON_HEIGHT,
                bgcolor=COLOR_PRIMARY,
                color="white",
                content=ft.Text("Guardar"),
                on_click=guardar,
            ),
        ],
    )

    page.overlay.append(dialog)
    dialog.open = True
    page.update()


def abrir_dialogo_agregar_subtitulo(
    page,
    cuadrilla,
    crear_subtitulo,
    actualizar_cuadrillas
):

    mensaje = texto_error()

    nombre_input = campo_texto(
        "Nombre del subtítulo"
    )

    def guardar(ev):

        nombre = nombre_input.value.strip().upper()

        if nombre == "":
            mensaje.value = "Captura el nombre del subtítulo"
            page.update()
            return

        cuadrilla["subtitulos"].append(
            crear_subtitulo(nombre)
        )

        dialog.open = False
        actualizar_cuadrillas()

    def cancelar(ev):
        dialog.open = False
        page.update()

    dialog = crear_app_dialog(
        titulo="Nuevo subtítulo",
        descripcion="Ejemplo: RECÁMARA 1, BAÑO PRINCIPAL, PATIO.",
        contenido=[
            nombre_input
        ],
        on_cancelar=cancelar,
        on_guardar=guardar,
    )

    page.overlay.append(dialog)
    dialog.open = True
    page.update()

def abrir_dialogo_agregar_trabajador(
    page,
    cuadrillas,
    cuadrilla,
    buscar_trabajador,
    calcular_valor,
    crear_trabajador,
    recalcular_cuadrilla,
    obtener_siguiente_numero_cuadrilla,
    actualizar_cuadrillas
):

    trabajador_encontrado = {
        "data": None
    }

    mensaje = ft.Text(
        "",
        size=SMALL_TEXT_SIZE,
        color=COLOR_DANGER,
    )

    info_trabajador = ft.Text(
        "Escribe un número de nómina.",
        size=SMALL_TEXT_SIZE,
        color=COLOR_MUTED,
    )

    info_dias = ft.Text(
        "",
        size=SMALL_TEXT_SIZE,
        color=COLOR_MUTED,
    )

    def validar_nomina(e):

        clave = clave_input.value.strip()

        if clave == "":
            trabajador_encontrado["data"] = None
            info_trabajador.value = "Escribe un número de nómina."
            info_trabajador.color = COLOR_MUTED
            page.update()
            return

        trabajador = buscar_trabajador(clave)

        if trabajador:
            trabajador_encontrado["data"] = trabajador
            info_trabajador.value = f"{trabajador[1]} | {trabajador[2]}"
            info_trabajador.color = COLOR_SUCCESS
        else:
            trabajador_encontrado["data"] = None
            info_trabajador.value = "Trabajador no encontrado"
            info_trabajador.color = COLOR_DANGER

        page.update()

    def validar_dias(e):

        if dias_input.value.strip() == "":
            info_dias.value = ""
            page.update()
            return

        dias = calcular_valor(
            dias_input.value
        )

        if dias is None:
            info_dias.value = "Fórmula inválida"
            info_dias.color = COLOR_DANGER
        else:
            info_dias.value = f"Resultado: {dias:.2f} días"
            info_dias.color = COLOR_SUCCESS

        page.update()

    def focus_dias(e):
        dias_input.focus()
        page.update()

    def focus_horas_extras(e):
        horas_extras_input.focus()
        page.update()

    def focus_descripcion(e):
        descripcion_horas_extras_input.focus()
        page.update()

    def guardar_desde_enter(e):
        guardar(e)

    clave_input = crear_app_textfield(
        label="Número de nómina",
        autofocus=True,
        on_change=validar_nomina,
        on_submit=focus_dias,
    )

    dias_input = crear_app_numberfield(
        label="Días trabajados",
        hint_text="Ejemplo: 7, 7/6*5, 3+2",
        on_change=validar_dias,
        on_submit=(
            focus_horas_extras
            if cuadrilla["tipo"] == "dia"
            else guardar_desde_enter
        ),
    )

    horas_extras_input = crear_app_numberfield(
        label="Horas extras",
        on_submit=focus_descripcion,
    )

    descripcion_horas_extras_input = crear_app_multiline(
        label="Descripción horas extras",
    )

    controles_dialogo = [
        clave_input,
        info_trabajador,
        dias_input,
        info_dias,
    ]

    if cuadrilla["tipo"] == "dia":
        controles_dialogo.extend([
            horas_extras_input,
            descripcion_horas_extras_input,
        ])

    controles_dialogo.append(mensaje)

    def guardar(ev):

        clave = clave_input.value.strip()

        if clave == "":
            mensaje.value = "Captura el número de nómina"
            page.update()
            return

        trabajador = trabajador_encontrado["data"]

        if trabajador is None:
            trabajador = buscar_trabajador(clave)

        if not trabajador:
            mensaje.value = "Trabajador no encontrado"
            page.update()
            return

        dias = calcular_valor(
            dias_input.value
        )

        if dias is None:
            mensaje.value = "Días trabajados inválidos"
            page.update()
            return

        if cuadrilla["tipo"] == "dia":
            numero_cuadrilla = obtener_siguiente_numero_cuadrilla(
                cuadrillas
            )
        else:
            numero_cuadrilla = cuadrilla["numero"]

        cuadrilla["trabajadores"].append(
            crear_trabajador(
                trabajador,
                dias,
                numero_cuadrilla,
                horas_extras_input.value.strip(),
                descripcion_horas_extras_input.value.strip()
            )
        )

        if cuadrilla["tipo"] == "destajo":
            recalcular_cuadrilla(
                cuadrilla
            )

        dialog.open = False

        actualizar_cuadrillas()

    def cancelar(ev):

        dialog.open = False
        page.update()

    dialog = crear_app_dialog(
        titulo="Agregar trabajador",
        descripcion="Captura el número de nómina y los días trabajados.",
        contenido=controles_dialogo,
        on_cancelar=cancelar,
        on_guardar=guardar,
        width=460,
    )

    page.overlay.append(dialog)
    dialog.open = True
    page.update()

def abrir_dialogo_agregar_concepto(
    page,
    subtitulo,
    buscar_concepto,
    crear_concepto,
    actualizar_cuadrillas
):

    mensaje = texto_error()

    clave_input = campo_texto("Clave concepto")
    largo_input = campo_texto("Largo")
    ancho_input = campo_texto("Ancho")
    alto_input = campo_texto("Alto")
    piezas_input = campo_texto("Piezas")
    notas_input = campo_texto("Notas", multiline=True)

    concepto_info = ft.Container(
        padding=12,
        bgcolor=COLOR_BACKGROUND,
        border_radius=CARD_RADIUS,
        content=ft.Text(
            "Escribe una clave para consultar el concepto.",
            size=SMALL_TEXT_SIZE,
            color=COLOR_MUTED,
        ),
    )

    def consultar_concepto(e):

        concepto_bd = buscar_concepto(
            clave_input.value.strip().upper()
        )

        if concepto_bd:
            concepto_info.content.value = (
                f"{concepto_bd[1]} | Unidad: {concepto_bd[2]}"
            )
            concepto_info.content.color = COLOR_SUCCESS
        else:
            concepto_info.content.value = "Concepto no encontrado"
            concepto_info.content.color = COLOR_DANGER

        page.update()

    clave_input.on_change = consultar_concepto

    def guardar(ev):

        clave = clave_input.value.strip().upper()

        if clave == "":
            mensaje.value = "Captura la clave del concepto"
            page.update()
            return

        concepto_bd = buscar_concepto(clave)

        if not concepto_bd:
            mensaje.value = "Concepto no encontrado"
            page.update()
            return

        subtitulo["conceptos"].append(
            crear_concepto(
                concepto_bd,
                largo_input.value.strip(),
                ancho_input.value.strip(),
                alto_input.value.strip(),
                piezas_input.value.strip(),
                notas_input.value.strip()
            )
        )

        dialog.open = False
        actualizar_cuadrillas()

    def cancelar(ev):
        dialog.open = False
        page.update()

    dialog = ft.AlertDialog(
        modal=True,

        title=ft.Text(
            "Nuevo concepto",
            size=SUBTITLE_SIZE,
            weight=ft.FontWeight.BOLD,
            color=COLOR_TEXT,
        ),

        content=ft.Container(
            width=520,
            content=ft.Column(
                spacing=14,
                tight=True,
                controls=[
                    ft.Text(
                        "Captura la clave del concepto y sus medidas.",
                        size=SMALL_TEXT_SIZE,
                        color=COLOR_MUTED,
                    ),
                    clave_input,
                    concepto_info,
                    ft.Row(
                        spacing=10,
                        controls=[
                            ft.Container(expand=True, content=largo_input),
                            ft.Container(expand=True, content=ancho_input),
                        ],
                    ),
                    ft.Row(
                        spacing=10,
                        controls=[
                            ft.Container(expand=True, content=alto_input),
                            ft.Container(expand=True, content=piezas_input),
                        ],
                    ),
                    notas_input,
                    mensaje,
                ],
            ),
        ),

        actions=[
            ft.TextButton(
                "Cancelar",
                on_click=cancelar,
            ),
            ft.ElevatedButton(
                height=BUTTON_HEIGHT,
                bgcolor=COLOR_PRIMARY,
                color="white",
                content=ft.Text("Guardar"),
                on_click=guardar,
            ),
        ],
    )

    page.overlay.append(dialog)
    dialog.open = True
    page.update()


def abrir_dialogo_agregar_actividades(
    page,
    subtitulo,
    actualizar_cuadrillas
):

    mensaje = texto_error()

    actividades_input = campo_texto(
        "Actividades realizadas",
        multiline=True,
        value=subtitulo.get("actividades", "")
    )

    def guardar(ev):

        actividades = actividades_input.value.strip()

        if actividades == "":
            mensaje.value = "Captura las actividades realizadas"
            page.update()
            return

        subtitulo["actividades"] = actividades

        dialog.open = False
        actualizar_cuadrillas()

    def cancelar(ev):
        dialog.open = False
        page.update()

    dialog = ft.AlertDialog(
        modal=True,

        title=ft.Text(
            "Agregar actividades",
            size=SUBTITLE_SIZE,
            weight=ft.FontWeight.BOLD,
            color=COLOR_TEXT,
        ),

        content=ft.Container(
            width=520,
            content=ft.Column(
                spacing=14,
                tight=True,
                controls=[
                    ft.Text(
                        "Describe las actividades realizadas en este subtítulo.",
                        size=SMALL_TEXT_SIZE,
                        color=COLOR_MUTED,
                    ),
                    actividades_input,
                    mensaje,
                ],
            ),
        ),

        actions=[
            ft.TextButton(
                "Cancelar",
                on_click=cancelar,
            ),
            ft.ElevatedButton(
                height=BUTTON_HEIGHT,
                bgcolor=COLOR_PRIMARY,
                color="white",
                content=ft.Text("Guardar"),
                on_click=guardar,
            ),
        ],
    )

    page.overlay.append(dialog)
    dialog.open = True
    page.update()

#endregion
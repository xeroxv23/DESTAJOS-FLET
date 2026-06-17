import flet as ft


# !! ==========================================================
# !! DIALOGS.PY
# !!
# !! Biblioteca central de formularios emergentes.
# !!
# !! Responsabilidades:
# !! - Nueva Cuadrilla
# !! - Agregar Trabajador
# !! - Agregar Subtítulo
# !! - Agregar Concepto
# !!
# !! Beneficio:
# !!
# !! obra_view.py ya no contiene cientos
# !! de líneas de formularios.
# !!
# !! Toda la captura de información vive aquí.
# !!
# !! ==========================================================

def abrir_dialogo_nueva_cuadrilla(
    page,
    cuadrillas,
    crear_cuadrilla,
    obtener_siguiente_numero_cuadrilla,
    actualizar_cuadrillas
):

    tipo = ft.RadioGroup(

        content=ft.Column(

            controls=[

                ft.Radio(
                    value="dia",
                    label="Por Día"
                ),

                ft.Radio(
                    value="destajo",
                    label="Destajo"
                )

            ]

        )

    )

    def guardar(ev):

        if not tipo.value:
            return

        if tipo.value == "destajo":

            numero = obtener_siguiente_numero_cuadrilla(
                cuadrillas
            )

        else:

            numero = None

        cuadrillas.append(
            crear_cuadrilla(
                numero,
                tipo.value
            )
        )

        dialog.open = False

        actualizar_cuadrillas()

    def cancelar(ev):

        dialog.open = False

        page.update()

    dialog = ft.AlertDialog(

        title=ft.Text(
            "Nueva Cuadrilla"
        ),

        content=tipo,

        actions=[

            ft.TextButton(
                "Cancelar",
                on_click=cancelar
            ),

            ft.TextButton(
                "Guardar",
                on_click=guardar
            )

        ]

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

    nombre_input = ft.TextField(
        label="Nombre del subtítulo"
    )

    def guardar(ev):

        nombre = nombre_input.value.strip()

        if nombre == "":
            return

        cuadrilla["subtitulos"].append(
            crear_subtitulo(nombre)
        )

        dialog.open = False

        actualizar_cuadrillas()

    def cancelar(ev):

        dialog.open = False
        page.update()

    dialog = ft.AlertDialog(
        title=ft.Text("Nuevo Subtítulo"),
        content=nombre_input,
        actions=[
            ft.TextButton("Cancelar", on_click=cancelar),
            ft.TextButton("Guardar", on_click=guardar)
        ]
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

    clave_input = ft.TextField(
        label="Número de nómina"
    )

    dias_input = ft.TextField(
        label="Días trabajados"
    )

    horas_extras_input = ft.TextField(
        label="Horas extras"
    )

    descripcion_horas_extras_input = ft.TextField(
        label="Descripción horas extras",
        multiline=True
    )

    def guardar(ev):

        trabajador = buscar_trabajador(
            clave_input.value
        )

        if not trabajador:
            print("Trabajador no encontrado")
            return

        dias = calcular_valor(
            dias_input.value
        )

        if dias is None:
            print("Fórmula inválida")
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

        # !! Solo las cuadrillas de destajo
        # !! calculan porcentajes de participación.
        if cuadrilla["tipo"] == "destajo":

            recalcular_cuadrilla(
                cuadrilla
            )

        dialog.open = False

        actualizar_cuadrillas()

    def cancelar(ev):

        dialog.open = False
        page.update()

    dialog = ft.AlertDialog(

        title=ft.Text(
            "Agregar Trabajador"
        ),

        content=ft.Column(
            controls=[
            clave_input,
            dias_input,
            horas_extras_input,
            descripcion_horas_extras_input
        ],
            tight=True
        ),

        actions=[
            ft.TextButton(
                "Cancelar",
                on_click=cancelar
            ),

            ft.TextButton(
                "Guardar",
                on_click=guardar
            )
        ]
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

    clave_input = ft.TextField(label="Clave Concepto")
    largo_input = ft.TextField(label="Largo")
    ancho_input = ft.TextField(label="Ancho")
    alto_input = ft.TextField(label="Alto")
    piezas_input = ft.TextField(label="Piezas")
    notas_input = ft.TextField(label="Notas", multiline=True)

    concepto_info = ft.Text("")

    def consultar_concepto(e):

        concepto_bd = buscar_concepto(
            clave_input.value.strip()
        )

        if concepto_bd:
            concepto_info.value = (
                f"{concepto_bd[1]} | Unidad: {concepto_bd[2]}"
            )
        else:
            concepto_info.value = "Concepto no encontrado"

        page.update()

    clave_input.on_change = consultar_concepto

    def guardar(ev):

        concepto_bd = buscar_concepto(
            clave_input.value.strip()
        )

        if not concepto_bd:
            print("Concepto no encontrado")
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

        title=ft.Text("Nuevo Concepto"),

        content=ft.Column(
            controls=[
                clave_input,
                concepto_info,
                largo_input,
                ancho_input,
                alto_input,
                piezas_input,
                notas_input
            ],
            tight=True
        ),

        actions=[
            ft.TextButton("Cancelar", on_click=cancelar),
            ft.TextButton("Guardar", on_click=guardar)
        ]
    )

    page.overlay.append(dialog)
    dialog.open = True
    page.update()

def abrir_dialogo_agregar_actividades(
    page,
    cuadrilla,
    actualizar_cuadrillas
):

    actividades_input = ft.TextField(
        label="Actividades realizadas",
        multiline=True,
        value=cuadrilla.get("actividades", "")
    )

    def guardar(ev):

        cuadrilla["actividades"] = actividades_input.value.strip()

        dialog.open = False

        actualizar_cuadrillas()

    def cancelar(ev):

        dialog.open = False

        page.update()

    dialog = ft.AlertDialog(

        title=ft.Text(
            "Agregar Actividades"
        ),

        content=actividades_input,

        actions=[

            ft.TextButton(
                "Cancelar",
                on_click=cancelar
            ),

            ft.TextButton(
                "Guardar",
                on_click=guardar
            )

        ]

    )

    page.overlay.append(dialog)

    dialog.open = True

    page.update()

# CODIGO
import flet as ft

from database_manager import buscar_obras

from views.obra_view import obra_view
from views.preview_view import preview_view

from services.persistencia_json import (
    obtener_claves_capturadas_semana,
    eliminar_captura_json
)

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
    CARD_PADDING,
    BUTTON_HEIGHT,
    SUBTITLE_SIZE,
    TEXT_SIZE,
    SMALL_TEXT_SIZE,
    PAGE_PADDING,
)

#COMPONENTES
from components.app_panel import crear_app_panel
from components.app_search import crear_app_search
from components.app_sidebar import crear_app_sidebar
from components.app_confirm import abrir_app_confirm


from layouts import crear_work_layout


#region OBRAS_VIEW.PY

# !! ==========================================================
# !! OBRAS_VIEW.PY
# !!
# !! Pantalla de selección de obras por semana.
# !!
# !! Funciones principales:
# !! - Buscar obras por clave
# !! - Mostrar resultados encontrados
# !! - Abrir captura de obra
# !! - Mostrar obras ya capturadas
# !! - Abrir vista previa de captura
# !! - Eliminar captura existente
# !!
# !! Flujo:
# !!
# !! semanas_view.py
# !!      ↓
# !! obras_view(page, semana_actual)
# !!      ↓
# !! obra_view.py / preview_view.py
# !! ==========================================================


def obras_view(page, semana_actual):

    # ======================================================
    # LISTA DE RESULTADOS DE BÚSQUEDA
    # ======================================================

    lista_view = ft.ListView(
        expand=True,
        spacing=12,
        padding=0,
    )

    # ======================================================
    # LISTA LATERAL DE OBRAS CAPTURADAS
    # ======================================================

    lista_capturadas = ft.Column(
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    # ======================================================
    # ACTUALIZAR OBRAS CAPTURADAS
    # ======================================================

    def actualizar_obras_capturadas():

        lista_capturadas.controls.clear()

        claves_capturadas = obtener_claves_capturadas_semana(
            semana_actual
        )

        if len(claves_capturadas) == 0:

            lista_capturadas.controls.append(
                ft.Container(
                    padding=16,
                    bgcolor=COLOR_BACKGROUND,
                    border_radius=CARD_RADIUS,
                    content=ft.Text(
                        "Sin obras capturadas",
                        size=TEXT_SIZE,
                        color=COLOR_MUTED,
                    ),
                )
            )

        else:

            for clave_capturada in claves_capturadas:

                def abrir_capturada(e, clave=clave_capturada):

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

                def vista_previa(e, clave=clave_capturada):

                    page.views.append(
                        preview_view(
                            page,
                            semana_actual,
                            clave
                        )
                    )

                    page.update()

                def eliminar_captura(e, clave=clave_capturada):

                    def confirmar_eliminacion():

                        eliminar_captura_json(
                            semana_actual,
                            clave
                        )

                        actualizar_obras_capturadas()

                        lista_view.controls.clear()

                        lista_view.controls.append(
                            mensaje_inicial()
                        )

                        page.update()

                    abrir_app_confirm(
                        page=page,
                        titulo="Eliminar captura",
                        mensaje=f"¿Deseas eliminar la captura de la obra {clave}?",
                        on_confirmar=confirmar_eliminacion,
                        texto_confirmar="Eliminar",
                    )

                lista_capturadas.controls.append(
                    ft.Container(
                        padding=14,
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
                                    clave_capturada,
                                    size=TEXT_SIZE,
                                    weight=ft.FontWeight.BOLD,
                                    color=COLOR_TEXT,
                                ),

                                ft.Row(
                                    spacing=4,
                                    wrap=True,
                                    controls=[

                                        ft.TextButton(
                                            content=ft.Text(
                                                "Abrir",
                                                size=SMALL_TEXT_SIZE,
                                                color=COLOR_PRIMARY,
                                            ),
                                            on_click=abrir_capturada,
                                        ),

                                        ft.TextButton(
                                            content=ft.Text(
                                                "Vista",
                                                size=SMALL_TEXT_SIZE,
                                                color=COLOR_PRIMARY,
                                            ),
                                            on_click=vista_previa,
                                        ),

                                        ft.TextButton(
                                            content=ft.Text(
                                                "Eliminar",
                                                size=SMALL_TEXT_SIZE,
                                                color=COLOR_DANGER,
                                            ),
                                            on_click=eliminar_captura,
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    )
                )

    # ======================================================
    # MENSAJE INICIAL
    # ======================================================

    def mensaje_inicial():

        return ft.Container(
            padding=24,
            bgcolor=COLOR_SURFACE,
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
                        "Busca una obra para comenzar",
                        size=SUBTITLE_SIZE,
                        weight=ft.FontWeight.BOLD,
                        color=COLOR_TEXT,
                    ),
                    ft.Text(
                        "Escribe una clave de obra, por ejemplo: A-001.",
                        size=TEXT_SIZE,
                        color=COLOR_MUTED,
                    ),
                ],
            ),
        )

    # ======================================================
    # CARGAR OBRAS ENCONTRADAS
    # ======================================================

    def cargar_obras(obras):

        claves_capturadas = obtener_claves_capturadas_semana(
            semana_actual
        )

        lista_view.controls.clear()

        if len(obras) == 0:

            lista_view.controls.append(
                ft.Container(
                    padding=24,
                    bgcolor=COLOR_SURFACE,
                    border_radius=CARD_RADIUS,
                    border=ft.Border(
                        left=ft.BorderSide(1, COLOR_BORDER),
                        top=ft.BorderSide(1, COLOR_BORDER),
                        right=ft.BorderSide(1, COLOR_BORDER),
                        bottom=ft.BorderSide(1, COLOR_BORDER),
                    ),
                    content=ft.Text(
                        "No se encontraron obras con esa clave.",
                        size=TEXT_SIZE,
                        color=COLOR_MUTED,
                    ),
                )
            )

            page.update()
            return

        for clave, nombre in obras:

            capturada = clave in claves_capturadas

            def abrir_obra(e, clave=clave, nombre=nombre):

                page.views.append(
                    obra_view(
                        page,
                        clave,
                        nombre,
                        semana_actual
                    )
                )

                page.update()

            lista_view.controls.append(
                ft.Container(
                    padding=CARD_PADDING,
                    bgcolor=COLOR_SURFACE,
                    border_radius=CARD_RADIUS,
                    border=ft.Border(
                        left=ft.BorderSide(1, COLOR_BORDER),
                        top=ft.BorderSide(1, COLOR_BORDER),
                        right=ft.BorderSide(1, COLOR_BORDER),
                        bottom=ft.BorderSide(1, COLOR_BORDER),
                    ),

                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,

                        controls=[

                            ft.Column(
                                spacing=6,
                                expand=True,
                                controls=[

                                    ft.Text(
                                        clave,
                                        size=SUBTITLE_SIZE,
                                        weight=ft.FontWeight.BOLD,
                                        color=COLOR_TEXT,
                                    ),

                                    ft.Text(
                                        nombre,
                                        size=TEXT_SIZE,
                                        color=COLOR_MUTED,
                                    ),

                                    ft.Text(
                                        "CAPTURADA" if capturada else "SIN CAPTURA",
                                        size=SMALL_TEXT_SIZE,
                                        weight=ft.FontWeight.BOLD,
                                        color=COLOR_SUCCESS if capturada else COLOR_MUTED,
                                    ),
                                ],
                            ),

                            ft.ElevatedButton(
                                height=BUTTON_HEIGHT,
                                bgcolor=COLOR_PRIMARY,
                                color="white",
                                content=ft.Text(
                                    "Abrir obra",
                                    size=TEXT_SIZE,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                on_click=abrir_obra,
                            ),
                        ],
                    ),
                )
            )

        page.update()

    # ======================================================
    # FILTRAR OBRAS
    # ======================================================

    def filtrar_obras(e):

        texto = e.control.value.strip().upper()

        if texto == "":

            lista_view.controls.clear()
            lista_view.controls.append(
                mensaje_inicial()
            )

            page.update()
            return

        resultados = buscar_obras(texto)

        cargar_obras(resultados)

    # ======================================================
    # REGRESAR A SEMANAS
    # ======================================================

    def regresar_semanas(e):

        page.views.pop()
        page.update()

    # ======================================================
    # BUSCADOR PRINCIPAL
    # ======================================================

    buscador = crear_app_search(
    label="Buscar obra por clave",
    hint_text="Ejemplo: A-001",
    on_change=filtrar_obras,
    width=520,
    autofocus=True,
)

    # Mensaje inicial
    lista_view.controls.append(
        mensaje_inicial()
    )

    actualizar_obras_capturadas()

    # ======================================================
    # RETURN DE LA VISTA
    # ======================================================

    return crear_work_layout(
        route="/obras",

        header_titulo=f"Semana {semana_actual['numero']}",
        header_subtitulo=(
            f"{semana_actual['fecha_inicio']} - "
            f"{semana_actual['fecha_fin']}"
        ),

        titulo="Listado de obras",
        descripcion="Busca una obra por clave para abrir o continuar su captura.",

        texto_boton="Regresar",
        on_regresar=regresar_semanas,

        controls=[
            ft.Row(
                expand=True,
                spacing=16,
                vertical_alignment=ft.CrossAxisAlignment.START,

                controls=[
                    ft.Column(
                        expand=True,
                        spacing=14,
                        controls=[
                            ft.Container(
                                width=960,
                                padding=16,
                                bgcolor=COLOR_SURFACE,
                                border_radius=CARD_RADIUS,
                                border=ft.Border(
                                    left=ft.BorderSide(1, COLOR_BORDER),
                                    top=ft.BorderSide(1, COLOR_BORDER),
                                    right=ft.BorderSide(1, COLOR_BORDER),
                                    bottom=ft.BorderSide(1, COLOR_BORDER),
                                ),
                                content=buscador,
                            ),

                            crear_app_panel(
                                titulo="Resultados de búsqueda",
                                contenido=lista_view,
                                expand=True,
                            ),
                        ],
                    ),

                    crear_app_sidebar(
                        titulo="Obras capturadas",
                        contenido=lista_capturadas,
                        width=260,
                        height=420,
                    ),
                ],
            ),
        ],
    )

#endregion
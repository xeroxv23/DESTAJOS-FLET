import flet as ft

from views.obras_view import obras_view

from services.semanas_service import (
    agregar_semana,
    eliminar_semana,
    listar_semanas
)

from services.persistencia_json import listar_capturas_semana

from styles import (
    COLOR_PRIMARY,
    COLOR_TEXT,
    COLOR_MUTED,
    COLOR_DANGER,
    COLOR_BORDER,
    BUTTON_HEIGHT,
    SUBTITLE_SIZE,
    TEXT_SIZE,
    SMALL_TEXT_SIZE,
)

# COMPONENTES
from components.app_card import (
    crear_app_card,
    crear_app_empty_card
)

from components.app_confirm import abrir_app_confirm

from layouts import crear_list_layout

#region SEMANAS_VIEW.PY

# !! ==========================================================
# !! SEMANAS_VIEW.PY
# !!
# !! Pantalla principal después del Login.
# !!
# !! Funciones principales:
# !! - Mostrar semanas creadas
# !! - Crear nueva semana
# !! - Eliminar semana
# !! - Abrir obras correspondientes a una semana
# !! - Mostrar cuántas obras tienen captura en cada semana
# !!
# !! Flujo:
# !!
# !! login_view.py
# !!     ↓
# !! semanas_view(page)
# !!     ↓
# !! Usuario selecciona semana
# !!     ↓
# !! obras_view(page, semana)
# !! ==========================================================


def semanas_view(page):

    # ======================================================
    # CONTENEDOR DE LISTADO DE SEMANAS
    #
    # Aquí se agregan dinámicamente las tarjetas de semanas.
    # ======================================================

    lista_semanas = ft.Column(
        spacing=16,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    # ======================================================
    # ACTUALIZAR SEMANAS
    #
    # Limpia y reconstruye visualmente el listado de semanas.
    # ======================================================

    def actualizar_semanas():

        lista_semanas.controls.clear()

        semanas = listar_semanas()

        if len(semanas) == 0:

            lista_semanas.controls.append(
                crear_app_empty_card(
                    titulo="No hay semanas creadas",
                    descripcion="Crea una nueva semana para comenzar la captura.",
                )
                
            )

        else:

            for semana in semanas:

                capturas = listar_capturas_semana(semana)

                def abrir_semana(e, semana=semana):

                    page.views.append(
                        obras_view(
                            page,
                            semana
                        )
                    )

                    page.update()

                def borrar_semana(e, semana=semana):

                    def confirmar_eliminacion():

                        eliminar_semana(
                            semana
                        )

                        actualizar_semanas()

                    abrir_app_confirm(
                        page=page,
                        titulo="Eliminar semana",
                        mensaje=(
                            f"¿Deseas eliminar la semana {semana['numero']}? "
                            "Esta acción puede afectar las capturas relacionadas."
                        ),
                        on_confirmar=confirmar_eliminacion,
                        texto_confirmar="Eliminar",
                    )

                lista_semanas.controls.append(
                    crear_app_card(
                        contenido=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,

                            controls=[

                                ft.Column(
                                    spacing=6,
                                    controls=[
                                        ft.Text(
                                            f"Semana {semana['numero']}",
                                            size=SUBTITLE_SIZE,
                                            weight=ft.FontWeight.BOLD,
                                            color=COLOR_TEXT,
                                        ),

                                        ft.Text(
                                            f"Inicio: {semana['fecha_inicio']}  |  Cierre: {semana['fecha_fin']}",
                                            size=TEXT_SIZE,
                                            color=COLOR_MUTED,
                                        ),

                                        ft.Text(
                                            f"Obras capturadas: {len(capturas)}",
                                            size=SMALL_TEXT_SIZE,
                                            color=COLOR_MUTED,
                                        ),
                                    ],
                                ),

                                ft.Row(
                                    spacing=10,
                                    controls=[
                                        ft.ElevatedButton(
                                            height=BUTTON_HEIGHT,
                                            bgcolor=COLOR_PRIMARY,
                                            color="white",
                                            content=ft.Text(
                                                "Abrir semana",
                                                size=TEXT_SIZE,
                                                weight=ft.FontWeight.BOLD,
                                            ),
                                            on_click=abrir_semana,
                                        ),

                                        ft.TextButton(
                                            content=ft.Text(
                                                "Eliminar",
                                                color=COLOR_DANGER,
                                                size=TEXT_SIZE,
                                            ),
                                            on_click=borrar_semana,
                                        ),
                                    ],
                                ),
                            ],
                        )
                    )
                )

        page.update()

    # ======================================================
    # NUEVA SEMANA
    #
    # Abre un cuadro de diálogo para capturar:
    # - Número de semana
    # - Fecha de inicio
    #
    # La fecha de cierre se calcula automáticamente
    # desde semanas_service.py.
    # ======================================================

    def nueva_semana(e):

        numero_input = ft.TextField(
            label="Número de semana",
            height=56,
            border_color=COLOR_BORDER,
            focused_border_color=COLOR_PRIMARY,
            text_size=TEXT_SIZE,
        )

        inicio_input = ft.TextField(
            label="Fecha inicio lunes (dd/mm/aa)",
            height=56,
            border_color=COLOR_BORDER,
            focused_border_color=COLOR_PRIMARY,
            text_size=TEXT_SIZE,
        )

        def guardar(ev):

            if numero_input.value.strip() == "":
                return

            if inicio_input.value.strip() == "":
                return

            agregar_semana(
                numero_input.value.strip(),
                inicio_input.value.strip()
            )

            dialog.open = False

            actualizar_semanas()

        def cancelar(ev):

            dialog.open = False

            page.update()

        dialog = ft.AlertDialog(
            modal=True,

            title=ft.Text(
                "Nueva semana",
                size=SUBTITLE_SIZE,
                weight=ft.FontWeight.BOLD,
                color=COLOR_TEXT,
            ),

            content=ft.Column(
                width=360,
                spacing=14,
                controls=[
                    numero_input,

                    inicio_input,

                    ft.Text(
                        "La fecha de cierre se calculará automáticamente +6 días.",
                        size=SMALL_TEXT_SIZE,
                        color=COLOR_MUTED,
                    )
                ],
                tight=True,
            ),

            actions=[
                ft.TextButton(
                    "Cancelar",
                    on_click=cancelar
                ),

                ft.ElevatedButton(
                    bgcolor=COLOR_PRIMARY,
                    color="white",
                    content=ft.Text("Guardar"),
                    on_click=guardar
                )
            ]
        )

        page.overlay.append(dialog)

        dialog.open = True

        page.update()

    # Cargar semanas al entrar a la vista
    actualizar_semanas()

    # ======================================================
    # CONSTRUCCIÓN VISUAL DE LA VISTA
    # ======================================================

    return crear_list_layout(
        route="/semanas",

        header_titulo="Capturador Destajos",
        header_subtitulo="Administración de semanas de captura",

        acciones_titulo="Gestión de semanas",
        acciones_descripcion="Crea nuevas semanas de captura para organizar tus destajos.",
        acciones=[
            {
                "texto": "Nueva semana",
                "on_click": nueva_semana,
                "tipo": "primary",
            },
        ],

        titulo="Semanas de captura",
        descripcion="Selecciona una semana para continuar con la captura de obras.",

        contenido=lista_semanas,
    )

#endregion
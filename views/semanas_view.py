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
    COLOR_PRIMARY_DARK,
    COLOR_BACKGROUND,
    COLOR_SURFACE,
    COLOR_TEXT,
    COLOR_MUTED,
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
                ft.Container(
                    padding=32,
                    bgcolor=COLOR_SURFACE,
                    border_radius=CARD_RADIUS,
                    border=ft.Border(
                        left=ft.BorderSide(1, COLOR_BORDER),
                        top=ft.BorderSide(1, COLOR_BORDER),
                        right=ft.BorderSide(1, COLOR_BORDER),
                        bottom=ft.BorderSide(1, COLOR_BORDER),
                    ),
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10,
                        controls=[
                            ft.Text(
                                "No hay semanas creadas",
                                size=SUBTITLE_SIZE,
                                weight=ft.FontWeight.BOLD,
                                color=COLOR_TEXT,
                            ),
                            ft.Text(
                                "Crea una nueva semana para comenzar la captura.",
                                size=TEXT_SIZE,
                                color=COLOR_MUTED,
                                text_align=ft.TextAlign.CENTER,
                            ),
                        ],
                    ),
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

                    eliminar_semana(
                        semana
                    )

                    actualizar_semanas()

                lista_semanas.controls.append(
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
                        ),
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

    return ft.View(
        route="/semanas",
        bgcolor=COLOR_BACKGROUND,
        padding=PAGE_PADDING,

        controls=[

            # Header superior
            ft.Container(
                padding=20,
                bgcolor=COLOR_PRIMARY_DARK,
                border_radius=CARD_RADIUS,

                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,

                    controls=[

                        ft.Column(
                            spacing=4,
                            controls=[
                                ft.Text(
                                    "Capturador Destajos",
                                    size=SUBTITLE_SIZE,
                                    weight=ft.FontWeight.BOLD,
                                    color="white",
                                ),

                                ft.Text(
                                    "Administración de semanas de captura",
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
                                "Nueva semana",
                                size=TEXT_SIZE,
                                weight=ft.FontWeight.BOLD,
                            ),
                            on_click=nueva_semana,
                        ),
                    ],
                ),
            ),

            ft.Container(height=18),

            ft.Text(
                "Semanas de captura",
                size=TITLE_SIZE,
                weight=ft.FontWeight.BOLD,
                color=COLOR_TEXT,
            ),

            ft.Text(
                "Selecciona una semana para continuar con la captura de obras.",
                size=TEXT_SIZE,
                color=COLOR_MUTED,
            ),

            ft.Container(height=10),

            lista_semanas,
        ],
    )

#endregion
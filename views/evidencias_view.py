import flet as ft

from services.evidencias_service import (
    guardar_evidencia_desde_archivo,
    listar_evidencias,
    eliminar_evidencia
)

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
    BUTTON_HEIGHT,
    TITLE_SIZE,
    SUBTITLE_SIZE,
    TEXT_SIZE,
    SMALL_TEXT_SIZE,
    PAGE_PADDING,
)

#COMPONENTES
from components.app_confirm import abrir_app_confirm
from components.app_header import crear_app_header
from components.app_card import (
    crear_app_card,
    crear_app_empty_card
)


#region EVIDENCIAS_VIEW.PY

def evidencias_view(page, semana_actual, clave_obra, nombre_obra):

    lista_evidencias = ft.Column(
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    nombre_evidencia_input = ft.TextField(
        label="Nombre de la evidencia",
        hint_text="Ejemplo: fachada, recámara principal, baño planta alta",
        height=56,
        border_color=COLOR_BORDER,
        focused_border_color=COLOR_PRIMARY,
        text_size=TEXT_SIZE,
    )

    ruta_evidencia_input = ft.TextField(
        label="Ruta de la imagen",
        hint_text=r"Ejemplo: C:\Users\Carlos\Pictures\foto.jpg",
        height=56,
        border_color=COLOR_BORDER,
        focused_border_color=COLOR_PRIMARY,
        text_size=TEXT_SIZE,
    )

    mensaje = ft.Text(
        "",
        size=SMALL_TEXT_SIZE,
        color=COLOR_DANGER,
    )

    def actualizar_evidencias():

        lista_evidencias.controls.clear()

        evidencias = listar_evidencias(
            semana_actual,
            clave_obra
        )

        if len(evidencias) == 0:

            lista_evidencias.controls.append(
                crear_app_empty_card(

                    titulo="Sin evidencias fotográficas",

                    descripcion=(
                        "Todavía no se han agregado imágenes "
                        "para esta obra."
                    )
                )
            )

        else:

            for evidencia in evidencias:

                def borrar_evidencia(e, ruta=evidencia["ruta"]):

                    def confirmar_eliminacion():

                        eliminar_evidencia(ruta)
                        actualizar_evidencias()

                    abrir_app_confirm(
                        page=page,
                        titulo="Eliminar evidencia",
                        mensaje="¿Deseas eliminar esta evidencia fotográfica?",
                        on_confirmar=confirmar_eliminacion,
                        texto_confirmar="Eliminar",
                    )

                lista_evidencias.controls.append(
                    crear_app_card(
                        contenido=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[

                                ft.Column(
                                    spacing=4,
                                    expand=True,
                                    controls=[
                                        ft.Text(
                                            evidencia["nombre"],
                                            size=TEXT_SIZE,
                                            weight=ft.FontWeight.BOLD,
                                            color=COLOR_TEXT,
                                        ),

                                        ft.Text(
                                            evidencia["ruta"],
                                            size=SMALL_TEXT_SIZE,
                                            color=COLOR_MUTED,
                                        ),
                                    ],
                                ),

                                ft.TextButton(
                                    content=ft.Text(
                                        "Eliminar",
                                        size=TEXT_SIZE,
                                        color=COLOR_DANGER,
                                    ),
                                    on_click=borrar_evidencia,
                                ),
                            ],
                        )
                    )
                )

        page.update()

    def agregar_evidencia(e):

        nombre = nombre_evidencia_input.value.strip()
        ruta = ruta_evidencia_input.value.strip()

        if nombre == "":
            mensaje.value = "Captura un nombre para la evidencia"
            page.update()
            return

        if ruta == "":
            mensaje.value = "Captura la ruta de la imagen"
            page.update()
            return

        try:
            guardar_evidencia_desde_archivo(
                semana_actual,
                clave_obra,
                ruta,
                nombre
            )
        except Exception as error:
            mensaje.value = str(error)
            page.update()
            return

        nombre_evidencia_input.value = ""
        ruta_evidencia_input.value = ""
        mensaje.value = ""

        actualizar_evidencias()

    def regresar_obra(e):

        page.views.pop()
        page.update()

    actualizar_evidencias()

    return ft.View(
        route="/evidencias",
        bgcolor=COLOR_BACKGROUND,
        padding=PAGE_PADDING,

        controls=[
            ft.Column(
                expand=True,
                spacing=16,

                controls=[

                    crear_app_header(
                        titulo="Evidencias fotográficas",
                        subtitulo=f"{clave_obra} - {nombre_obra}",
                        descripcion=f"Semana {semana_actual['numero']}",
                        texto_boton="Regresar",
                        on_regresar=regresar_obra,
                    ),
                    
                    crear_app_card(
                        titulo="Agregar evidencia",
                        subtitulo=(
                            "Temporalmente usaremos una ruta de imagen en Windows. "
                            "En Android se cambiará por cámara o galería."
                        ),
                        contenido=ft.Column(
                            spacing=12,
                            controls=[
                                nombre_evidencia_input,

                                ruta_evidencia_input,

                                mensaje,

                                ft.ElevatedButton(
                                    height=BUTTON_HEIGHT,
                                    bgcolor=COLOR_PRIMARY,
                                    color="white",
                                    content=ft.Text(
                                        "Agregar evidencia",
                                        size=TEXT_SIZE,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                    on_click=agregar_evidencia,
                                ),
                            ],
                        ),
                    ),

                    crear_app_card(
                        titulo="Evidencias guardadas",
                        contenido=lista_evidencias,
                        expand=True,
                    ),
                ],
            )
        ],
    )

#endregion
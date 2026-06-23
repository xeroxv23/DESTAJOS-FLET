import flet as ft

from database_manager import validar_usuario
from views.semanas_view import semanas_view

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
    TEXT_SIZE,
    SMALL_TEXT_SIZE,
)


#region LOGIN_VIEW.PY

# !! ==========================================================
# !! LOGIN_VIEW.PY
# !!
# !! Primera pantalla del sistema.
# !!
# !! Funciones principales:
# !! - Solicitar usuario
# !! - Solicitar contraseña
# !! - Validar credenciales contra SQLite
# !! - Mostrar mensajes de error
# !! - Redirigir al listado de semanas si el acceso es válido
# !!
# !! Flujo:
# !!
# !! main.py
# !!     ↓
# !! login_view(page)
# !!     ↓
# !! Usuario captura credenciales
# !!     ↓
# !! validar_usuario()
# !!     ↓
# !! semanas_view(page)
# !! ==========================================================


def login_view(page):

    # ======================================================
    # MENSAJE DE ERROR / VALIDACIÓN
    #
    # Se muestra cuando:
    # - El usuario deja campos vacíos
    # - El usuario o contraseña son incorrectos
    # ======================================================

    mensaje = ft.Text(
        "",
        color=COLOR_DANGER,
        size=SMALL_TEXT_SIZE,
    )

    # ======================================================
    # FUNCIÓN INICIAR SESIÓN
    #
    # Se ejecuta cuando:
    # - El usuario presiona el botón "Iniciar sesión"
    # - El usuario presiona Enter en usuario o contraseña
    # ======================================================

    def iniciar_sesion(e):

        # Leer valores capturados
        usuario = txt_usuario.value.strip()
        password = txt_password.value.strip()

        # Validar campos vacíos antes de consultar SQLite
        if not usuario or not password:
            mensaje.value = "Captura usuario y contraseña"
            page.update()
            return

        # Consultar usuario y contraseña en SQLite
        resultado = validar_usuario(
            usuario,
            password
        )

        # Si las credenciales son correctas
        if resultado:

            # Limpiar vistas actuales
            page.views.clear()

            # Abrir pantalla de semanas
            page.views.append(
                semanas_view(page)
            )

            page.update()

        # Si las credenciales son incorrectas
        else:
            mensaje.value = "Usuario o contraseña incorrectos"
            page.update()

    # ======================================================
    # CAMPO USUARIO
    #
    # Permite capturar el usuario registrado en la base
    # de datos LOGIN BD / SQLite.
    # ======================================================

    txt_usuario = ft.TextField(
        label="Usuario",
        width=320,
        height=56,
        border_color=COLOR_BORDER,
        focused_border_color=COLOR_PRIMARY,
        text_size=TEXT_SIZE,
        on_submit=iniciar_sesion,
    )

    # ======================================================
    # CAMPO CONTRASEÑA
    #
    # password=True oculta la contraseña.
    # can_reveal_password=True permite mostrar/ocultar
    # la contraseña desde el campo.
    # ======================================================

    txt_password = ft.TextField(
        label="Contraseña",
        password=True,
        can_reveal_password=True,
        width=320,
        height=56,
        border_color=COLOR_BORDER,
        focused_border_color=COLOR_PRIMARY,
        text_size=TEXT_SIZE,
        on_submit=iniciar_sesion,
    )

    # ======================================================
    # CONSTRUCCIÓN VISUAL DEL LOGIN
    #
    # Diseño:
    # - Fondo corporativo claro
    # - Tarjeta blanca centrada
    # - Logo circular
    # - Título de la aplicación
    # - Campos táctiles
    # - Botón principal grande
    # ======================================================

    return ft.View(
        route="/",
        bgcolor=COLOR_BACKGROUND,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER,

        controls=[

            # Tarjeta principal del login
            ft.Container(
                width=440,
                padding=32,
                bgcolor=COLOR_SURFACE,
                border_radius=CARD_RADIUS,

                # Borde suave para separar la tarjeta del fondo
                border=ft.Border(
                    left=ft.BorderSide(1, COLOR_BORDER),
                    top=ft.BorderSide(1, COLOR_BORDER),
                    right=ft.BorderSide(1, COLOR_BORDER),
                    bottom=ft.BorderSide(1, COLOR_BORDER),
                ),

                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=18,

                    controls=[

                        # Logo circular
                        ft.Container(
                            width=150,
                            height=150,
                            border_radius=100,

                            border=ft.Border(
                                left=ft.BorderSide(1, COLOR_PRIMARY_DARK),
                                top=ft.BorderSide(1, COLOR_PRIMARY_DARK),
                                right=ft.BorderSide(1, COLOR_PRIMARY_DARK),
                                bottom=ft.BorderSide(1, COLOR_PRIMARY_DARK),
                            ),

                            clip_behavior=ft.ClipBehavior.HARD_EDGE,

                            content=ft.Image(
                                src="logo.jpg",
                                width=150,
                                height=150,
                                fit="cover",
                            ),
                        ),

                        # Nombre del sistema
                        ft.Text(
                            "Capturador Destajos",
                            size=TITLE_SIZE,
                            weight=ft.FontWeight.BOLD,
                            color=COLOR_TEXT,
                            text_align=ft.TextAlign.CENTER,
                        ),

                        # Subtítulo explicativo
                        ft.Text(
                            "Acceso al sistema de nómina de obra",
                            size=SMALL_TEXT_SIZE,
                            color=COLOR_MUTED,
                            text_align=ft.TextAlign.CENTER,
                        ),

                        ft.Container(height=6),

                        # Campo usuario
                        txt_usuario,

                        # Campo contraseña
                        txt_password,

                        # Mensajes de error
                        mensaje,

                        # Botón principal
                        ft.ElevatedButton(
                            height=BUTTON_HEIGHT,
                            width=320,
                            bgcolor=COLOR_PRIMARY,
                            color="white",

                            content=ft.Text(
                                "Iniciar sesión",
                                size=TEXT_SIZE,
                                weight=ft.FontWeight.BOLD,
                            ),

                            on_click=iniciar_sesion,
                        ),
                    ],
                ),
            )
        ],
    )

#endregion
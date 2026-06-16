import flet as ft

from database_manager import validar_usuario
from views.obras_view import obras_view


# !! ==========================================================
# !! LOGIN_VIEW.PY
# !!
# !! Primera pantalla del sistema.
# !!
# !! Funciones principales:
# !! - Solicitar usuario
# !! - Solicitar contraseña
# !! - Validar acceso contra SQLite
# !! - Redirigir al listado de obras
# !!
# !! Flujo:
# !!
# !! main.py
# !!     ↓
# !! login_view.py
# !!     ↓
# !! validar_usuario()
# !!     ↓
# !! obras_view.py
# !!
# !! Esta vista NO consulta directamente SQLite.
# !! Utiliza database_manager.py para validar credenciales.
# !! ==========================================================


def login_view(page):

    # ! Campo para capturar usuario
    txt_usuario = ft.TextField(
        label="Usuario",
        width=300
    )

    # ! Campo para capturar contraseña
    # ! password=True oculta los caracteres
    txt_password = ft.TextField(
        label="Contraseña",
        password=True,
        width=300
    )

    # ! Etiqueta para mostrar errores
    # ! Ejemplo:
    # ! Usuario o contraseña incorrectos
    mensaje = ft.Text(
        "",
        color="red"
    )

    # !! ----------------------------------------------------------
    # !! iniciar_sesion()
    # !!
    # !! Se ejecuta cuando el usuario presiona:
    # !! [ Entrar ]
    # !!
    # !! Pasos:
    # !! 1. Leer usuario y contraseña
    # !! 2. Consultar SQLite
    # !! 3. Si son válidos:
    # !!       abrir obras_view
    # !! 4. Si son inválidos:
    # !!       mostrar mensaje de error
    # !! ----------------------------------------------------------
    def iniciar_sesion(e):

        usuario = txt_usuario.value.strip()
        password = txt_password.value.strip()

        # ! Consulta a SQLite mediante database_manager.py
        resultado = validar_usuario(
            usuario,
            password
        )

        # ! Credenciales correctas
        if resultado:

            # !! Limpiar vistas actuales
            page.views.clear()

            # !! Abrir listado de obras
            page.views.append(
                obras_view(page)
            )

            page.update()

        # ! Credenciales incorrectas
        else:

            mensaje.value = (
                "Usuario o contraseña incorrectos"
            )

            page.update()

    # !! ==========================================================
    # !! RETURN DE LA VISTA
    # !!
    # !! Construcción visual del Login
    # !!
    # !! Contiene:
    # !! - Logo
    # !! - Usuario
    # !! - Contraseña
    # !! - Mensajes de error
    # !! - Botón Entrar
    # !! ==========================================================
    return ft.View(
        route="/",

        controls=[

            # ! Separación superior
            ft.Container(height=30),

            # ! Logo principal
            ft.Image(
                src="logo.jpg",
                width=220
            ),

            # ! Nombre de la aplicación
            ft.Text(
                "CAPTURADOR DESTAJOS",
                size=28,
                weight=ft.FontWeight.BOLD
            ),

            # ! Usuario
            txt_usuario,

            # ! Contraseña
            txt_password,

            # ! Mensajes de error
            mensaje,

            # ! Botón de acceso
            ft.ElevatedButton(
                content=ft.Text("Entrar"),
                on_click=iniciar_sesion
            )

        ],

        # ! Centrar controles horizontalmente
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
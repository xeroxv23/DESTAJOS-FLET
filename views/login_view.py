import flet as ft

from database_manager import validar_usuario
from views.semanas_view import semanas_view

#region LOGINVIEW.PY
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
#endregion


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
#region INICIAR SESION
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
#endregion

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
                semanas_view(page)
            )

            page.update()

        # ! Credenciales incorrectas
        else:

            mensaje.value = (
                "Usuario o contraseña incorrectos"
            )

            page.update()

#region  RETURN DE LA VISTA 

    #  ==========================================================    

    #  Construcción visual del Login
    # 
    #  Contiene:
    #  - Logo
    #  - Usuario
    #  - Contraseña
    #  - Mensajes de error
    #  - Botón Entrar
    #  ==========================================================
#endregion

    return ft.View(
        route="/",
        # SI QUISIERAMOS CAMBIAR EL COLOR 
        #bgcolor="#3A4134",

        controls=[

            # ! Separación superior
            ft.Container(height=30),

            # ! Logo principal
            ft.Container(
                width=260,
                height=260,
                border_radius=220,

                border=ft.Border(
                    left=ft.BorderSide(0.5, "black"),
                    top=ft.BorderSide(0.5, "black"),
                    right=ft.BorderSide(0.5, "black"),
                    bottom=ft.BorderSide(0.5, "black"),
                ),

                clip_behavior=ft.ClipBehavior.HARD_EDGE,

                content=ft.Image(
                    src="logo.jpg",
                    width=220,
                    height=220,
                    fit="cover"
                )
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
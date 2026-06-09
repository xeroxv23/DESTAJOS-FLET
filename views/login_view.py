import flet as ft

from database_manager import validar_usuario
from views.obras_view import obras_view


def login_view(page):

    txt_usuario = ft.TextField(
        label="Usuario",
        width=300
    )

    txt_password = ft.TextField(
        label="Contraseña",
        password=True,
        width=300
    )

    mensaje = ft.Text(
        "",
        color="red"
    )

    def iniciar_sesion(e):

        usuario = txt_usuario.value.strip()
        password = txt_password.value.strip()

        resultado = validar_usuario(
            usuario,
            password
        )

        if resultado:

            page.views.clear()

            page.views.append(
                obras_view(page)
            )

            page.update()

        else:

            mensaje.value = (
                "Usuario o contraseña incorrectos"
            )

            page.update()

    return ft.View(
        route="/",
        controls=[

            ft.Container(height=30),

            ft.Image(
                src="logo.jpg",
                width=220
            ),

            ft.Text(
                "CAPTURADOR DESTAJOS",
                size=28,
                weight=ft.FontWeight.BOLD
            ),

            txt_usuario,

            txt_password,

            mensaje,

            ft.ElevatedButton(
                content=ft.Text("Entrar"),
                on_click=iniciar_sesion
            )

        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
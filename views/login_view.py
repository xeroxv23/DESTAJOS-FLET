import flet as ft


def login_view(page):

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

            ft.TextField(
                label="Usuario",
                width=300
            ),

            ft.TextField(
                label="Contraseña",
                password=True,
                width=300
            ),

            ft.ElevatedButton(
                content=ft.Text("Entrar")
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
import flet as ft

def vacaciones_view(page):

    def buscar_vacaciones(e):
        codigo = txt_consulta_vacaciones.value

        if not codigo:
            page.snack_bar = ft.SnackBar(ft.Text("Ingresa un número de nómina"))
            page.snack_bar.open = True
            page.update()
            return

        page.snack_bar = ft.SnackBar(
            ft.Text(f"Buscando vacaciones para nómina: {codigo}")
        )
        page.snack_bar.open = True
        page.update()

    txt_consulta_vacaciones = ft.TextField(
        label="Número de nómina del trabajador",
        hint_text="Ej. 10245",
        width=320,
        keyboard_type=ft.KeyboardType.NUMBER,
        text_align=ft.TextAlign.CENTER
    )

    return ft.View(
        route="/",
        controls=[
            ft.Container(height=30),

            ft.Image(
                src="logo.jpg",
                width=180
            ),

            ft.Container(height=10),

            ft.Text(
                "CONSULTA DE VACACIONES",
                size=24,
                weight=ft.FontWeight.BOLD
            ),

            ft.Text(
                "Introduce el numero de nomina del trabajador que necesitas consultar",
                size=12,
            ),

            ft.Container(height=20),

            txt_consulta_vacaciones,

            ft.Container(height=15),

            ft.ElevatedButton(
                content=ft.Text("Consultar"),
                on_click=buscar_vacaciones
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
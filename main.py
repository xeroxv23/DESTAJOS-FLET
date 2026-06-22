import flet as ft

from views.login_view import login_view

#region  MAIN.PY
    # !! ==========================================================
    # !! MAIN.PY
    # !!
    # !! Archivo principal de arranque de la aplicación.
    # !!
    # !! Responsabilidades:
    # !! - Inicializar Flet.
    # !! - Configurar la ventana principal.
    # !! - Cargar la primera vista del sistema.
    # !! - Definir carpeta de assets.
    # !!
    # !! Este archivo NO debe contener lógica de negocio.
    # !! No debe consultar SQLite.
    # !! No debe capturar destajos.
    # !!
    # !! Solo debe encargarse del arranque general.
    # !! ==========================================================
#endregion

#region !! FLUJO GENERAL DE LA APLICACION
    # !! ==========================================================
    # !!
    # !! Login
    # !!   ↓
    # !! Listado de Obras
    # !!   ↓
    # !! Obra Seleccionada
    # !!   ↓
    # !! Captura de Destajos
    # !!   ↓
    # !! Exportar Obra
    # !!
    # !! ==========================================================
#endregion

def main(page: ft.Page):

    # ! Título de la ventana de la aplicación.
    page.title = "Capturador Destajos"

    page.theme_mode = ft.ThemeMode.DARK

    # !! ----------------------------------------------------------
    # !! CONFIGURACION PARA DESARROLLO EN PC
    # !!
    # !! Este tamaño permite trabajar cómodamente
    # !! durante el desarrollo en Windows.
    # !!
    # !! Más adelante, para tablet, se puede cambiar
    # !! a pantalla completa o maximizada.
    # !! ----------------------------------------------------------
    page.window.width = 1200
    page.window.height = 800

    # ! Margen general interno de toda la aplicación.
    page.padding = 20

    # !! ----------------------------------------------------------
    # !! CONFIGURACION FUTURA PARA TABLET
    # !!
    # !! Cuando la aplicación sea desplegada
    # !! en tablets Android, revisar estas opciones:
    # !!
    # !! page.window.maximized = True
    # !!
    # !! o
    # !!
    # !! page.window.full_screen = True
    # !!
    # !! Nota:
    # !! La compatibilidad puede depender del método
    # !! final de empaquetado de Flet.
    # !! ----------------------------------------------------------

    # !! ----------------------------------------------------------
    # !! VISTA INICIAL
    # !!
    # !! La aplicación siempre inicia en Login.
    # !!
    # !! login_view.py se encargará de:
    # !! - Mostrar campos usuario/contraseña.
    # !! - Validar credenciales.
    # !! - Redirigir a obras_view.py.
    # !! ----------------------------------------------------------
    page.views.append(
        login_view(page)
    )

    # ! Refresca la ventana después de agregar la vista inicial.
    page.update()


# !! ==========================================================
# !! ARRANQUE DE FLET
# !!
# !! ft.run() ejecuta la aplicación.
# !!
# !! assets_dir="assets" indica que los archivos gráficos
# !! se buscarán dentro de la carpeta assets.
# !!
# !! Ejemplo:
# !! assets/logo.jpg
# !!
# !! En las vistas se usa:
# !! ft.Image(src="logo.jpg")
# !! ==========================================================
ft.run(
    main,
    assets_dir="assets"
)
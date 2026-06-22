from services.persistencia_json import cargar_captura
from export.excel_exporter import exportar_prueba_encabezado


semana = {
    "numero": 25,
    "fecha_inicio": "15/06/26",
    "fecha_fin": "21/06/26"
}

captura = cargar_captura(
    semana,
    "C-004"
)

if not captura:

    print("No existe captura JSON para esa obra")
    print("Ruta esperada:")
    print("capturas/semana_25/C-004.json")

else:

    ruta = exportar_prueba_encabezado(
        captura
    )

    print("Archivo generado:")
    print(ruta)
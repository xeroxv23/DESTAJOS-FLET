from database_manager import listar_conceptos

for concepto in listar_conceptos()[:5]:
    print(concepto)
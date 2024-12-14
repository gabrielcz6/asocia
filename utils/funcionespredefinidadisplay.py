def obtener_descripcion_puntaje(j):
    j+=1
    if j == 1:
        return "Insuficiente"
    elif j == 2:
        return "Básico"
    elif j == 3:
        return "Aceptable"
    elif j == 4:
        return "Bueno"
    elif j == 5:
        return "Excelente"
    else:
        return "Valor fuera de rango"  # En caso de que j no sea 1-5
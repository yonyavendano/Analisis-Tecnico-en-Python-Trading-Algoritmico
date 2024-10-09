# -*- coding: utf-8 -*-
# Importar librerías
import yfinance as yf
import json
# Librerías Propias
from config.config import activos

# Umbral de correlación (correlaciones menores a este valaor serán consideradas bajas)
umbral = 0.5

# Almacenar los activos con baja correlación para cada activo por tipo
resultados_correlacion = {}

# Iterar sobre cada tipo de activo
for tipo, lista_activos in activos.items():
    print(f"Analizando: {tipo}")
    
    # Descargar los datos históricos
    datos = yf.download(lista_activos, period="1y")["Close"]
    
    # Calcular la matriz de correlación
    correlacion = datos.corr()
    
    # Diccionario para almacenar los activos con baja corelación
    baja_correlacion_activos = {}
    
    for col in correlacion.columns:
        baja_correlacion = []
        for index in correlacion.index:
            if index != col and abs(correlacion.loc[index, col]) < umbral:
                baja_correlacion.append(index)
        # Guardar los activos con baja correlación para el activo actual
        baja_correlacion_activos[col] = baja_correlacion
    
    resultados_correlacion[tipo] = baja_correlacion_activos
    
# Mostrar los resultados de baja correlación por tipo de activo
for tipo, activos_correlacion in resultados_correlacion.items():
    print("#" * 10, f"{tipo.capitalize()} - Activos con baja correlación", "#" * 10, "\n")
    for activo, correlaciones in activos_correlacion.items():
        if len(correlaciones) > 0:
            print(f"\n{activo}:\n")
            print(json.dumps(correlaciones, indent=4))
        else:
            print(f"\n\n{activo}: No hay activos con baja correlación para este activo")
    print("\n\n")
    

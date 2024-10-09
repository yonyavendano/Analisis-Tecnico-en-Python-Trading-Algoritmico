# -*- coding: utf-8 -*-
# Importar librerías
import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# Descargar datos históricos para diferentes activos
tickers = ["AAPL", "MSFT", "GOOGL", "TSLA", "NFLX", "NVDA", "AMD", "PYPL"]
start_date = "2023-01-01"
end_date = "2024-01-01"

# Crear un diccionario vacío para almacenar los datos
datos = {}

for ticker in tickers:
    df = yf.download(ticker, start=start_date, end=end_date, interval="1d")
    datos[ticker] = df
    
# Crear un DataFrame para almacenar los resultados
resultados = pd.DataFrame(index=tickers)

# Calcular los retornos y las volatilidades para cada activo
for ticker in tickers:
    datos_ticker = datos[ticker]["Close"]
    
    # Calcular los retornos diarios
    retornos_diarios = datos_ticker.pct_change().dropna()
    
    volatilidad_diaria = np.std(retornos_diarios, ddof=1)
    volatilidad_anual = volatilidad_diaria * np.sqrt(252) # Volatilidad Anualizada
    
    promedio_diario = retornos_diarios.mean()
    promedio_anual = promedio_diario * 252 # Retorno Anualizado
    
    # Alamcenar resultados
    resultados.loc[ticker, "Volatilidad Diaria"] = volatilidad_diaria
    resultados.loc[ticker, "Volatilidad Anual"] = volatilidad_anual
    resultados.loc[ticker, "Retorno Diario"] = promedio_diario
    resultados.loc[ticker, "Retorno Anual"] = promedio_anual
    
# Crear un gráfico para visualizar las desviaciones estándar
fig, ax = plt.subplots(figsize=(22, 14))

barras = ax.bar(resultados.index, resultados["Volatilidad Anual"], color=["blue", "green", "red", "orange", "purple",
                                                                          "brown", "pink", "gray"])   
for barra, retorno_anual in zip(barras, resultados["Retorno Anual"]):
    altura = barra.get_height()
    ax.text(barra.get_x() + barra.get_width() / 2, altura, f"{retorno_anual:.2%}", ha="center",
            va = "bottom", fontsize=15, weight="bold")
    
ax.set_xlabel("Acciones/Insturmentos", fontsize=14)
ax.set_ylabel("Volatilidad Anual de los Rendimientos", fontsize=14)
ax.set_title("Comparación de la Desviación Estándar de los Precios con Retornos Anuales", fontsize=16, weight="bold")
ax.grid()

plt.show()
    
# Recordatorio:
#   - La desviación estándar de los rendimientos mide la volatilidad de un activo, indicando cómo varían sus rendimientos
#     respecto a su promedio. Alta desviación significa mayor riesgo e incertidumbre.
#   - En la gestión de riesgo, controlar la desviación estándar ayuda a evaluar la estabilidad de un activo y ajustar las
#     estrategias de inversión para minimizar las pérdidas y optimizar el rendimiento.

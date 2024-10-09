# -*- coding: utf-8 -*-
# Importar librerías
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Configuración de parámetros
ticker = "TSLA"
fecha_inicial = "2023-01-01"
fecha_final = "2024-01-01"

# Descargar datos
datos = yf.download(ticker, start=fecha_inicial, end=fecha_final, interval="1d")

# Calcular el Rendimiento Simple
datos["Rendimiento_Simple"] = datos["Close"].pct_change() # datos["Close"] / datos["Close"].shift(periods=1) - 1

# Calcular el Rendimiento Logarítmico
datos["Rendimiento_Logarítmico"] = np.log(datos["Close"] / datos["Close"].shift(periods=1))

# Mostar los primeros registros
print("Datos con Rendimiento Simple y Logarítmico:")
print(datos[["Rendimiento_Simple", "Rendimiento_Logarítmico"]].head())

# Graficas
plt.figure(figsize=(14, 7))

# Gráfica de Rendimientos Simples
plt.subplot(2, 1, 1)
plt.plot(datos.index, datos["Rendimiento_Simple"], label="Rendimiento Simple", color="blue")
plt.xlabel("Fecha")
plt.ylabel("Rendimiento Simple")
plt.title("Rendimiento Simple")
plt.legend()

# Gráfica de Rendimiento Logarítmico
plt.subplot(2, 1, 2)
plt.plot(datos.index, datos["Rendimiento_Logarítmico"], label="Rendimiento Logarítmico", color="green")
plt.xlabel("Fecha")
plt.ylabel("Rendimiento Logarítmico")
plt.title("Rendimiento Logarítmico")
plt.legend()

plt.tight_layout()
plt.show()

# Comparar la relevancia de cada rendimiento
rendimiento_simple_promedio_anualizado = datos["Rendimiento_Simple"].mean() * datos.dropna().shape[0]
rendimiento_logaritmico_promedio_anualizado = np.exp(datos["Rendimiento_Logarítmico"].mean() * datos.dropna().shape[0]) - 1
print("Rendimiento Simple Anualizado:", rendimiento_simple_promedio_anualizado)
print("Rendimiento Logarítmico Anualizado:", rendimiento_logaritmico_promedio_anualizado)

print("Rendimiento Real:", datos["Close"].iloc[-1] / datos["Close"].iloc[0] - 1)

# Escenario Hipotético
precios_accion = pd.DataFrame(data=[100, 20, 40, 80], index=[0, 1, 2, 3], columns=["Precios"])
rendimiento_simple = precios_accion.pct_change().mean()
rendimiento_logaritmico = np.exp(np.log(precios_accion / precios_accion.shift(periods=1)).mean() * (precios_accion.shape[0] - 1)) - 1
print("Rendimiento Simple Erróneo:", rendimiento_simple)
print("Rendimiento Logarítmico Correcto:", rendimiento_logaritmico)

# Recordatorio:
#   - Rendimiento Simple:
#       * Es la tasa de cambio porcentual en el precio de cierre de un activo de un día al siguiente.
#       * Es fácil de interpretar y comúnmente utilizado en informes financieros.
#       * No es aditivo a lo largo del tiempo, lo que puede complicar el análisis a largo plazo y llevar a conclusiones erróneas.
#   - Rendimiento Logarítmico:
#       * Es la diferencia logarítmica entre el precio de cierre de un activo de un día al siguiente.
#       * Es aditivo a lo largo del tiempo, lo que facilita el análisis de rendimientos acumulados y la modelización de series temporales.
#       * A menudo es preferido en análisis cuantitativo y financiero debido a sus propiedades matemáticas.

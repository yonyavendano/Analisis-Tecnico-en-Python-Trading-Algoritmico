# -*- coding: utf-8 -*-
# Importar librerías
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

# Definir Acción
ticker = "AMZN"

# Descargar datos
datos = yf.download(ticker, start="2023-01-01", end="2024-01-01", interval="1d")

# Calcular el Rendimiento Simple
datos["Rendimiento_Simple"] = datos["Close"].pct_change()

# Calcular el Rendimiento Logarítmico
datos["Rendimiento_Logarítmico"] = np.log(datos["Close"] / datos["Close"].shift(periods=1))

# Calcular el Rendimiento Simple Acumulado
datos["Rendimiento_Simple_Acumulado"] = (1 + datos["Rendimiento_Simple"]).cumprod() - 1

# Calcular el Rendimiento Logarítmico Acumulado
datos["Rendimiento_Logarítmico_Acumulado"] = np.exp(datos["Rendimiento_Logarítmico"].cumsum()) - 1

# Mostrar los primeros registros
print("Datos con Rendimiento Simple y Logarítmico Acumulado:")
print(datos[["Rendimiento_Simple_Acumulado", "Rendimiento_Logarítmico_Acumulado"]].head())

# Gráficas
plt.figure(figsize=(14, 7))

# Gráfica de Rendimiento Simple Acumulado
plt.subplot(2, 1, 1)
plt.plot(datos.index, datos["Rendimiento_Simple_Acumulado"], label="Rendimiento Simple Acumulado", color="blue")
plt.xlabel("Fecha")
plt.ylabel("Rendimiento Acumulado")
plt.title("Rendimiento Simple Acumulado")
plt.legend()

# Gráfica de Rendimiento Logarítmico Acumulado
plt.subplot(2, 1, 2)
plt.plot(datos.index, datos["Rendimiento_Logarítmico_Acumulado"], label="Rendimiento Logarítmico Acumulado", color="green")
plt.xlabel("Fecha")
plt.ylabel("Rendimiento Acumulado")
plt.title("Rendimiento Logarítmico Acumulado")
plt.legend()

plt.tight_layout()
plt.show()

# Recordatorio:
#   - El Rendimiento Acumulado representa el crecimiento total de una inversión a lo largo de un periodo.
#     Calculado a partir del rendimiento diario compuesto, nos permite observar como se ha acumulado el rendimiento total,
#     considerando los efectos de la capitalización de los rendimientos diarios a lo largo del tiempo.

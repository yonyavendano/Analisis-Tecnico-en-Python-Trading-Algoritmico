# -*- coding: utf-8 -*-
# Importar librerías
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns # pip install seaborn
import mplfinance as mpf # pip install mplfinance
import plotly.graph_objects as go # pip install plotly
import webbrowser

# Parámetros de Descarga
ticker = "AMZN"
fecha_inicial = "2023-01-01"
fecha_final = "2024-01-01"

# Descargar datos
datos = yf.download(ticker, start=fecha_inicial, end=fecha_final, interval="1d")

# Gráfico 1: Precio de Cierre usando matplotlib
plt.figure(figsize=(12, 6))
plt.plot(datos.index, datos["Close"], label="Precio de Cierre", color="blue")
plt.xlabel("Fecha")
plt.ylabel("Precio de Cierre")
plt.title("Precio de Cierre:" + ticker)
plt.legend()
plt.grid(True)
plt.show()

# Gráfico 2: Subplots para el Precio de Cierre, Bajo, Alto y Apertura
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(22, 12))

# Precio de Cierre
axes[0, 0].plot(datos.index, datos["Close"], color="blue")
axes[0, 0].set_title("Precio de Cierre")
axes[0, 0].set_ylabel("Precio")
axes[0, 0].grid()

# Precio Bajo
axes[0, 1].plot(datos.index, datos["Low"], color="red")
axes[0, 1].set_title("Precio Bajo")
axes[0, 1].set_ylabel("Precio")
axes[0, 1].grid()

# Precio Alto
axes[1, 0].plot(datos.index, datos["High"], color="green")
axes[1, 0].set_title("Precio Alto")
axes[1, 0].set_ylabel("Precio")
axes[1, 0].grid()

# Precio de Apertura
axes[1, 1].plot(datos.index, datos["Open"], color="purple")
axes[1, 1].set_title("Precio de Apertura")
axes[1, 1].set_ylabel("Precio")
axes[1, 1].grid()

plt.tight_layout()
plt.show()

# Gráfico 3: Rendimientos usando Seaborn
datos["Rendimiento_Simple"] = datos["Close"].pct_change()
datos.dropna(inplace=True)

plt.figure(figsize=(12, 6))
sns.lineplot(x=datos.index, y=datos["Rendimiento_Simple"], color="orange")
plt.xlabel("Fecha")
plt.ylabel("Rendimiento Simple")
plt.title("Rendimiento Simple Para el Activo")
plt.grid(True)
plt.show()

# Gráfico 4: Gráfico de velas usando mplfinance
mpf.plot(datos, type="candle", style="yahoo", title="Gráfico de Velas", ylabel="Precio", volume=True, figsize=(22, 10),
         figscale=3.0, mav=(9, 21))
plt.show()

# Gráfico 5: Gráfico de Velas usando Plotly
fig = go.Figure(data=[
    go.Candlestick(x=datos.index,
                   open=datos["Open"],
                   high=datos["High"],
                   low=datos["Low"],
                   close=datos["Close"])
    ])

fig.update_layout(
    title="Gráfico de Velas con Plotly",
    xaxis_title="Fecha",
    yaxis_title="Precio",
    width=1500, # Ancho en píxeles
    height=700  # Altura en píxeles
    )

# Guardar el gráfico en un archivo HTML
fig.write_html("grafico_velas_plotly.html")

# Opcional: Abrir automáticamente el plot en nuestro navegador predeterminado
webbrowser.open("grafico_velas_plotly.html")

# Recordatorio:
#   - El uso de herramientas visuales nos ayuda a ver patrones y entender los datos de manera más clara y rápida.

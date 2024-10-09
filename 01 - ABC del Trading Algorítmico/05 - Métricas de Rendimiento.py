# -*- coding: utf-8 -*-
# Importar librerías
import yfinance as yf
import matplotlib.pyplot as plt
import statsmodels.api as sm # pip install statsmodels
from datetime import timedelta

# Parámetros de Descarga
ticker = "TSLA"
benchmark_ticker = "^GSPC" # Ticker del índice de referencia (S&P500)
fecha_inicial = "2020-01-01"
fecha_final = "2024-01-01"

# Descargar datos
datos = yf.download(ticker, start=fecha_inicial, end=fecha_final, interval="1d")
benchmark = yf.download(benchmark_ticker, start=fecha_inicial, end=fecha_final, interval="1d")

# Calcular los rendimientos diarios
datos["Rendimiento"] = datos["Close"].pct_change()
benchmark["Rendimiento"] = benchmark["Close"].pct_change()
datos.dropna(inplace=True)
benchmark.dropna(inplace=True)

# Calcular la Máxima Pérdida (Max Drawdown)
def max_drawdown(rendimientos):
    
    """
    Calcula la máxima pérdida de una serie de rendimientos
    """
    
    # Calcular
    capital_acumulado = (1 + rendimientos).cumprod()
    maximo_acumulado = capital_acumulado.cummax()
    drawdown = (maximo_acumulado - capital_acumulado) / maximo_acumulado
    maxima_perdida_valor = drawdown.max()
    
    # Encontrar el punto más alto y el punto más bajo del drawdown
    fecha_final = drawdown.idxmax()
    fecha_maxima = capital_acumulado[:fecha_final].idxmax()
    
    return maxima_perdida_valor, capital_acumulado, drawdown, fecha_maxima, fecha_final

maxima_perdida_accion, capital_acumulado, drawdown, fecha_maxima, fecha_final = max_drawdown(datos["Rendimiento"])
print(f"Máxima Pérdida de {ticker}: {maxima_perdida_accion:.2%}")

# Comentario explicativo
print(f"""
La Máxima Pérdida es la mayor pérdida desde un punto alto hasta un punto bajo durante el periodo analizado.
En este caso, la Máxima Pérdida del ticker: {ticker} es {maxima_perdida_accion:.2%}.
Esto indica la mayor caída en el valor de la acción desde un máxima histórico durante el periodo de estudio.
      """)
      
# Gráficar la Máxima Pérdida
plt.figure(figsize=(22, 8))
plt.plot(datos.index, capital_acumulado, label="Rendimiento Acumulado", color="blue")
plt.plot(datos.index, capital_acumulado - drawdown * capital_acumulado, label="Drawdown", color="red", linestyle="--")

# Resaltar el área de Máxima Pérdida desde el punto más alto hasta el más bajo
plt.fill_between(x=datos.index, y1=capital_acumulado, y2=capital_acumulado - drawdown * capital_acumulado,
                 where=((datos.index >= fecha_maxima) & (datos.index <= fecha_final)), color="red",
                 alpha=0.3, label="Área de Máxima Pérdida")

# Añadir flechas horizontales para indicar el inicio y el fin de la Máxima Pérdida
plt.annotate("Inicio del Drawdown", xy=(fecha_maxima, capital_acumulado.loc[fecha_maxima]),
             xytext=(fecha_final + timedelta(days=55), capital_acumulado.loc[fecha_maxima] * 1.01),
             arrowprops=dict(facecolor="black", arrowstyle="->", connectionstyle="arc3,rad=0.1", lw=3),
             fontsize=15, color="black")

plt.annotate("Fin del Drawdown", xy=(fecha_final, capital_acumulado.loc[fecha_final]),
             xytext=(fecha_final + timedelta(days=25), capital_acumulado.loc[fecha_final] * 0.40),
             arrowprops=dict(facecolor="black", arrowstyle="->", connectionstyle="arc3,rad=0.1", lw=3),
             fontsize=15, color="black")

plt.xlabel("Fecha", size=20)
plt.ylabel("Valor", size=20)
plt.title("Capital Acumulado y Máxima Pérdida", size=20)
plt.legend()
plt.grid(True)
plt.show()

# Calcular Alpha y Beta
X = sm.add_constant(benchmark["Rendimiento"])
y = datos["Rendimiento"]

# Ajustar el modelo de Regresión
modelo = sm.OLS(y, X).fit()

# Extraer Alpha y Beta
alpha = modelo.params["const"] * 252 # Anualizar el Alpha
beta = modelo.params["Rendimiento"] 

print(f"Alpha de {ticker}: {alpha:.2%}")
print(f"Beta de {ticker}: {beta:.2%}")

# Comentario Explicativo
print(f"""
El Alpha de {ticker} es {alpha:.2%}. Esto indica el rendimiento adicional que la acción ha generado en comparación con el 
rendimiento esperado basado en su riesgo relativo del mercado.
Un Alpha positivo sugiere que la acción ha superado las expectativas dadas según sus características de riesgo.

El Beta de {ticker} es {beta:.2%}. Esto mide la volatilidad de la acción en relación con el índice de referencia.
Una Beta mayor a 1 indica que la acción es más volátil que el mercado, mientras que una Beta menor a 1 indica que es menos volátil.
      """)
      
# Graficar los rendimientos acumulados
plt.figure(figsize=(22, 8))
plt.plot(datos.index, (1 + datos["Rendimiento"]).cumprod(), label=f"Rendimiento Acumulado de {ticker}", color="blue", lw=2)
plt.plot(benchmark.index, (1 + benchmark["Rendimiento"]).cumprod(), label=f"Rendimiento Acumulado {benchmark_ticker}", color="orange", linestyle="--", lw=3)
plt.xlabel("Fecha")
plt.ylabel("Rendimiento Acumulado")
plt.title("Rendimiento Acumulado Comparativo")
plt.legend()
plt.grid(True)
plt.show()

# Recordatorio:
#   - Máxima Pérdida (Max DrawDown):
#       * Mide la mayor pérdida desde un punto alto hasta un punto bajo durante un período.
#       * Ayuda a evaluar el riesgo y la profundidad de las caídas en el capital.
#   - Alpha:
#       * Representa el rendimiento adicional de una inversión en comparación con el índice de referencia.
#       * Un alpha positivo indica un rendimiento superior al esperado según el riesgo asumido.
#   - Beta:
#       * Mide la volatilidad o el riesgo sistemático de una inversión en relación con el índice de referencia.
#       * Un beta mayor a 1 indica que la inversión es más volátil que el índice, mientras que un beta menor a 
#         1 indica menor volatilidad.

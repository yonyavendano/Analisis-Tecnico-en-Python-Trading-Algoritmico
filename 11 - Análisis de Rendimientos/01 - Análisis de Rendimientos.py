# -*- coding: utf-8 -*-
# Importar librerías
import yfinance as yf
import seaborn as sns
import matplotlib.pyplot as plt

# Definir tickers
tickers = ["SPY", "MSFT", "AAPL"]

# Crear una figura con varios subplots
fig, axes = plt.subplot_mosaic("ABC;DDD", figsize=(35, 18), height_ratios=(3, 2), dpi=100)

axes_list = list(axes.keys())

# Iterar y graficar cada activo
precios = {}
for i, ticker in enumerate(tickers):
    # Descargar los datos históricos de cada activo
    df = yf.download(ticker, start="2015-01-01", end="2024-01-01", interval="1d")
    precios[ticker] = df
    precios[ticker]["Rendimiento"] = df["Close"].pct_change()
    precios[ticker]["Retorno Acumulado"] = (1 + precios[ticker]["Rendimiento"]).cumprod()
    
    # Calcular los retornos mensuales
    retornos_mensuales = precios[ticker]["Rendimiento"].resample("M").sum()
    
    # Crear una tabla pivote con los retornos mensuales
    retornos_mensuales = retornos_mensuales.to_frame()
    retornos_mensuales["Año"] = retornos_mensuales.index.year
    retornos_mensuales["Mes"] = retornos_mensuales.index.strftime("%b")
    
    tabla_pivote = retornos_mensuales.pivot(index="Año", columns="Mes", values="Rendimiento")
    
    # Ordenar los meses para que aparezcan en orden cronológico
    meses_orden = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    tabla_pivote = tabla_pivote[meses_orden]
    
    # Crear el mapa de calor en el subplot correspondiente
    heatmap = sns.heatmap(tabla_pivote, cmap="RdYlGn", annot=True, annot_kws={"size": 13}, fmt=".1%", 
                          cbar_kws={"label": "Retornos Mensuales (%)"}, ax=axes[axes_list[i]], vmin=-0.10, vmax=0.10)
    axes[axes_list[i]].set_title(f"{ticker} Retornos Mensuales (%)", fontsize=18)
    axes[axes_list[i]].set_xlabel("Mes", fontsize=18)
    axes[axes_list[i]].set_ylabel("Año", fontsize=18)
    axes[axes_list[i]].grid()
    
    # Ajustar el tamaño del texto de la etiqueta de la barra de color
    cbar = heatmap.collections[0].colorbar
    cbar.set_label("Retornos Mensuales (%)", fontsize=14)
    # Ajustar el tamaño del texto de los ejes
    heatmap.set_xticklabels(heatmap.get_xticklabels(), fontsize=14)
    heatmap.set_yticklabels(heatmap.get_yticklabels(), fontsize=14)
    
    # Graficar los Retornos Acumulados
    precios[ticker]["Retorno Acumulado"].plot(ax=axes["D"], label=ticker)

axes["D"].set_xticklabels(axes["D"].get_xticklabels(), fontsize=16)    
axes["D"].set_yticklabels(axes["D"].get_yticklabels(), fontsize=16)
axes["D"].grid(lw=3)

plt.suptitle("\nAnálisis de Rendimientos por Meses\n", fontsize=20, fontweight="bold")
plt.legend(loc="upper left", fontsize=15)
plt.title("Rendimiento de Instrumentos Financieros", size=18)
plt.ylabel("Rendimiento", size=18)
plt.tight_layout()
plt.show()    
    
# Recordatorio:
#   - Considerar el contexto del mercado: Asegúrate de tener en cuenta el contexto general del mercado al analizar los rendimientos
#     mensuales. Un mes con un rendimiento positivo para un activo puede ser resultado del comportamiento general del mercado, no solo
#     de las características individuales de cada activo.
#   - Revisar Estacionalidades: Identifica patrones estacionales y tendencias en los rendimientos de los activos. Algunos meses
#     pueden mostrar un rendimiento consistentemente alto o bajo, lo cual puede influir en tus decisiones de inversión.
#   - Optimización de Estrategias: Utiliza la información sobre el comportamiento estacional para ajustar tus estrategias de inversión.
#     Aprovecha los meses con tendencias positivas para tomar posiciones largas y sé cauteloso en meses con tendencias negativas,
#     adaptando tus decisiones a las condiciones de mercado.

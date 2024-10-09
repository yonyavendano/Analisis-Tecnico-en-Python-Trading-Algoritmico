# -*- coding: utf-8 -*-
# Importar librerías
import investpy # pip install investpy 
import yfinance as yf
import pandas as pd
import time
import seaborn as sns
import matplotlib.pyplot as plt

# Obtener la lista de acciones en Investing
stocks = investpy.stocks.get_stocks()
print("Total de Instrumentos Financieros (Acciones):", stocks.shape[0])
print("Total de Países Diferentes:", stocks["country"].drop_duplicates().shape[0])

# Filtrar por país (USA)
stocks_usa = stocks[stocks["country"] == "united states"].reset_index(drop=True).drop_duplicates()
print("Total de Instrumentos:", stocks_usa.shape[0])

# Crear una lista para almacenar la información del sector
stocks_sectors = []
# Crear una instancia para obtener la información
tickers = yf.Tickers(stocks_usa["symbol"].tolist())

# Obtener el sector para cada ticker utilizando yfinance
contador = 0 
for ticker, yfinance_ticker_object in tickers.tickers.items():
    try: 
        info = yfinance_ticker_object.info
        sector = info.get("sector", "Unknown")
        stocks_sectors.append((ticker, sector))
        if (contador + 1) % 100 == 0:
            print(f"Total de Activos Descargados: {contador + 1}/{stocks_usa.shape[0]}")
    except Exception as error:
        print("No se pudo descargar para el activo:", ticker)
        print("Con error ->", error)
        
    time.sleep(0.10)
    contador += 1
    
# Convertir la información a un DataFrame para mejor visualización
sectors_df = pd.DataFrame(stocks_sectors, columns=["Ticker", "Sector"])
print(sectors_df)

# Guardar
stocks_usa.merge(right=sectors_df, left_on="symbol", right_on="Ticker").drop(columns=["Ticker"]).to_csv("../datos/sectores.csv")

# Agrupar por sector para mantener los 4 sectores más altos
sectors_df = sectors_df[sectors_df["Sector"] != "Unknown"]
sectors_df_top = sectors_df.groupby(["Sector"]).count().sort_values(by="Ticker", ascending=False).head(4)
print(sectors_df_top)
print(f"Análisis con {sectors_df_top.sum().iloc[0]} activos diferentes")

# Mantener activos
sectors_df = sectors_df[sectors_df["Sector"].isin(sectors_df_top.index)]

# Descargar datos
tablas_pivotes = {}
retornos_acumulados = {}
for i in sectors_df_top.index:
    tickers_sector = sectors_df[sectors_df["Sector"] == i]["Ticker"].tolist()
    precios = yf.download(tickers_sector, start="2015-01-01", end="2025-01-01", interval="1d")
    # Eliminar tickers sin información completa
    precios = precios["Close"].dropna(axis=1)
    # Calcular los rendimientos
    rendimiento = precios.pct_change()
    # Promediar por filas
    retorno_final = rendimiento.mean(axis=1)
    # Retorno acumulado
    retorno_acumulado = (1 + retorno_final).cumprod() - 1
    retornos_acumulados[i] = retorno_acumulado
    # Calcular los retornos mensuales
    retornos_mensuales = retorno_final.resample("M").sum()
    # Tabla Pivote con retornos mensuales
    retornos_mensuales = retornos_mensuales.to_frame(name=i)
    retornos_mensuales["Year"] = retornos_mensuales.index.year
    retornos_mensuales["Month"] = retornos_mensuales.index.strftime("%b")
    pivot_table = retornos_mensuales.pivot(index="Year", columns="Month", values=i)
    meses_orden = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    pivot_table = pivot_table[meses_orden]
    tablas_pivotes[i] = pivot_table
    
# Generar Plots Visuales
fig, axes = plt.subplot_mosaic("AB;CD;EE", figsize=(32, 16))
    
for sector, subplot in zip(tablas_pivotes, axes.values()):
    # Crear el mapa de calor en el subplot correspondiente
    heatmap = sns.heatmap(tablas_pivotes[sector], cmap="RdYlGn", annot=True, annot_kws={"size": 13}, fmt=".1%", 
                          cbar_kws={"label": "Retornos Mensuales (%)"}, ax=subplot, vmin=-0.10, vmax=0.10)
    subplot.set_title(f"{sector} Retornos Mensuales (%)", fontsize=18)
    subplot.set_xlabel("Mes", fontsize=18)
    subplot.set_ylabel("Año", fontsize=18)
    subplot.grid()
    
    # Ajustar el tamaño del texto de la etiqueta de la barra de color
    cbar = heatmap.collections[0].colorbar
    cbar.set_label("Retornos Mensuales (%)", fontsize=14)
    # Ajustar el tamaño del texto de los ejes
    heatmap.set_xticklabels(heatmap.get_xticklabels(), fontsize=14)
    heatmap.set_yticklabels(heatmap.get_yticklabels(), fontsize=14)
    
    # Graficar Retornos Acumulados
    retornos_acumulados[sector].plot(ax=axes["E"], label=sector)
    
axes["E"].set_xticklabels(axes["E"].get_xticklabels(), fontsize=16)    
axes["E"].set_yticklabels(axes["E"].get_yticklabels(), fontsize=16)
axes["E"].grid(lw=3)

plt.suptitle("\nAnálisis de Rendimientos por Meses\n", fontsize=20, fontweight="bold")
plt.legend(loc="upper left", fontsize=15)
plt.title("Rendimiento de Instrumentos Financieros", size=18)
plt.ylabel("Rendimiento", size=18)
plt.tight_layout()
plt.show()      
    
# Recordatorio:
#   - Dividir nuestro análisis por sectores nos puede ayudar a identificar patrones de comportamiento en su rendimiento en ciertos
#     meses del año.
#   - Se pueden ajustar diferentes estrategias de inversión en base al comportamiento estacional y las tendencias históricas de cada
#     sector.
#   - Identificar que sectores suelen liderar o rezagarse en diferentes etaás del ciclo económico puede ser clave para posicionarse
#     estratégicamente y aprovechar tendencias emergentes.

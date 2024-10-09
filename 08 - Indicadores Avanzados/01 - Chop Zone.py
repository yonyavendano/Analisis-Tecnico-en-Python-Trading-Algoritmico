# -*- coding: utf-8 -*-
# Importar librerías
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

# Indicador: Chop Zone
def Chop_Zone(df: pd.DataFrame, longitud: int = 30, longitud_ema: int = 34, columna: str = "Close") -> pd.Series:
    
    """
    El indicador Chop Zone (CZ) es una herramienta de análisis técnico que ayuda a identificar la fuerza y dirección
    de una tendencia en el mercado, utilizando un enfoque basado en el ángulo de la media móvil exponencial (EMA).
    Proporciona señales visuales para determinar si un mercado está en una tendencia fuerte (alcista o bajista) o en
    una fase de consolidación.
    
    Cómo Operarlo:
        
        El indicador Chop Zone es utilizadao para identificar la volatilidad y la fuerza de una tendencia en los mercados
        financieros. Se basa en el cálculo del ángulo de una EMA (Media Móvil Exponencial) en relación con el precio
        promedio ponderado del activo. Los valores resultantes del indicador están codificados en colores, lo que permite
        a los traders visualizar rápidamente la fortaleza o debilidad de la tendencia actual. Los colores fríos como el verde
        y el azul indican una tendencia alcista fuerte, mientras que los colores cálidos como el rojo y el naranja sugieren
        una tendencia bajista o un posible cambio de dirección.
        
    -----------
    Parámetros:
    -----------
    param : pd.DataFrame : df : Datos históricos del activo.
    -----------
    param : int : longitud : Ventana a ser usada en el cálculo de CZ (por defecto, se establece en 30).
    -----------
    param : int : longitud_ema : Ventana a ser utilizada en el cálculo del EMA para el CZ (por defecto, se establece en 34).
    -----------
    param : str : columna : Columna a usar en el cálculo del CZ (por defecto, se establece en 'Close').
    -----------
    Salida:
    -----------
    return : pd.Series : Cálculo del Chop Zone.
    """
    
    # Calcular precios típicos y rangos
    columna_precio = df[columna]
    TP = (df["High"] + df["Low"] + df["Close"]) / 3
    precio_suavizado = columna_precio.rolling(window = longitud, min_periods=longitud)
    max_suavizado = precio_suavizado.max()
    min_suavizado = precio_suavizado.min()
    rango_HL = 25 / (max_suavizado - min_suavizado) * min_suavizado
    
    # Calcular la EMA y el ángulo de la EMA
    ema = df[columna].ewm(span=longitud_ema, min_periods=longitud_ema, adjust=False).mean()
    x1_ema = 0
    x2_ema = 1
    y1_ema = 0
    y2_ema = (ema.shift(periods=1) - ema) / TP * rango_HL
    c_ema = np.sqrt((x2_ema - x1_ema) ** 2 + (y2_ema - y1_ema) ** 2)
    angulo_ema0 = round(np.rad2deg(np.arccos((x2_ema - x1_ema) / c_ema)))
    angulo_ema1 = np.where(y2_ema > 0, - angulo_ema0, angulo_ema0)[max(longitud, longitud_ema):]
    CZ = np.where(angulo_ema1 >= 5, 0,
         np.where((angulo_ema1 >= 3.57) & (angulo_ema1 < 5), 1,
         np.where((angulo_ema1 >= 2.14) & (angulo_ema1 < 3.57), 2,
         np.where((angulo_ema1 >= 0.71) & (angulo_ema1 < 2.14), 3,
         np.where(angulo_ema1 <= -5, 4,
         np.where((angulo_ema1 <= -3.57) & (angulo_ema1 > -5), 5,
         np.where((angulo_ema1 <= -2.14) & (angulo_ema1 > -3.57), 6,
         np.where((angulo_ema1 <= -0.71) & (angulo_ema1 > -2.14), 7, 8))))))))
    
    return pd.Series([np.nan] * max(longitud, longitud_ema) + CZ.tolist(), index=df.index, name="CZ")

# Obtener Datos
ticker = "AMZN"
df = yf.download(ticker, start="2022-01-01", end="2024-01-01", interval="1d")

# Calcular CZ
cz = Chop_Zone(df, longitud=30, longitud_ema=34, columna="Close").dropna()
    
# Graficar Indicador
fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(18, 10), sharex=True)

# Graficar Precio de Cierre
df["Close"].loc[cz.index].reset_index(drop=True).plot(ax=ax[0], xlabel="Fecha", ylabel="Precio", label="Precio de Cierre")
ax[0].set_title("Precio de Cierre", fontsize=20)
ax[0].grid()

# Colores para el Bar Plot
colores = {
    
    0: "#26C6DA", # Turquesa - Tendencia Alcista Fuerte
    1: "#43A047", # Verde Oscuro - Tendencia Alcista Moderada
    2: "#A5D6A7", # Verde Claro - Tendencia Alcista Leve
    3: "#009688", # Lima - Tendencia Alcista Débil 
    4: "#D50000", # Rojo Oscuro - Tendencia Bajista Fuerte
    5: "#E91E63", # Rojo - Tendencia Bajista Moderada
    6: "#FF6D00", # Naranja - Tendencia Bajista Leve
    7: "#FFB74D", # Naranja Claro - Tendencia Bajista Débil
    8: "#FDD835"  # Amarillo - Tendencia Neutral o sin Dirección Clara
    
    }

# Generar Barras de Colores
for i in range(0, cz.shape[0], 1):
    ax[1].bar(i, 1, color=colores[int(cz[i])])
    
ax[1].set_title("Indicador Chop Zona", fontsize=20)
ax[1].set_xticks(ticks=range(0, cz.shape[0], 10), labels=cz.index[0::10], rotation=75, fontsize=8)

plt.tight_layout()
plt.show()
 
# Recordatorio:
#   - El CZ te ayuda a visualizar la fuerza y dirección de una tendencia utilizando una escala de colores, facilitando la interpretación.
#   - Cambios rápidos en los colores del indicador pueden alertarte sobre posibles reversiones de tendencia.
#   - CZ tiene algunas limitaciones, como la falta de sensibilidad a cambios rápidos en el mercado, pero esto se puede arreglar
#     ajustando los parámetros del indicador.

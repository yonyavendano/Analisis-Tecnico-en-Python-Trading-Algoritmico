# -*- coding: utf-8 -*-
# Importar librerías
import pandas as pd
import numpy as np
import yfinance as yf
import mplfinance as mpf
import matplotlib.pyplot as plt

# Indicador: Índice de Fuerza Relativa (RSI)
def Indicador_Fuerza_Relativa(df: pd.DataFrame, longitud: int = 14, columna: str = "Close") -> pd.Series:

    """
    El Índice de Fuerza Relativa (RSI) es un indicador utilizado en el análisis técnico que mide la magnitud de los 
    cambios recientes en los precios para evaluar condiciones de sobrecompra o sobreventa en el precio de una acción
    u otro activo.
    
    Cómo Operarlo:
        
        La interpretación y uso tradicionales del RSI indican que valores de 70 o más sugieren que un activo está 
        sobrecomprado o sobrevalorado y podrían estar listo para una reversión de tendencia o una corrección de precio.
        Una lectura de RSI de 30 o menos indican una condición de sobreventa o infravalorada.
        
    -----------
    Parámetros:
    -----------
    param : int : longitud : Ventana a usar en el cálculo del RSI (por defecto, se establece en 14).
    -----------
    param : str : columna : Columna a utilizar en el cálculo del RSI (por defecto, se establece en 'Close').
    -----------
    Salida:
    -----------
    return : pd.Series : Cálculo del Índice de Fuerza Relativa (RSI).
    """
    
    # Calcular
    Delta = df[columna].diff(periods=1)
    Ganancia = Delta.where(Delta >= 0, 0)
    Perdida = np.abs(Delta.where(Delta < 0, 0))
    # Valores en la posición de la longitud
    media_ganancia = Ganancia.ewm(span=longitud, min_periods=longitud, adjust=False).mean()
    media_perdida = Perdida.ewm(span=longitud, min_periods=longitud, adjust=False).mean()
    RS = media_ganancia / media_perdida
    RSI = pd.Series(np.where(RS == 0, 100, 100 - (100 / (1 + RS))), name="RSI", index=df.index)
    
    return RSI

# Descargar Datos
ticker = "NVDA"
df = yf.download(ticker, start="2021-01-01", end="2024-01-01", interval="1d")

# Calcular RSI
rsi = Indicador_Fuerza_Relativa(df)

# Niveles de sobrecompra y sobreventa
sobrecomprayventa = [
    
    mpf.make_addplot([70] * len(rsi), panel=2, color="gray", linestyle="--"),
    mpf.make_addplot([30] * len(rsi), panel=2, color="gray", linestyle="--")
    
    ]

ap = [
      
      mpf.make_addplot(rsi, panel=2, color="blue", ylabel="RSI")
      
      ] + sobrecomprayventa

mpf.plot(df, type="candle", style="yahoo", volume=True, addplot=ap, title="Índice de Fuerza Relativa (RSI)",
         ylabel="Precio del Activo", ylabel_lower="Volumen", figsize=(22, 10), figscale=3.0, warn_too_much_data=df.shape[0])

plt.show()

# Recordatorio:
#   - El RSI es un indicador de impulso que mide la magnitud de los cambios en los precios para evaluar condiciones de sobrecompra o sobreventa.
#   - Valores de RSI de 70 o más sugieren que el activo pordía estar sobrecomprado, mientras que valores de 30 o menos indican sobreventa.
#   - Las líneas discontinuas en gris representan los niveles críticos de sobrecompra y sobreventa. Cuando el RSI cruza estas líneas,
#     puede ser un indicio de una posible reversión en la tendencia.
#   - El RSI se utiliza para identificar posibles puntos de entrada o salida en el mercado basado en estas condiciones extremas.

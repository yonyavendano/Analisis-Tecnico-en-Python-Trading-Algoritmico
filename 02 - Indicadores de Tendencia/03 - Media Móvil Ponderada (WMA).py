# -*- coding: utf-8 -*-
# Importar librerías
import pandas as pd
import numpy as np
import yfinance as yf
import mplfinance as mpf
import matplotlib.pyplot as plt

# Indicador: Media Móvil Ponderada (WMA)
def Media_Movil_Ponderada(df: pd.DataFrame, longitud: int = 9, columna: str = "Close") -> pd.Series:
    
    """
    La Media Móvil Ponderada (WMA) es un indicador técnico que asigna un mayor peso a los puntos de datos más recientes,
    ya que son más relevantes que los puntos de datos en el pasado lejano. La suma de los pesos debe sumar 1. En el caso
    de la SMA, los pesos están distribuidos por igual.
    
    Cómo operarlo:
        
        Las Medias Móviles Ponderadas de 9 y 12 días son a menudo las más citadas y analizadas como promedios a corto plazo.
        La WMA se opera de la misma manera que la SMA. La principal diferencia entre estas dos es la importancia que la WMA
        da a los datos más recientes.
        
    ----------    
    Parámetros
    ----------
    param : pd.DataFrame : df : Datos históricos del activo financiero.
    ----------
    param : int : longitud : Ventana a utilizar en el cálculo de la WMA (por defecto, se establece en 9).
    ----------
    param : str : columna : Columna a utilizar en el cálculo de la WMA (por defecto, se establece en 'Close').
    ----------
    Salida:
    ----------
    return : pd.Series : Cálculo de la Media Móvil Ponderada.
    """
    
    # Calcular
    df = df[columna]
    pesos = np.arange(1, longitud + 1) / np.arange(1, longitud + 1).sum()
    func = lambda x: np.sum(pesos * x)
    WMA = df.rolling(window=longitud, min_periods=longitud).apply(func, raw=True)
    WMA.name = "WMA"
    
    return WMA

# Obtener Datos
df = yf.download("META", start="2023-01-01", end="2025-07-01", interval="1d", multi_level_index=False)

# Calcular Indicador
wma_9 = Media_Movil_Ponderada(df, longitud=9, columna="Close")
wma_12 = Media_Movil_Ponderada(df, longitud=12, columna="Close")

# Graficar
wma_plots = [
    
    mpf.make_addplot(wma_9, label="WMA 9 días", color="purple", type="line"),
    mpf.make_addplot(wma_12, label="WMA 12 días", color="red", type="line")
    
    ]

mpf.plot(df, type="candle", style="yahoo", volume=True, figsize=(22, 10), addplot=wma_plots, figscale=4.0,
         title="Medias Móviles Ponderadas")
plt.show()

# Recordatorio:
#   - La Media Móvil Ponderada (WMA) da más peso a los precios recientes, lo que la hace más sensible a los cambios recientes
#     en el precio.
#   - Las WMA comunes son las de 9 y 12 periodos. La WMA se utiliza para identificar la tendencia y generar señales de compra o venta.
#   - La WMA se puede operar de manera similar a la SMA, pero es más reactiva a los cambios recientes en el precio.
#   - Para evitar malas interpretaciones, es útil usar la WMA en combinación con otra WMA de diferente longitud.

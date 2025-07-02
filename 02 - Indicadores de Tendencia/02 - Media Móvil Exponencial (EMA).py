# -*- coding: utf-8 -*-
# Importar librerías
import pandas as pd
import yfinance as yf
import mplfinance as mpf
import matplotlib.pyplot as plt

# Indicador: Media Móvil Exponencial (EMA)
def Media_Movil_Exponencial(df: pd.DataFrame, longitud: int = 26, columna: str = "Close") -> pd.Series:
    
    """
    La Media Móvil Exponencial (EMA) es un indicador técnico que rastrea el precio de un activo (como una acción o una mercancía)
    a lo largo del tiempo. La EMA es un tipo de media móvil ponderada (WMA) que otorga más peso o importancia a los datos
    de precios recientes.
    
    Cómo Operarlo:
        
        Las Medias Móviles Exponenciales de 12 y 26 días son a menudo las más citadas y analizadas como promedios a corto plazo.
        La EMA se opera de la misma manera que la SMA. La principal diferencia entre estas dos es la importancia que la EMA da a 
        los datos más recientes.
        
    ----------
    Parámetros
    ----------
    param : pd.DataFrame : df : Datos Históricos del activo.
    ----------
    param : int : longitud : Ventana a utilizar en el cálculo de la EMA (por defecto, se establece en 26).
    ----------
    param : str : columna : Columna a utilizar en el cálculo de la EMA (por defecto, se establece en 'Close').
    ----------
    Salida:
    ----------
    return : pd.Series : Cálculo de la Media Móvil Exponencial.
    """
    
    # Calcular
    df = df[columna]
    EMA = df.ewm(span=longitud, min_periods=longitud, adjust=False).mean()
    EMA.name = "EMA"
    
    return EMA

# Descargar los datos
df = yf.download("GOOGL", start="2025-01-01", end="2025-07-01", interval="1d", multi_level_index=False)

# Calcular Indicador
ema_12 = Media_Movil_Exponencial(df, longitud=12, columna="Close")
ema_26 = Media_Movil_Exponencial(df, longitud=26, columna="Close")

# Graficar
ema_plots = [
    
    mpf.make_addplot(ema_12, label="EMA 12 Días", color="green", type="line"),
    mpf.make_addplot(ema_26, label="EMA 26 Días", color="blue", type="line")
    
    ]

mpf.plot(df, type="candle", style="yahoo", volume=True, figsize=(22, 10), addplot=ema_plots, figscale=3.0,
         title="Medias Móviles Exponenciales")
plt.show()

# Recordatorio:
#   - La Media Móvil Exponencial (EMA) da más peso a los precios recientes, lo que la hace más sensible a los cambios recientes en el precio.
#   - Las EMAs comunes son las de 12 y 26 días. La EMA se utiliza para identificar la tendencia y generar señales de compra o venta.
#   - La EMA se puede operar de manera similar a la SMA, pero es más reactiva a los cambios recientes en el precio.
#   - Para evitar malas interpretaciones, es útil usar la EMA en combinación con otra EMA de diferente longitud.

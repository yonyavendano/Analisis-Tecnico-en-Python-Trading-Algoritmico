# -*- coding: utf-8 -*-
# Importar librerías
import pandas as pd
import yfinance as yf
import mplfinance as mpf
import matplotlib.pyplot as plt

# Indicador: Media Móvil Simple (SMA)
def Media_Movil_Simple(df: pd.DataFrame, longitud: int = 21, columna: str = "Close") -> pd.Series:

#  """
#    La Media Móvil Simple (SMA o MA) se utiliza comúnmente para identificar la dirección de la tendencia de una acción o para 
#   determinar sus niveles de soporte y resistencia. Es un indicador de seguimiento de tendencia -o rezagado- porque se basa en 
#    precios pasados.
#   
#   Cuanto más largo es el periodo de la media móvil, mayor es el rezago. Así que una SMA de 200 días tendrá un mayor grado de 
#   rezago que una SMA de 20 días porque contiene precios de los últimos 200 días.
   
#   Cómo Operarlo:
        
#        Dado que la SMA se utiliza como niveles de Soporte y Resistencia, la operación básica es comprar cerca del soporte en
#        tendencias alcistas y vender cerca de las resistencias en tendencias bajistas.
        
#       Operar con solo una SMA puede llevar a malas interpretaciones, y puede ser peligroso. Por eso, operar con SMAs requerirá
#        una media móvil rápida y una lenta. Si la MA rápida cruza de abajo hacia arriba a la MA lenta, esto indica una oportunidad
#        de compra. Si la MA rápida cruza de arriba hacia abajo a la MA lenta, esto indica una oportunidad de venta.
        
#    ----------
#    Parámetros
#    ----------
#    param : pd.DataFrame : df : Datos Históricos.
#    ----------
#    param : int : longitud : Ventana a utilizar en el cálculo de la SMA (por defecto, se establece en 21).
#    ----------
#    param : str : columna : Columna a utilizar en el cálculo de la SMA (por defecto, se establece en 'Close').
#    ----------
#    Salida:
#    ----------
#    """
    
    """
    La Media Móvil Simple (SMA o MA) se utiliza comúnmente para identificar la dirección de la tendencia de una acción o para 
    determinar sus niveles de soporte y resistencia. Es un indicador de seguimiento de tendencia -o rezagado- porque se basa en 
    precios pasados.
    
    Cuanto más largo es el periodo de la media móvil, mayor es el rezago. Así que una SMA de 200 días tendrá un mayor grado de 
    rezago que una SMA de 20 días porque contiene precios de los últimos 200 días.
    
    Cómo Operarlo:
        
        Dado que la SMA se utiliza como niveles de Soporte y Resistencia, la operación básica es comprar cerca del soporte en
        tendencias alcistas y vender cerca de las resistencias en tendencias bajistas.
        
        Operar con solo una SMA puede llevar a malas interpretaciones, y puede ser peligroso. Por eso, operar con SMAs requerirá
        una media móvil rápida y una lenta. Si la MA rápida cruza de abajo hacia arriba a la MA lenta, esto indica una oportunidad
        de compra. Si la MA rápida cruza de arriba hacia abajo a la MA lenta, esto indica una oportunidad de venta.
        
    ----------
    Parámetros
    ----------
    param : pd.DataFrame : df : Datos Históricos.
    ----------
    param : int : longitud : Ventana a utilizar en el cálculo de la SMA (por defecto, se establece en 21).
    ----------
    param : str : columna : Columna a utilizar en el cálculo de la SMA (por defecto, se establece en 'Close').
    ----------
    Salida:
    ----------
    return : pd.Series : Cálculo de la Media Móvil Simple.
    """
    
    # Calcular
    df = df[columna]
    MA = df.rolling(window=longitud, min_periods=longitud).mean()
    MA.name = "MA"
    
    return MA
    
# Obtener Datos
df = yf.download("NFLX", start="2023-01-01", end="2024-01-01", interval="1d") 

# Calcular Indicador
media_mov_9 = Media_Movil_Simple(df, longitud=9, columna="Close")
media_mov_21 = Media_Movil_Simple(df, longitud=21, columna="Close")    

# Graficar
media_mov_plots = [
    
    mpf.make_addplot(media_mov_9, label="Media Móvil 9 días", color="green", type="line"),
    mpf.make_addplot(media_mov_21, label="Media Móvil 21 días", color="blue", type="line")
    
    ]
    
mpf.plot(df, type="candle", style="yahoo", volume=True, figsize=(22, 10), addplot=media_mov_plots, figscale=3.0,
         title=dict(title="Promedios Móviles", size=20)) 
plt.show()   
    
# Recordatorio:
#   - La Media Móvil Simple (SMA) es útil para identificar tendenciasa y niveles de Soporte y Resistencia.
#   - Un periodo más largo en la SMA indica un mayor rezago en nuestro indicador.
#   - Operar con una SMA sola puede llevar a malas interpretaciones; por lo tanto, se recomienda utilizarla en conjunto
#     con otra SMA para obtener señales de compra o venta más precisas.

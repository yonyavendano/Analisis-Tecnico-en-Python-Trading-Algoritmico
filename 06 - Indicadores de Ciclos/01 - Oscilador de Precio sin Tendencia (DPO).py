# -*- coding: utf-8 -*-
# Importar librerías
import pandas as pd
import yfinance as yf
import mplfinance as mpf
import matplotlib.pyplot as plt

# Indicador: Oscilador de Precio Detrended
def Oscilador_Precio_Detrended(df: pd.DataFrame, longitud: int = 20, centrar: bool = False, columna: str = "Close") -> pd.Series:
    
    """
    El Oscilador de Precios Detrended (DPO) es un indicador técnico que elimina las tendencias de precios con el fin de estimar la
    longitud de los ciclos de precios de pico a pico o de valle a valle.
    
    A diferencia de otros osciladores, como el Estócastico o el MACD, el DPO no es un indicador de Momentum. En cambio, resalta los 
    picos y los valles en el precio, que se utilizan para estimar puntos de compra y venta en línea con el ciclo histórico.
    
    Cómo Operarlo:
        
        El DPO busca ayudar a un trader a identificar el ciclo de precios de un activo. Lo hace comparando un SMA con un precio histórico
        que está cerca del medio del período de retroceso. Al observar los picos y valles históricos en el indicador que se alinearon con
        los picos y valles en el precio, los traders típicamente dibujan líneas verticales en estos puntos y luego cuentan cuánto tiempo
        transcurrió entre ellos.
        
        Si los valles están separados por dos meses, eso ayuda a evaluar cuándo puede llegar la próxima oportunidad de compra. Esto se
        hace aislando el valle más reciente en el indicador/precio y luego proyectando el próximo valle dos meses hacia adelante. Lo mismo
        se aplica a los picos.
        
    -----------
    Parámetros:
    -----------
    param : pd.DataFrame : df : Datos históricos.
    -----------
    param : int : longitud : Ventana a ser utilizada en el cálculo del DPO (por defecto, se establece en 20).
    -----------
    param : bool : centrar : Si es True, coloca las etiquetas en el centro de la ventana. Si es False, las etiquetas permanecen en su
                             posición original (por defecto, se establece en False).
    -----------
    param : str : columna : Columna a utilizar en el cálculo del DPO (por defecto, se establece en 'Close').
    -----------
    Salida:
    -----------
    return : pd.Series : Cálculo del Oscilador de Precios sin Tendencia.
    """
    
    # Calcular
    precio_col = df[columna]
    precio_rolling = precio_col.rolling(window=longitud, min_periods=longitud).mean()
    t = int((0.5 * longitud) + 1)
    if centrar:
        DPO = (precio_col.shift(periods=t) - precio_rolling).shift(periods=-t)
    else:
        DPO = precio_col - precio_rolling.shift(periods=t)
    DPO.name = "DPO"
    
    return DPO

# Descargar datos
ticker = "AAPL"
df = yf.download(ticker, start="2022-01-01", end="2024-01-01")
    
# Calcular al DPO
dpo_df = Oscilador_Precio_Detrended(df, longitud=20, centrar=False) 
    
# Crear plots adicionales
adplots = [
    
    mpf.make_addplot(dpo_df, color="gray", label="DPO", panel=2, ylabel="DPO"),
    mpf.make_addplot([20] * dpo_df.shape[0], color = "red", linestyle="--", panel=2),
    mpf.make_addplot([0] * dpo_df.shape[0], color = "red", linestyle="--", panel=2),
    mpf.make_addplot([-20] * dpo_df.shape[0], color = "red", linestyle="--", panel=2)
    
    ] 

fig, ax = mpf.plot(df, type="candle", style="charles", addplot=adplots, volume=True, returnfig=True, panel_ratios=(3, 1, 2), figsize=(22, 10))

ax[0].set_xlabel("Fecha", fontsize=14)
ax[0].set_ylabel("Precio", fontsize=14)
ax[0].set_title("Oscilador de Precio sin Tendencia")

plt.show()
    
# Recordatorio:
#   - El Oscilador de Precios Detrended (DPO) elimina las tendencias de precios para estimar la longitud de los ciclos.
#   - Se utiliza para identificar los picos y valles en el precio y estimar la longitud de los ciclos en los precios.
#   - Los picos y valles se deben de identificar de manera única para cada activo.

# -*- coding: utf-8 -*-
# Importar librerías
import pandas as pd
import numpy as np
import yfinance as yf
import mplfinance as mpf
import matplotlib.pyplot as plt

# Indicador: SuperTendencia
def SuperTendencia(df: pd.DataFrame, longitud: int = 14, factor: float = 3.0) -> pd.DataFrame:
    
    """
    SuperTendencia es un indicador de seguimiento de tendencias que dibuja una línea en el gráfico de velas para ayudar a identificar
    la dirección predominante del mercado. La línea cambia de color según la tendencia actual: una línea roja por encima de las velas
    señala una tendencia bajista, mientras que una línea verde debajo de las velas indica una tendencia alcista. Estas líneas también
    actúan como niveles de soporte y resistencia; la línea verde puede servir como un nivel de soporte durante una tendencia alcista,
    y la línea roja puede funcionar como resistencia durante una tendencia bajista.
    
    Cómo Operarlo:
        
        La forma más sencilla de operar con el indicador de SuperTendencia es seguir las señales de cambio de tendencia que proporciona.
        Compra cuando la línea es verde, lo que indica una tendencia alcista, y vende cuando la línea es roja, reflejando una tendencia
        bajista. Este indicador es frecuentemente usado en combinación con otras herramientas técnicas para una estrategia de trading
        más robusta. Una estrategia popular es combinar SuperTendencia con el Índice de Fuerza Relativa (RSI). Si la línea de
        SuperTendencia cambia de verde a rojo y el RSI cruza por debajo del nivel 50, podrías considerar abrir una posición corta. De
        manera inversa, si la línea de SuperTendencia cambia de roja a verde y el RSI cruza por encima del nivel de 50, podrías abrir
        una posición larga. Esta combinación te ayuda a confirmar las señales de SuperTendencia y mejorar la precisión de tus decisiones
        en el trading.
        
    -----------
    Parámetros:
    -----------
    param : pd.DataFrame : df : Datos del activo.
    -----------
    param : int : longitud : Ventana a utilizar en el cálculo de ST (por defecto, se establece en 14).
    -----------
    param : float : factor : Multiplicador de cálculo de ATR (por defecto, se establece en 3.0).
    -----------
    Salida:
    -----------
    return : pd.DataFrame : Cálculo de SuperTendencia.
    """
    
    # Calcular ATR
    High, Low = df["High"], df["Low"]
    H_minus_L = High - Low
    prev_cl = df["Close"].shift(periods=1)
    H_minus_PC = abs(High - prev_cl)
    L_minus_PC = abs(prev_cl - Low)
    TR = pd.Series(np.max([H_minus_L, H_minus_PC, L_minus_PC], axis=0), index=df.index, name="TR")
    ATR = TR.ewm(alpha=1/longitud, min_periods=longitud, adjust=False).mean()
    
    # Calcular Bandas
    medio = (df["High"] + df["Low"]) / 2
    FinalUpperB = medio + factor * ATR # Banda Superior para indicar una tendencia alcista
    FinalLowerB = medio - factor * ATR # Banda Inferior para indicar una tendencia bajista
    
    # Inicializar SuperTendencia
    ST = np.zeros(ATR.shape[0])
    close = df["Close"].values
    
    # Iterar
    for i in range(1, ATR.shape[0]):
        # Calcular SuperTendencia para cada punto
        if close[i] > FinalUpperB[i - 1]:
            ST[i] = True
        elif close[i] < FinalLowerB[i - 1]:
            ST[i] = False
        else:
            ST[i] = ST[i - 1]
            # Ajustar las bandas finales para reflejar la dirección de la tendencia
            if ST[i] == True and FinalLowerB[i] < FinalLowerB[i - 1]:
                FinalLowerB[i] = FinalLowerB[i - 1]
            elif ST[i] == False and FinalUpperB[i] > FinalUpperB[i - 1]:
                FinalUpperB[i] = FinalUpperB[i - 1]
                
        # Eliminar bandas según la dirección de la tendencia
        if ST[i] == True:
            FinalUpperB[i] = np.nan
        else:
            FinalLowerB[i] = np.nan
            
    # Ajustar el valor inicial para evitar valores no deseados en la primera posición
    if ST[1] == 0:
        FinalLowerB[0] = np.nan
    else:
        FinalUpperB[0] = np.nan
        
    # Eliminar valores no deseados y ajustar los arrays de las bandas
    FU = FinalUpperB[longitud -1:]
    FL = FinalLowerB[longitud - 1:]
    ST_df = pd.concat([FU, FL], axis=1)
    ST_array = np.nansum([FU, FL], axis=0)
    ST_array[0] = np.nan
    ST_df["SuperTendencia"] = ST_array
    ST_df.columns = ["FinalUpperB", "FinalLowerB", "SuperTendencia"]
    
    return ST_df

# Obtener Datos
ticker = "AMZN"
df = yf.download(ticker, start="2022-01-01", end="2024-01-01")
            
# Calcular Indicador
st = SuperTendencia(df)          
            
# Generar plots adicionales
st_plots = [
    
    mpf.make_addplot(st["SuperTendencia"], color="black", label="Cambio de Tendencia"),
    mpf.make_addplot(st["FinalUpperB"], color="red", label="Tendencia Bajista"),
    mpf.make_addplot(st["FinalLowerB"], color="green", label="Tendencia Alcista")
    
    ]          
            
mpf.plot(df[-st.shape[0]:], type="candle", style="yahoo", volume=True, figsize=(22, 10), addplot=st_plots, figscale=3.0,
         title="Super Tendencia")
plt.show()         
            
# Recordatorio:
#   - El indicador de SuperTendencia nos ayuda a identificar la dirección predominante del mercado mediante el trazado de líneas
#     de soporte y resistencia.

# -*- coding: utf-8 -*-
# Importar librerías
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Indicador: Ciclo de Tendencia de Schaff
def Ciclo_Tendencia_Schaff(df: pd.DataFrame, longitud_rapida: int = 23, longitud_lenta: int = 50, ciclo: int = 10, suavizado: int = 3,
                           suavizado2: int = 3, columna: str = "Close") -> pd.Series:
    
    """
    El Ciclo de Tendencia Schaff es un indicador oscilador cíclico. Se basa en la suposición de que las tendencias de las divisas
    se aceleran y desaceleran en un patrón cíclico. El STC es relevante como una señal temprana para detectar tendencias en las 
    divisas, proporcionando una línea de señal mejorada.
    
    Cómo Operarlo:
        
        Hay 2 umbrales presentes, 25 y 75. Cuando el indicador cruza por encima de la línea de 25, se observa una tendencia alcista.
        Cuando el indicador cruza por debajo de la línea de 75, comienza una tendencia bajista. Una vez que el indicador está entre
        las líneas de 25 y 75, significa que la tendencia se está desarrollando en una de las dos direcciones. Además, esos niveles
        pueden usarse como áreas de sobrecompra y sobreventa.
        
        Una forma de evitar señales falsas es agregar una SMA de 50 períodos. Si el STC está en una tendencia alcista pero los precios
        aún están por debajo de la línea SMA, espere a que el precio cruce de abajo hacia arriba la línea SMA. Por el contrario, si el
        STC está en una tendencia bajista pero los precios aún están por encima de la línea SMA, espere a que el precio cruce de arriba
        hacia abajo la línea SMA.
        
    -----------
    Parámetros:
    -----------
    param : pd.DataFrame : df : Datos del instrumento/activo financiero.
    -----------
    param : int : longitud_rapida : Ventana rápida a utilizar en el cálculo del STC (por defecto, se establece en 23).
    -----------
    param : int : longitud_lenta : Ventana lenta a utilizar en el cálculo del STC (por defecto, se establece en 50).
    -----------
    param : int : ciclo : Ventana cíclica a utilizar en el cálculo del STC (por defecto, se establece en 10).
    -----------
    param : int : suavizado : Ventana suavizada No. 1 a utilizar en el cálculo del STC (por defecto, se establece en 3).
    -----------
    param : int : suavizado2 : Ventana suavizada No. 2 a utilizar en el cálculo del STC (por defecto, se establece en 3).
    -----------
    param : str : columna : Columna a utilizar en el cálculo del STC (por defecto, se establece en 'Close').
    -----------
    Salida:
    -----------
    return : pd.Series : Cálculo del Ciclo de Tendencia Schaff.
    """
    
    # Calcular EMAs
    EMA1 = df[columna].ewm(span=longitud_rapida, min_periods=longitud_rapida, adjust=False).mean()
    EMA2 = df[columna].ewm(span=longitud_lenta, min_periods=longitud_lenta, adjust=False).mean()
    
    # MACD
    MACD = EMA1 - EMA2
    # Máximo y mínimo del MACD
    rodante = MACD.rolling(window=ciclo, min_periods=ciclo)
    MACD_min = rodante.min()
    MACD_max = rodante.max()
    # Calcular el Estocástico %K
    Stoch_k = 100 * (MACD - MACD_min) / (MACD_max - MACD_min)
    
    # Calcular Stoch_d
    Stoch_d = Stoch_k.ewm(span=suavizado, min_periods=suavizado, adjust=False).mean()
    Stoch_d_min = Stoch_d.rolling(window=ciclo, min_periods=ciclo).min()
    Stoch_d_max = Stoch_d.rolling(window=ciclo, min_periods=ciclo).max()
    Stoch_kd = 100 * (Stoch_d - Stoch_d_min) / (Stoch_d_max - Stoch_d_min)
    
    # STC
    STC = Stoch_kd.ewm(span=suavizado2, min_periods=suavizado2, adjust=False).mean()
    STC = pd.Series([np.nan] * (df.shape[0] - STC.shape[0]) + STC.values.tolist(), index=df.index)
    STC.name = "STC"
    
    return STC

# Descargar datos
ticker = "SAN"
df = yf.download(ticker, start="2019-01-01", end="2024-01-01", interval="1d")
    
# Calcular el Indicador
stc = Ciclo_Tendencia_Schaff(df)  
    
# Crear subplots
fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(22, 10), sharex=True)

# Gráfico de Precios de Cierre
ax1.set_title("Gráfico de: " + ticker)
ax1.plot(df.index, df["Close"], color="blue", label = "Precio de Cierre")
ax1.set_ylabel("Precio")
ax1.legend()

# Rellenar áreas de sobrecompra en verde
for fecha_inicio in stc[stc >= 75].index:
    # Encontrar la fecha final para la área de sobrecompra que se quiere colorear
    fecha_final = (
        
        stc[stc.index > fecha_inicio][stc[stc.index > fecha_inicio] < 75].index.min()  # Fecha en la que STC baja de 75
        if len(stc[stc.index > fecha_inicio][stc[stc.index > fecha_inicio] < 75]) > 0
        else df.index[-1]
        
        )
    # Rellenar el área entre fecha_inicio y fecha_final con color verde
    ax1.axvspan(fecha_inicio, fecha_final, color="lightgreen", alpha=0.5)
    

# Rellenar áreas de sobreventa en rojo
for fecha_inicio in stc[stc <= 25].index:
    # Encontrar la fecha final para la área de sobreventa se quiere colorear
    fecha_final = (
        
        stc[stc.index > fecha_inicio][stc[stc.index > fecha_inicio] > 25].index.min()  # Fecha en la que STC sube de 25
        if len(stc[stc.index > fecha_inicio][stc[stc.index > fecha_inicio] > 25]) > 0
        else df.index[-1]
        
        )
    # Rellenar el área entre fecha_inicio y fecha_final con color coral
    ax1.axvspan(fecha_inicio, fecha_final, color="lightcoral", alpha=0.5)
    
# Gráfico del STC
ax2.plot(stc.index, stc, color="blue", label="STC")
ax2.axhline(y=75, color="black", linestyle="--", alpha=0.7)
ax2.axhline(y=25, color="black", linestyle="--", alpha=0.7)
ax2.set_ylabel("STC")

# Rellenar las áreas bajo la curva STC
ax2.fill_between(stc.index, stc, 75, where=(stc >= 75), color="green", alpha=0.3)
ax2.fill_between(stc.index, stc, 25, where=(stc <= 25), color="red", alpha=0.3)

plt.show()
    
# Recordatorio:
#   - El Ciclo de Tendencia de Schaff es un indicador cíclico que ayuda a detectar tendencias en los mercados.
#   - Los niveles de 25 y 75 actúan como zonas de sobrecompra y sobreventa, respectivamente.
#   - El STC debe de ser usado en combinación con otros indicadores y análisis para una toma de decisiones más completa.

# -*- coding: utf-8 -*-
# Importar librerías
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

# Indicador: Rango Promedio Verdadero (ATR)
def Rango_Promedio_Verdadero(df: pd.DataFrame, longitud: int = 14) -> pd.Series:
    
    """
    Rango Promedio Verdadero (ATR) es un indicador de análisis técnico que mide la volatilidad del mercado descomponiendo el rango 
    total del precio de un activo para ese período.
    
    Cómo Operarlo:
        
        ATR se usa comúnmente como un método de salida que se puede aplicar sin importar cómo se tome la decisión de entrada.
        Una técnica popular es conocida como la "salida de candelabro". Esta salida coloca un stop trailing por debajo del máximo
        más alto que el activo alcanzó desde que se realizó el comercio. La distancia entre el máximo más alto y el nivel de stop 
        se define como algunas veces el ATR. Por ejemplo, el valor de ATR puede restarse tres veces del máximo más alto desde
        el comercio actual.
        
        Recuerda que una mayor volatilidad generalmente significa un costo transaccional más bajo, por lo que el ATR puede ser una
        herramienta útil para agregar a un sistema de trading para mejorar las estrategias a corto plazo.
        
    -----------
    Parámetros:
    -----------
    param : pd.DataFrame : df : Datos históricos del activo.
    -----------
    param : int : longitud : Ventana a ser utilizada en el cálculo del ATR (por defecto, se establece en 14).
    -----------
    Salida:
    -----------
    return : pd.Series : Cálculo del ATR.
    """
    
    # Calcular TR
    High, Low = df["High"], df["Low"]
    H_minus_L = High - Low
    prev_cl = df["Close"].shift(periods=1)
    H_minus_pc = High - prev_cl
    L_minus_pc = abs(prev_cl - Low)
    TR = pd.Series(np.max([H_minus_L, H_minus_pc, L_minus_pc], axis=0), index=df.index, name="TR")
    # ATR
    ATR = TR.ewm(alpha=1/longitud, min_periods=longitud).mean()
    ATR.name = "ATR"
    
    return ATR

# Descargar datos históricos
ticker = "V"
df = yf.download(ticker, start="2022-01-01", end="2024-01-01")
    
# Calculo del Indicador
atr = Rango_Promedio_Verdadero(df, longitud=14)    
      
# Crear gráfico
fig, ax = plt.subplots(figsize=(22, 8))

# Graficar el Rango Promedio Verdadero
ax.plot(df.index, atr, color="darkblue", linestyle="--", linewidth=2, label="Rango Promedio Verdadero (ATR)")
ax.axhline(y=atr.mean(), color="gray", linestyle="--", linewidth=3.0, label="Promedio ATR")

ax.set_xlabel("Fecha", fontsize=14)
ax.set_ylabel("Valor del ATR", fontsize=14)
ax.set_title("Rango Promedio Verdadero de: " + ticker)
ax.legend(loc="upper right")
ax.grid()
plt.tight_layout()
plt.show()
    
# Recordatorio:
#   - El ATR mide la volatilidad del mercado descomponiendo el rango total del precio.
#   - Un ATR más alto indica mayor volatilidad, mientras que un ATR más bajo sugiere menor volatilidad.
#   - Es útil para ajustar niveles de stop loss y mejorar estrategias de gestión de riesgo.

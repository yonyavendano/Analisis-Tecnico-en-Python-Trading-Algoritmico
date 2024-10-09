# -*- coding: utf-8 -*-
# Importar librerías
import pandas as pd
import numpy as np
import yfinance as yf
import mplfinance as mpf
import matplotlib.pyplot as plt

# Indicador: Índice de Ulcer
def Ulcer_Index(df: pd.DataFrame, longitud: int = 14, columna: str = "Close") -> pd.Series:
    
    """
    El Índice de Ulcer (UI) es un indicador técnico que mide el riesgo a la baja en términos de la profundidad y duración de las caídas
    de precios. El Índice aumenta a medida que el precio se aleja de los máximos recientes y cae a medida que el precio sube a nuevos
    máximos. Cuanto mayor sea el valor del UI, más tiempo tardará una acción en volver al máximo anterior. En términos simples, es una
    medida de volatilidad en la baja.
    
    Cómo Operarlo:
        
        UI se utiliza generalmente como una medida de riesgo en varios contextos donde se usa la desviación estándar. Un UI promedio más 
        bajo significa un menor riesgo de drawdown en comparación con una inversión con un UI promedio más alto. Aplicar un MA al UI 
        mostrará que acciones y fondos tienen menor volatilidad en general.
        
        Observar picos en el UI que están más allá de lo "normal" también se puede usar para indicar tiempos de riesgo excesivo a la baja,
        lo que los inversores pueden desear evitar saliendo de posiciones largas.
        
    -----------
    Parámetros:
    -----------
    param : pd.DataFrame : df : Datos históricos.
    -----------
    param : int : longitud : Ventana para el cálculo del UI (por defecto, se establece en 14).
    -----------
    param : str : columna : Columna a utilizar en el cálculo del UI (por defecto, se establece en 'Close').
    -----------
    Salida:
    -----------
    return : pd.Series : Cálculo del Índice de Ulcer.
    """
    
    # Calcular
    precio_col = df[columna]
    rolling_max = precio_col.rolling(window=longitud, min_periods=longitud).max()
    Perc_Drawdown = ((precio_col - rolling_max) / rolling_max) * 100
    sqrt_func = lambda x: np.sqrt((x ** 2).mean())
    UI = Perc_Drawdown.rolling(window=longitud, min_periods=longitud).apply(sqrt_func, raw=True)
    UI.name = "UI"
    
    return UI

# Obtener Datos
ticker = "AAPL"
df = yf.download(ticker, start="2022-01-01", end="2024-01-01")

# Calcular Indicador
ui_df = Ulcer_Index(df, longitud=14)
    
# Crear el gráfico
ap = [
      
      mpf.make_addplot(ui_df, color="blue", label="UI", panel=2, ylabel="UI"),
      mpf.make_addplot([5] * len(ui_df), color="red", panel=2, linestyle="--")
      
      ] 

fig, ax = mpf.plot(df, type="candle", style="charles", addplot=ap, volume=True, returnfig=True)

fig.set_size_inches(22, 8)

ax[0].set_xlabel("Fecha", fontsize=14)
ax[0].set_ylabel("Precios", fontsize=14)
ax[0].set_title("Índice de Ulcer para: " + ticker, fontsize=16, weight="bold")

plt.show()
    
# Recordatorio:
#   - El Índice de Ulcer mide el riesgo a la baja en términos de la profundidad y duración de las caídas en los precios.
#   - Un valor más alto del UI indica mayor volatilidad a la baja y mayor riesgo de drawdown.
#   - Un valor más bajo del UI sugiere una menor volatilidad a la baja y menor riesgo.

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
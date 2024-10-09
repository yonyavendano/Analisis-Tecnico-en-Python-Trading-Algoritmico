# -*- coding: utf-8 -*-
# Importar librerías
import pandas as pd
import numpy as np
import yfinance as yf
import mplfinance as mpf
import matplotlib.pyplot as plt

# Indicador: SAR Parabólico
def Parabolic_SAR(df: pd.DataFrame, incremento: float = 0.02, max_paso: float = 0.20) -> pd.DataFrame:
    
    """
    El indicador Parabolic SAR (Stop and Reverse) se usa para determinar la dirección de la tendencia y posibles
    reversales en el precio. El SAR Parabólico utiliza un método de stop y reversa para identificar puntos adecuados
    de entrada y salida.
    
    Cómo Operarlo:
        
        El PSAR genera señales de compra o venta cuando la posición de los puntos se mueve de un lado del precio del activo
        al otro. Por ejemplo, una señal de compra ocurre cuando los puntos se mueven de arriba del precio a abajo del precio,
        mientras que una señal de venta ocurre cuando los puntos se mueven de abajo del precio a arriba del precio.
        
        Los puntos del PSAR se utilizan para establecer órdenes de stop loss en tendencia. Si el precio está subiendo y el PSAR
        también está subiendo, el PSAR puede usarse como una posible salida si estás en una posición larga. Si el precio cae por
        debajo del PSAR, sal de la operación larga.
        
    -----------
    Parámetros:
    -----------
    param : pd.DataFrame : df : Datos del activo.
    -----------
    param : float : incremento : Incremento máximo a utilizar en el cálculo del Parabolic SAR (por defecto, se establece en 0.02).
    -----------
    param : float : max_paso : Paso máximo a utilizar en el cálculo del Parabolic SAR (por defecto, se establece en 0.20).
    -----------
    Salida:
    -----------
    return : pd.DataFrame : Cálculo del SAR Parabólico.
    """
    
    # Calcular
    data = df.copy()
    High, Low, Close = data["High"].values, data["Low"].values, data["Close"].values
    psar_up, psar_down = np.repeat(np.nan, Close.shape[0]), np.repeat(np.nan, Close.shape[0])
    
    # Inicializar variables
    up_trend = True
    up_trend_high = High[0]
    down_trend_low = Low[0]
    acc_factor = incremento
    
    # Iterar sobre los precios para calcular el PSAR
    for i in range(2, Close.shape[0]):
        reversal = False 
        max_high = High[i]
        min_low = Low[i]
        
        # Tendencia Alcista
        if up_trend:
            # Calcular el PSAR para la tendencia alcista
            Close[i] = Close[i - 1] + (acc_factor * (up_trend_high - Close[i - 1]))
            if min_low < Close[i]: # Verificar si hay reversión a tendencia bajista
                reversal = True
                Close[i] = up_trend_high 
                down_trend_low = min_low
                acc_factor = incremento 
            else:
                if max_high > up_trend_high: # Actualizar el máximo en tendencia alcista
                    up_trend_high = max_high
                    acc_factor = min(acc_factor + incremento, max_paso)
                low1 = Low[i - 1]
                low2 = Low[i - 2]
                if low2 < Close[i]: # Asegurarnos que el PSAR no está por encima de los precios más bajos recientes
                    Close[i] = low2
                elif low1 < Close[i]:
                    Close[i] = low1
                    
        # Tendencia Bajista
        else:
            # Calcular el PSAR para la tendencia bajista
            Close[i] = Close[i - 1] - (acc_factor * (Close[i - 1] - down_trend_low))
            if max_high > Close[i]: # Verificar si hay reversión a tendencia alcista
                reversal = True
                Close[i] = down_trend_low 
                up_trend_high = max_high
                acc_factor = incremento 
            else:
                if min_low < down_trend_low: # Actualizar el mínimo en tendencia bajista
                    down_trend_low = min_low
                    acc_factor = min(acc_factor + incremento, max_paso)
                high1 = High[i - 1]
                high2 = High[i - 2]
                if high2 > Close[i]: # Asegurarnos que el PSAR no está por debajo de los precios más altos recientes
                    Close[i] = high2
                elif high1 > Close[i]:
                    Close[i] = high1
    
        # Determinar la tendencia actual
        up_trend = up_trend != reversal 
        
        # Asignar los valores de PSAR a las respectivas tendencias
        if up_trend:
            psar_up[i] = Close[i]
        else:
            psar_down[i] = Close[i]
            
    # Crear las columnas en el DataFrame para almacenar los resultados
    data["PSAR"] = Close
    data["UpTrend"] = psar_up
    data["DownTrend"] = psar_down
    
    return data[["PSAR", "UpTrend", "DownTrend"]]
    
# Obtener Datos
df = yf.download("NKLA", start="2023-01-01", end="2024-01-01", interval="1d")

# Calcular Indicador
psar = Parabolic_SAR(df, incremento=0.02, max_paso=0.20)

# Gráficos adicionales
apds = [
        
        mpf.make_addplot(psar["UpTrend"], type="scatter", markersize=10, color="g", label="Tendencia Alcista"),
        mpf.make_addplot(psar["DownTrend"], type="scatter", markersize=10, color="r", label="Tendencia Bajista")
        
        ]    

fig, axes = mpf.plot(df, type="candle", style="yahoo", volume=True, addplot=apds, title="Gráfico de Velas con Parabolic SAR",
                     ylabel="Precio", ylabel_lower="Volumen", figsize=(26, 10), returnfig=True)

axes[0].legend(loc="upper left", fontsize=8)
plt.show()
    
# Recordatorio:
#   - El Parabolic SAR es un indicador útil para identificar reversiones de tendencia, pero debe combinarse con otros indicadores
#     o análisis para confirmar las señales antes de tomar decisiones.
#   - Ajustar los parámetros según las características del activo y la estrategia que estemos utilizando.

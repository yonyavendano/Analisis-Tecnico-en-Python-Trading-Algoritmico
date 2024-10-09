# -*- coding: utf-8 -*-
# Importar librerías
import pandas as pd
import yfinance as yf
import mplfinance as mpf
import matplotlib.pyplot as plt

# Indicador: Índice de Volatilidad Relativa
def Indice_Volatilidad_Relativa(df: pd.DataFrame, longitud_std_dev: int = 14, longitud_suavizado: int = 14, columna: str = "Close") -> pd.Series:
    
    """
    El Índice de Volatilidad Relativa (RVI) es un indicador que mide la dirección y magnitud de la volatilidad. El RVI oscila en el rango
    de 0 a 100. Un aumento en el valor del RVI indica un movimiento alcista del precio, mientras que una caída en el RVI indicaría una
    disminución en el precio.
    
    Cómo Operarlo:
        
        Lecturas de RVI por encima de 50 se consideran como una señal alcista y por debajo de 50 como una señal bajista.
        
        Lecturas de RVI por encima de 70 se considerarían como lecturas alcistas fuertes que apuntan a una fuerte tendencia alcista y la
        posibilidad de una condición de sobrecompra, mientras que lecturas de RVI por debajo de 30 se considerarían como lecturas bajistas
        fuertes que apuntan a una fuerte tendencia bajista y la posibilidad de una condición de sobreventa.
        
    -----------
    Parámetros:
    -----------
    param : pd.DataFrame : df : Datos del activo financiero.
    -----------
    param : int : longitud_std_dev : Ventana para el cálculo del RVI (por defecto, se establece en 14).
    -----------
    param : int : longitud_suavizado : Ventana para el cálculo del suavizado del RVI (por defecto, se establece en 14).
    -----------
    param : str : columna : Columna a utilizar en el cálculo del RVI (por defecto, se establece en 'Close').
    -----------
    Salida:
    -----------
    return : pd.Series : Cálculo del Índice de Volatilidad Relativa.
    """
    
    # Calcular
    precio_col = df[columna]
    desviacion_std_roll = precio_col.rolling(window=longitud_std_dev, min_periods=longitud_std_dev).std()
    cambio = precio_col.diff(periods=1)
    UpSum = desviacion_std_roll.where(cambio >= 0, 0).ewm(span=longitud_suavizado, adjust=False).mean()
    DwSum = desviacion_std_roll.where(cambio < 0, 0).ewm(span=longitud_suavizado, adjust=False).mean()
    
    RVI = (100 * UpSum) / (UpSum + DwSum)
    RVI.name = "RVI"
    
    return RVI

# Descargar datos
ticker = "ADBE"
df = yf.download(ticker, start="2022-01-01", end="2024-01-01", interval="1d")

# Calcular el Índice de Volatilidad Relativa
rvi_df = Indice_Volatilidad_Relativa(df, longitud_std_dev=14, longitud_suavizado=14)
    
# Calcular el SMA del RVI
sma_longitud = 14
sma_rvi = rvi_df.rolling(window=sma_longitud, min_periods=sma_longitud).mean()
sma_rvi.name = "SMA_RVI"

# Crear el gráfico
ap = [
      
      mpf.make_addplot(rvi_df, color="blue", label="RVI", panel=2, ylabel="RVI"),
      mpf.make_addplot(sma_rvi, color="red", linestyle="--", label="SMA RVI", panel=2),
      mpf.make_addplot([70] * len(rvi_df), panel=2, color="gray", linestyle="--", label="Fuerte Tendencia Alcista"),
      mpf.make_addplot([30] * len(rvi_df), panel=2, color="gray", linestyle="--", label="Fuerte Tendencia Bajista")
      
      ]
    
fig, axes = mpf.plot(df, type="candle", style="charles", volume=True, addplot=ap, returnfig=True, figsize=(22, 10))

axes[0].set_xlabel("Fecha", fontsize=14)
axes[0].set_ylabel("Precio", fontsize=14)  
axes[0].set_title("Índice de Volatilidad Relativa de: " + ticker, fontsize=16, weight="bold")

plt.show()
    
# Recordatorio:
#   - El Índice de Volatilidad Relativa mide la dirección y magnitud de la volatilidad en un rango de 0 a 100.
#   - Lecturas por encima de 50 sugieren una tendencia alcista, mientras que lecturas por debajo de 50 indican una tendencia bajista.
#   - Valores superiores a 70 señalan una fuerte tendencia alcista y posible sobrecompra, mientras que valores inferiores a 30
#     indican una fuerte tendencia bajista y posible sobreventa.

# -*- coding: utf-8 -*-
# Importar librerías
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import timedelta

# Indicador: Volumen de Balance
def On_Balance_Volume(df: pd.DataFrame, columna: str = "Close") -> pd.Series:
    
    """
    On-Balance Volume (OBV) es un indicador en el trading técnico que utiliza el volumen para predecir cambios en el precio de
    los activos. Se basa en la distinción entre dinero inteligente -es decir, inversores institucionales (aumento de volatilidad)-
    y menos sofisticados inversores minoristas (baja volatilidad).
    
    Cómo Operarlo:
        
        El OBV se puede usar para medir el nivel de volatilidad y como una herramienta para posicionar transacciones a un menor costo
        cuando la volatilidad es alta. Ademas, se puede ajustar una Media Móvil al cálculo y comprar cuando la MA cruce por encima
        del OBV y vender cuando la MA cruce por debajo del OBV.
        
    -----------
    Parámetros:
    -----------
    param : pd.DataFrame : df : Datos históricos.
    -----------
    param : str : columna : Columna a ser utilizada en el cálculo del OBV (por defecto, se usa 'Close').
    -----------
    Salida:
    -----------
    return : pd.Series : Cálculo del On-Balance Volume.
    """
    
    # Calcular
    volume = df["Volume"]
    OBV = (np.sign(df[columna].diff(periods=1)) * volume).fillna(value=volume).cumsum()
    OBV.name = "OBV"
    
    return OBV

# Descargar datos
ticker = "V"
df = yf.download(ticker, start="2022-01-01", end="2024-01-01", interval="1d")

# Calcular Indicador
obv = On_Balance_Volume(df)

# Calcular la media móvil del OBV
sma_period = 20
obv_sma = obv.rolling(window=sma_period, min_periods=sma_period).mean()

# Crear gráfico con subplots
fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(22, 12), sharex=True)

# Subplot 1: Precio de Cierre
ax1.plot(df.index, df["Close"], color="orange", label="Precios de Cierre de:" + ticker, linewidth=2)
ax1.set_ylabel("Precios del Activo", fontsize=15, color="orange")
ax1.legend(loc="upper left")
ax1.set_title("Precio de Cierre y On-Balance Volume", fontsize=16)

# Subplot 2: On-Balance Volume
ax2.plot(obv.index, obv, color="dodgerblue", linestyle="--", linewidth=2, label="On-Balance Volume (OBV)")
ax2.plot(obv_sma.index, obv_sma, color="green", linestyle="--", linewidth=2, label=f"SMA {sma_period} días/periodos")
ax2.axhline(y=0, color="gray", linestyle="--")
ax1.set_ylabel("OBV", fontsize=15)
ax1.set_xlabel("Fecha", fontsize=15)

# Añadir anotaciones para señales de compra/venta en OBV
buy_signals = (obv > obv_sma) & (obv.shift(periods=1) <= obv_sma.shift(periods=1))
sell_signals = (obv < obv_sma) & (obv.shift(periods=1) >= obv_sma.shift(periods=1))

ax2.scatter(df.index[buy_signals], obv[buy_signals], color="lime", marker="^", label="Señal de Compra", s=100, edgecolors="black")
ax2.scatter(df.index[sell_signals], obv[sell_signals], color="red", marker="v", label="Señal de Venta", s=100, edgecolors="black")

# Añadir texto explicativo sobre cómo operarlo
ax2.text(df.index[-1] + timedelta(days=17), obv.max() * 0.8, "Señales de Compra cuando \nOBV cruza por encima de SMA", fontsize=12, color="lime",
         bbox=dict(facecolor="white", edgecolor="lime", boxstyle="round,pad=0.5"))
ax2.text(df.index[-1] + timedelta(days=17), obv.min() * 0.8, "Señales de Venta \nOBV cruza por debajo de SMA", fontsize=12, color="red",
         bbox=dict(facecolor="white", edgecolor="red", boxstyle="round,pad=0.5"))

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Recordatorio:
#   - El OBV es una herramienta que utiliza el volumen para evaluar la fuerza y confirmación de una tendencia en los precios.
#   - Las señales de compra y venta proporcionan puntos de entrada y salida, pero siempre deben ser confirmadas con otros indicadores.

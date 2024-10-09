# -*- coding: utf-8 -*-
# Importar librerías
import pandas as pd
import numpy as np
import yfinance as yf
import mplfinance as mpf
import matplotlib.pyplot as plt

# Indicador: Know Sure Thing
def Know_Sure_Thing(df: pd.DataFrame, roclen1: int = 10, roclen2: int = 15, roclen3: int = 20, roclen4: int = 30, smalen1: int = 10,
                    smalen2: int = 10, smalen3: int = 10, smalen4: int = 15, signal: int = 9, columna: str = "Close") -> pd.DataFrame:
    
    """
    Conocer Cosa Segura (Know Sure Thing) es un indicador técnico desarrollado para facilitar la lectura de tasas de cambio. Es útil para
    identificar puntos importantes en los ciclos de activos porque su fórmula está ponderada para estar más influenciada por los intervalos
    de tiempo más largos y dominantes, con el fin de reflejar mejor los movimientos principales en el ciclo del mercado de valores.
    
    Cómo Operarlo:
        
        El KST fluctúa por encima o por debajo de la línea de cero. En su forma más básica, el momentum favorece a los toros cuando el KST
        es positivo y favorece a los osos cuando el KST es negativo. Una lectura positiva significa que los valores ponderados y suavizados
        de la tasa de cambio son en su mayoría positivos y los precios están en alza. Una lectura negativa indica que los precios están
        en descanso. Se añade una línea de señal al indicador para generar señales de compra/venta. Cuando el indicador cruza de abajo
        hacia arriba (hacia la línea de la señal) significa una señal de compra y cuando cruza de arriba hacia abajo (la línea de señal)
        signigica una señal de venta.
        
    -----------
    Parámetros:
    -----------
    param : pd.DataFrame : df : Datos del activo.
    -----------
    param : int : roclen1 : Ventana No. 1 para ser utilizada en la Tasa de Cambio para el cálculo del KST (por defecto, se establece en 10).
    -----------
    param : int : roclen2 : Ventana No. 2 para ser utilizada en la Tasa de Cambio para el cálculo del KST (por defecto, se establece en 15).
    -----------
    param : int : roclen3 : Ventana No. 3 para ser utilizada en la Tasa de Cambio para el cálculo del KST (por defecto, se establece en 20).
    -----------
    param : int : roclen4 : Ventana No. 4 para ser utilizada en la Tasa de Cambio para el cálculo del KST (por defecto, se establece en 30).
    -----------
    param : int : smalen1 : Ventana No. 1 para ser utilizada en el Promedio Móvil para el cálculo del KST (por defecto, se establece en 10).
    -----------
    param : int : smalen2 : Ventana No. 2 para ser utilizada en el Promedio Móvil para el cálculo del KST (por defecto, se establece en 10).
    -----------
    param : int : smalen3 : Ventana No. 3 para ser utilizada en el Promedio Móvil para el cálculo del KST (por defecto, se establece en 10).
    -----------
    param : int : smalen4 : Ventana No. 4 para ser utilizada en el Promedio Móvil para el cálculo del KST (por defecto, se establece en 15).
    -----------
    param : int : señal : Ventana de señal a ser utilizada en el cálculo del KST (por defecto, se establece en 9).
    -----------
    param : str : columna : Columna a ser utilizada en el cálculo del KST (por defecto, se establece en 'Close').
    -----------
    Salida:
    -----------
    return : pd.DataFrame : Cálculo del Know Sure Thing.
    """
    
    # Calcular
    price_col = df[columna]
    # ROCs con Medias Móviles
    ROC1R = price_col.diff(periods=roclen1) / price_col.shift(periods=roclen1) * 100
    ROC1R = ROC1R.rolling(window=smalen1, min_periods=smalen1).mean()
    ROC2R = price_col.diff(periods=roclen2) / price_col.shift(periods=roclen2) * 100
    ROC2R = ROC2R.rolling(window=smalen2, min_periods=smalen2).mean()
    ROC3R = price_col.diff(periods=roclen3) / price_col.shift(periods=roclen3) * 100
    ROC3R = ROC3R.rolling(window=smalen3, min_periods=smalen3).mean()
    ROC4R = price_col.diff(periods=roclen4) / price_col.shift(periods=roclen4) * 100
    ROC4R = ROC4R.rolling(window=smalen4, min_periods=smalen4).mean()
    
    # KST
    KST_df = (ROC1R + 2 * ROC2R + 3 * ROC3R + 4 * ROC4R)
    KST_signal = KST_df.rolling(window=signal).mean()
    KST = pd.concat([KST_df, KST_signal], axis=1)
    KST.columns = ["KST", "KST Signal"]
    
    return KST

# Descargar datos
ticker = "MSCI"
df = yf.download(ticker, start="2021-01-01", end="2024-01-01", interval="1d")

# Calcular KST
df[["KST", "KST Signal"]] = Know_Sure_Thing(df)
    
df["Cruces"] = np.where((df["KST"] > df["KST Signal"]) & (df["KST"].shift(periods=1) < df["KST Signal"].shift(periods=1)), 1,
                        np.where((df["KST"] < df["KST Signal"]) & (df["KST"].shift(periods=1) > df["KST Signal"].shift(periods=1)), -1,
                                 np.nan))

ap = [
      
      mpf.make_addplot(df["KST"], panel=2, color="orange", ylabel="KST"),
      mpf.make_addplot(df["KST Signal"], panel=2, color="blue", ylabel="Señal"),
      mpf.make_addplot(df["KST"].where(df["Cruces"] == 1, np.nan), panel=2, marker="^", markersize=100, color="green", type="scatter"),
      mpf.make_addplot(df["KST"].where(df["Cruces"] == -1, np.nan), panel=2, marker="v", markersize=100, color="red", type="scatter")
      
      ]

fig, axes = mpf.plot(df, type="candle", volume=True, addplot=ap, figsize=(28, 15), style="yahoo", 
                     title="Precios, Volumen e Indicador KST", warn_too_much_data=df.shape[0], ylabel="Precio",
                     ylabel_lower="Volumen", panel_ratios=(2, 1, 3), returnfig=True)

for ax in axes:
    ax.yaxis.label.set_size(18) # Cambiar el tamaño según sea necesario
    ax.yaxis.label.set_fontsize(18)
    ax.yaxis.label.set_fontweight("bold")
    
plt.show()
    
# Recordatorio:
#   - Know Sure Thing combina varias tasas de cambio ponderadas para evaluar el momentum del activo.
#   - Utiliza la línea de señal para generar señales de compra o venta.

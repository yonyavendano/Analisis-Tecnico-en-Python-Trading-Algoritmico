# -*- coding: utf-8 -*-
# Importar librerías
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

# Indicador: RSI Estocástico
def RSI_Estocastico(df: pd.DataFrame, longitud_rsi: int = 14, longitud_stoch: int = 14, suavizarK: int = 3, suavizarD: int = 3, 
                    columna: str = "Close") -> pd.DataFrame:
    
    """
    El Índice de Fuerza Relativa Estocástico (StochRSI) es un indicador técnico utilizado para medir la fortaleza y debilidad del
    RSI durante un período de tiempo determinado. El StochRSI deriva sus valores del RSI. Básicamente, se aplica un oscilador
    estocástico a un conjunto de valores de RSI; por lo tanto, se basa en el precio.
    
    La fórmula estocástica se utiliza para comparar el precio de cierre de la acción con su rango de precios para predecir los puntos
    de cambio de precio (condiciones de sobrecompra y sobreventa en el mercado). El Oscilador StochRSI comprende un indicador más
    sensible ajustado a un rendimiento histórico específico.
    
    Cómo Operarlo:
        
        Una lectura de StochRSI por encima de 80 se considera sobrecompra (por lo que se puede colocar una posición corta), mientras
        que una lectura por debajo de 20 se considera sobrevendida (por lo que se puede colocar una posición larga). La sobrecompra
        no significa necesariamente que el precio se invertirá hacia abajo, al igual que la sobreventa no significa que el precio se
        invertirá hacia arriba. Más bien, las condiciones de sobrecompra y sobreventa simplemente alertan a los operadores de que el 
        RSI está cerca de los extremos de sus lecturas recientes. Una lectura de cero significa que el RSI está en su nivel más bajo
        en "n" periodos y una lectura de 100 significa que el RSI está en el nivel más alto en los últimos "n" periodos.
        
    -----------
    Parámetros:
    -----------
    param : int : longitud_rsi : Ventana a utilizar en el cálculo del RSI (por defecto, se establece en 14).
    -----------
    param : int : longitud_stoch : Ventana a utilizar en el cálculo del StochRSI (por defecto, se establece en 14).
    -----------
    param : int : suavizarK : Ventana a utilizar en el cálculo del StochRSI_k (por defecto, se establece en 3).
    -----------
    param : int : suavizarD : Ventana a utilizar en el cálculo del StochRSI_d (por defecto, se establece en 3).
    -----------
    param : str : columna : Columna a utilizar en el cálculo del RSI Estocástico (por defecto, se establece en 'Close').
    -----------
    Salida:
    -----------
    return : pd.DataFrame : Cálculo del Índice de Fuerza Relativa Estocástico.
    """
    
    # Calcular RSI
    Delta = df[columna].diff(periods=1)
    Ganancia = Delta.where(Delta >= 0, 0)
    Perdida = np.abs(Delta.where(Delta < 0, 0))
    # Valores en la posición de la longitud
    media_ganancia = Ganancia.ewm(span=longitud_rsi, min_periods=longitud_rsi, adjust=False).mean()
    media_perdida = Perdida.ewm(span=longitud_rsi, min_periods=longitud_rsi, adjust=False).mean()
    RS = media_ganancia / media_perdida
    RSI = pd.Series(np.where(RS == 0, 100, 100 - (100 / (1 + RS))), name="RSI", index=df.index)
    
    # Calcular StochRSI
    minimo_rolling_RSI = RSI.rolling(window=longitud_stoch, min_periods=longitud_stoch).min()
    maximo_rolling_RSI = RSI.rolling(window=longitud_stoch, min_periods=longitud_stoch).max()
    StochRSI = (RSI - minimo_rolling_RSI) / (maximo_rolling_RSI - minimo_rolling_RSI)
    StochRSI_k = StochRSI.rolling(window=suavizarK, min_periods=suavizarK).mean()
    StochRSI_d = StochRSI_k.rolling(window=suavizarD, min_periods=suavizarD).mean()
    
    StRSI = pd.concat([StochRSI * 100, StochRSI_k * 100, StochRSI_d * 100], axis=1)
    StRSI.columns = ["StochRSI", "StochRSI_k", "StochRSI_d"]
    
    return StRSI

# Obtener Datos Históricos
ticker = "BTC-USD" 
df = yf.download(ticker, start="2022-01-01", end="2024-01-01", interval="1d")
    
# Calcular Indicador
stochrsi_df = RSI_Estocastico(df)

# Graficar
plt.figure(figsize=(22, 12))
plt.subplot(2, 1, 1)
plt.plot(df.index, df["Close"], label="Precio de Cierre", color="orange", lw=3)
plt.title("Precio de Cierre de:" + ticker)
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(stochrsi_df.index, stochrsi_df["StochRSI_k"], label = "StochRSI (K)", color="blue")
plt.plot(stochrsi_df.index, stochrsi_df["StochRSI_d"], label = "StochRSI (D)", color="red")
plt.plot(stochrsi_df.index, stochrsi_df["StochRSI"], label = "StochRSI", color="black")
plt.axhline(y=80, color="red", linestyle="--", label="SobreCompra (80)")
plt.axhline(y=20, color="green", linestyle="--", label="SobreVenta (20)") 
plt.title("Stochastic RSI de:" + ticker)
plt.legend(loc="center left", fontsize=8)
plt.tight_layout()
plt.show()
    
# Recordatorio: 
#   - El StochRSI combina el RSI con un Oscilador Estocástico para proporcionar una evaluación más precisa de las condiciones del mercado.
#   - Lecturas por encima de 80 sugieren que el activo está sobrecomprado, mientras que lecturas por debajo de 20 indican sobreventa.

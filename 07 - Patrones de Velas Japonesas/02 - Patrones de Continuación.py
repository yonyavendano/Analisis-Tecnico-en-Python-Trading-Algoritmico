# -*- coding: utf-8 -*-
# Importar librerías
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import mplfinance as mpf

# Descargar datos históricos
ticker = "AMZN"
fecha_inicio = "2021-01-01"
fecha_final = "2024-06-01"
df = yf.download(ticker, start=fecha_inicio, end=fecha_final, interval="1d")

# Patrón No. 1: Marubozu
# El Marubozu es una vela que no tiene sombras o tiene sombras muy pequeñas, indicando un fuerte
# control del mercado por una dirección.

# Marubozu
def is_marubozu(df: pd.DataFrame):
    
    """
    Identifica el patrón de velas "Marubozu" en un DataFrame.
    
    -----------
    Parámetros:
    -----------
    param : pd.DataFrame : df : Datos Históricos.
    -----------
    Salida:
    -----------
    return : pd.Series : Serie booleana que indica donde ocurre el patrón de Marubozu
    """
    
    # Cálculo de las dimensiones de las sombras
    sombra_inferior = df["Open"] - df["Low"]
    sombra_superior = df["High"] - df["Close"]
    
    # Condiciones para identificar un Marubozu
    marubozu_condicion = (sombra_inferior <= 0.10 * (df["High"] - df["Low"])) & (sombra_superior <= 0.10 * (df["High"] - df["Low"]))
    
    return marubozu_condicion

# Identificar Marubozu
marubozu = is_marubozu(df)
print(marubozu)
    
# Graficar Patrones
mpf.plot(df.loc[marubozu[marubozu].index], style="yahoo", type="candle", title="Marubozu", figsize=(22, 5), figscale=3.0)
plt.show()
    
# Patrón No. 2: Three White Soldiers
# Este patrón alcista se forma con tres velas largas y blancas/verdes (alcista) consecutivas, que cierran en el nivel más alto del día,
# indicando una fuerte tendencia alcista.

# Three White Soldiers
def is_three_white_soldiers(df: pd.DataFrame):    
    
    """
    Identifica el patrón de velas "Three White Soldiers" en un DataFrame.
    
    -----------
    Parámetros:
    -----------
    param : pd.DataFrame : df : Datos Históricos.
    -----------
    Salida:
    -----------
    return : pd.Series : Serie booleana que indica donde ocurre el patrón de Three White Soldiers
    """
    
    # Condiciones para identificar Three White Soldiers
    condicion = (df["Close"].shift(periods=2) > df["Open"].shift(periods=2)) & \
                (df["Close"].shift(periods=1) > df["Open"].shift(periods=1)) & \
                (df["Close"] > df["Open"]) & \
                (df["Close"].shift(periods=2) < df["Close"].shift(periods=1)) & \
                (df["Close"].shift(periods=1) < df["Close"]) & \
                (df["Open"].shift(periods=2) < df["Open"].shift(periods=1)) & \
                (df["Open"].shift(periods=1) < df["Open"])
                
    return condicion

# Identificar Three White Soldiers
tws = is_three_white_soldiers(df)

# Graficar Patrones
mpf.plot(df.loc[tws[tws].index], style="yahoo", type="candle", title="Three White Soldiers", figsize=(22, 5), figscale=3.0)
plt.show()

# Patrón No. 3: Three Black Crows
# Este patrón bajista se forma con 3 velas largas y negras (bajistas) consecutivas, que cierran en el nivel más bajo del día, 
# indicando una fuerte tendencia bajista.

# Three Black Crows
def is_three_black_crows(df: pd.DataFrame):    
    
    """
    Identifica el patrón de velas "Three Black Crows" en un DataFrame.
    
    -----------
    Parámetros:
    -----------
    param : pd.DataFrame : df : Datos Históricos.
    -----------
    Salida:
    -----------
    return : pd.Series : Serie booleana que indica donde ocurre el patrón de Three Black Crows
    """
    
    # Condiciones para identificar Three White Soldiers
    condicion = (df["Close"].shift(periods=2) < df["Open"].shift(periods=2)) & \
                (df["Close"].shift(periods=1) < df["Open"].shift(periods=1)) & \
                (df["Close"] < df["Open"]) & \
                (df["Close"].shift(periods=2) > df["Close"].shift(periods=1)) & \
                (df["Close"].shift(periods=1) > df["Close"]) & \
                (df["Open"].shift(periods=2) > df["Open"].shift(periods=1)) & \
                (df["Open"].shift(periods=1) > df["Open"])
                
    return condicion

# Identificar Three Black Crows
tbc = is_three_black_crows(df)

# Graficar Patrones
mpf.plot(df.loc[tbc[tbc].index], style="yahoo", type="candle", title="Three Black Crows", figsize=(22, 5), figscale=3.0)
plt.show()

# Recordatorio:
#   - El patrón Marubozu indica un control total del mercado durante la sesión.
#   - El patrón Three White Soldiers sugiere una fuerte continuación de la tendencia alcista actual. Cada vela debe
#     cerrar más alto que la anterior, y cada apertura debe de ser superior a la apertura de la vela anterior.
#   - El patrón Three Black Crows indican una sólida continuación de la tendencia bajista. Cada vela debe cerrar más
#     bajo que la anterior, y cada apertura debe ser inferior a la apertura de la vela anterior.

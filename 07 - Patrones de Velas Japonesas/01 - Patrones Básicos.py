# -*- coding: utf-8 -*-
# Importar librerías
import pandas as pd
import yfinance as yf
import mplfinance as mpf
import matplotlib.pyplot as plt

# Descargar Datos Históricos
ticker = "AMZN"
fecha_inicio = "2021-01-01"
fecha_final = "2024-01-01"
df = yf.download(ticker, start=fecha_inicio, end=fecha_final, interval="1d")

# Patrón No. 1: Martillo (Hammer)
# El Martillo se forma cuando el cuerpo es pequeño y la sombra inferior es al menos el doble del tamaño del cuerpo.
# La sombra superior debe ser pequeña o inexistente.

# Hammer
def is_hammer(df: pd.DataFrame):
    
    """
    Identifica el patrón de velas "Martillo" en un DataFrame.
    
    -----------
    Parámetros:
    -----------
    param : pd.DataFrame : df : Datos Históricos.
    -----------
    Salida:
    -----------
    return : pd.Series : Serie booleana que indica donde ocurre el patrón de Martillo
    """
    
    # Cálculo de las dimensiones del cuerpo y las sombras
    cuerpo = abs(df["Close"] - df["Open"])
    sombra_inferior = abs(df["Low"] - df[["Open", "Close"]].min(axis=1))
    sombra_superior = abs(df["High"] - df[["Open", "Close"]].max(axis=1))
    
    # Condiciones para identificar un Martillo
    condicion_martillo = (sombra_inferior >= 2 * cuerpo) & (sombra_superior < cuerpo)
    
    # Verificar que la vela sea la más baja en las últimas 3 velas
    min_ultimas_3 = df["Low"].rolling(window=3, min_periods=3).min()
    es_baja = (df["Low"] == min_ultimas_3)
    
    # Combinar las condiciones
    martillo = condicion_martillo & es_baja
    
    return martillo

# Hammer
hammer = is_hammer(df)
print(hammer)

# Graficar Patrones
mpf.plot(df.loc[hammer[hammer].index], style="yahoo", type="candle", title="Martillo (Hammer)", figsize=(22, 5), figscale=3.0)
plt.show() 
    
# Patrón No. 2: Hombre Colgado (Hanging Man)
# El Hombre Colgado es similar al Martillo, pero aparece en una tendencia alcista.

# Hanging Man
def is_hanging_man(df: pd.DataFrame):
    
    """
    Identifica el patrón de velas "Hanging Man" en un DataFrame.
    
    -----------
    Parámetros:
    -----------
    param : pd.DataFrame : df : Datos Históricos.
    -----------
    Salida:
    -----------
    return : pd.Series : Serie booleana que indica donde ocurre el patrón de Hanging Man.
    """
    
    # Cálculo de las dimensiones del cuerpo y las sombras
    cuerpo = abs(df["Close"] - df["Open"])
    sombra_inferior = abs(df["Low"] - df[["Open", "Close"]].min(axis=1))
    sombra_superior = abs(df["High"] - df[["Open", "Close"]].max(axis=1))
    
    # Condiciones para identificar un Hanging Man
    condicion_hanging_man = (sombra_inferior >= 2 * cuerpo) & (sombra_superior < cuerpo)
    
    # Verificar que la vela sea la más alta en las últimas 3 velas
    max_ultimas_3 = df["High"].rolling(window=3, min_periods=3).max()
    es_maximo = (df["High"] == max_ultimas_3)
    
    # Combinar las condiciones
    hanging_man = condicion_hanging_man & es_maximo
    
    return hanging_man

# Hanging Man
hanging_man = is_hanging_man(df)
print(hanging_man)
    
# Graficar Patrones
mpf.plot(df.loc[hanging_man[hanging_man].index], style="yahoo", type="candle", title="Hanging Man", figsize=(22, 5), figscale=3.0)
plt.show()
    

# Patrón No. 3: Doji
# El Doji ocurre cuando el precio de apertura y cierre son casi iguales, lo que sugiere indecisión en el mercado.

# Doji
def is_doji(df: pd.DataFrame):

    """
    Identifica el patrón de velas "Doji" en un DataFrame.
    
    -----------
    Parámetros:
    -----------
    param : pd.DataFrame : df : Datos Históricos.
    -----------
    Salida:
    -----------
    return : pd.Series : Serie booleana que indica donde ocurre el patrón de Doji.
    """
    
    # Cálculo de la diferencia entre la apertura y el cierre.
    cuerpo = abs(df["Close"] - df["Open"])
    
    # Condición de cuerpo pequeño
    cuerpo_pequeno = cuerpo <= (df["High"] - df["Low"]) * 0.1 
    
    # Condición de centrado de cuerpo
    centrado = (abs((df["High"] + df["Low"]) / 2 - (df["Open"] + df["Close"]) / 2)) <= (df["High"] - df["Low"]) * 0.1
    
    # Condiciones para identificar un Doji
    doji = cuerpo_pequeno & centrado
    
    return doji

# Doji
doji = is_doji(df)

# Graficar Patrones
mpf.plot(df.loc[doji[doji].index], style="yahoo", type="candle", title="Doji", figsize=(22, 5), figscale=3.0)
plt.show()
    
# Recordatorio:
#   - Un Martillo aparece tras una tendencia bajista, indicando posible reversión a la alza. Se caracteriza por una sombra inferior
#     larga y un cuerpo pequeño en la parte superior.
#   - Un Hanging Man aparece al final de una tendencia alcista, sugiriendo una posible reversión a la baja. Similar al Martillo, pero
#     en una tendencia alcista.
#   - Un Doji se forma cuando los precios de apertura y cierre son casi iguales, señalando indecisión en el mercado y un posible cambio
#     de tendencia, dependiendo del contexto.

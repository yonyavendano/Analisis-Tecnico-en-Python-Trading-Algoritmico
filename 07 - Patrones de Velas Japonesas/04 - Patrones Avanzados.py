# -*- coding: utf-8 -*-
# Importar librerías
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import mplfinance as mpf

# Descargar datos históricos
ticker = "AMZN"
fecha_inicio = "2021-01-01"
fecha_final = "2024-01-01"
df = yf.download(ticker, start=fecha_inicio, end=fecha_final, interval="1d")

# Patrón Three Outside Down
def three_outside_down(df: pd.DataFrame) -> pd.DataFrame:
    
    """
    Identifica el patrón de vela Three Outside Down en un DataFrame.
    
    El patrón Three Outside Down es una señal de reversión bajista en un mercado alcista. 
    Consiste en tres velas: la primera es una vela alcista, seguida de una vela bajista que 
    envuelve la primera, y una tercera vela bajista que cierra por debajo del mínimo de la 
    segunda vela.
    
    Parámetros:
    ----------
    param : pd.DataFrame : df : Datos Históricos.
    ----------
    Salida:
    ----------
    return : pd.DataFrame : DataFrame con el patrón Three Outside Down identificado.
    """
    
    # Calcular las series desplazadas
    O, H, L, C = df["Open"], df["High"], df["Low"], df["Close"]
    O1, H1, L1, C1 = O.shift(1), H.shift(1), L.shift(1), C.shift(1)
    O2, H2, L2, C2 = O.shift(2), H.shift(2), L.shift(2), C.shift(2)
    
    # Definir el patrón
    tod = (
        
        ((C2 - O2) / (H2 - L2) >= 0.50) &
        (L2 > C1) & 
        (H2 < O1) & 
        ((O1 - C1) >= (0.60 * (H1 - L1))) &
        (((H1 - L1) / (H2 - L2)) <= 2.5) &
        (O > C1) &
        (C < C1) &
        (((O - C) / (H - L)) >= 0.45) & 
        (((O - C) / (O1 - C1)) < 1.0) & 
        (O < ((O1 + C1) / 2)) & 
        (H < (O1 - (O1 - C1) * 0.33)) &
        (L < L1)
        
        )
    
    return df[tod]

# Encontrar Patrones
df_tod = three_outside_down(df)
print(df_tod)

if len(df_tod) > 0:
    fig, axes = mpf.plot(df_tod, type="candle", style="yahoo", figsize=(22, 10), figscale=3.0, 
                         title="Three Outside Down", returnfig=True)
    plt.show()
    
# Patrón Three Outside Up
def three_outside_up(df: pd.DataFrame) -> pd.DataFrame:
    
    """
    Identifica el patrón de vela Three Outside Up en un DataFrame.
    
    El patrón Three Outside Up es una señal de reversión alcista en un mercado bajista. 
    Consiste en tres velas: la primera es una vela bajista, seguida de una vela alcista que 
    envuelve la primera, y una tercera vela alcista que cierra por encima del máximo de la 
    segunda vela.
    
    Parámetros:
    ----------
    param : pd.DataFrame : df : Datos Históricos.
    ----------
    Salida:
    ----------
    return : pd.DataFrame : DataFrame con el patrón Three Outside Up identificado.
    """
    
    # Calcular las series desplazadas
    O, H, L, C = df["Open"], df["High"], df["Low"], df["Close"]
    O1, H1, L1, C1 = O.shift(1), H.shift(1), L.shift(1), C.shift(1)
    O2, H2, L2, C2 = O.shift(2), H.shift(2), L.shift(2), C.shift(2)
    
    # Definir el patrón
    tou = (
        
        ((O2 - C2) / (H2 - L2) >= 0.50) &
        (H2 < C1) & 
        (L2 > O1) & 
        ((C1 - O1) >= (0.60 * (H1 - L1))) &
        (((H1 - L1) / (H2 - L2)) <= 2.5) &
        (O < C1) &
        (C > C1) &
        (((C - O) / (H - L)) >= 0.45) & 
        (((C - O) / (C1 - O1)) < 1.0) & 
        (O > ((O1 + C1) / 2)) & 
        (L > (O1 + (O1 - C1) * 0.33)) &
        (H > H1)
        
        )
    
    return df[tou]

# Encontrar Patrones
df_tou = three_outside_up(df)
print(df_tou)

if len(df_tou) > 0:
    fig, axes = mpf.plot(df_tou, type="candle", style="yahoo", figsize=(22, 10), figscale=3.0, 
                         title="Three Outside Up", returnfig=True)
    plt.show()   
    
# Recordatorio:
#   - El patrón Three Outside Down es un patrón de reversión bajista que sugiere una posible reversión de una tendencia alcista a bajista.
#   - El patrón Three Outside Up es un patrón de reversión alcista que sugiere una posible reversión de una tendencia bajista a alcista.

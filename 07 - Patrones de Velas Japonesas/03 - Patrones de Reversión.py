# -*- coding: utf-8 -*-
# Importar librerías
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import mplfinance as mpf

# Obtener Datos Históricos
ticker = "AAPL"
fecha_inicio = "2010-01-01"
fecha_final = "2024-01-01"
df = yf.download(ticker, start=fecha_inicio, end=fecha_final, interval="1d")

# Patrón Morning Star: El Morning Star es un patrón alcista de tres velas que señala un cambio en la tendencia de bajista a alcista.
def morning_star(df: pd.DataFrame, longitud: int = 10) -> pd.DataFrame:
    
    """
    Identifica el patrón de vela 'Morning Star' en un DataFrame
    
    -----------
    Parámetros:
    -----------
    param : pd.DataFrame : df : Datos históricos.
    -----------
    param : int : longitud : Ventana para el cálculo del MS (por defecto, se establece en 10).
    -----------
    Salida:
    -----------
    return : pd.DataFrame : Datos del activo donde se encontró al indicador/patrón.
    """
    
    # Calcular las series desplazadas
    O, H, L, C = df["Open"], df["High"], df["Low"], df["Close"]
    O1, H1, L1, C1 = O.shift(periods=1), H.shift(periods=1), L.shift(periods=1), C.shift(periods=1)
    O2, H2, L2, C2 = O.shift(periods=2), H.shift(periods=2), L.shift(periods=2), C.shift(periods=2)
    
    # Definir al patrón Morning Star
    ms = (
        
        ((O2 - C2) / (H2 - L2) >= 0.70) &
        (O1 < L2) & 
        (abs(C1 - O1) / (H1 - L1) <= 0.50) & 
        (abs(C1 - O1) / (H1 - L1) >= 0.10) &
        ((H1 - L1) / (H2 - L2) <= 0.30) &
        (H1 < (L2 + 0.30 * (H2 - L2))) &
        ((C - O) / (H - L) >= 0.70) & 
        ((H - L) / (H2 - L2) <= 1.0) & 
        ((H2 - L2) / (H - L) <= 1.3) &
        ((H - L) / (H2 - L2) >= 0.70) &
        (L < H1) & 
        (O > O1) & 
        (O > C1) &
        (H < H2) &
        (C < O2) &
        (L1 == L1.rolling(window=longitud, min_periods=longitud).min())
        
        )
    
    return df[ms]

# Identificar Patrones
df_morning_star = morning_star(df, longitud=10)
print(df_morning_star)

# Graficar Morning Star si hay datos
if len(df_morning_star) > 0:
    fig, axes = mpf.plot(df_morning_star, type="candle", style="yahoo", volume=True, figsize=(22, 10), title="Patrón Morning Star",
                         ylabel="Precio", ylabel_lower="Volumen", panel_ratios=(2, 1), returnfig=True)
    plt.show()
    
# Patrón Evening Star: El Evening Star es un patrón bajista de tres velas que señala un cambio en la tendencia de alcista a bajista.
def evening_star(df: pd.DataFrame, longitud: int = 10) -> pd.DataFrame:
    
    """
    Identifica el patrón de vela 'Evening Star' en un DataFrame
    
    -----------
    Parámetros:
    -----------
    param : pd.DataFrame : df : Datos históricos.
    -----------
    param : int : longitud : Ventana para el cálculo del ES (por defecto, se establece en 10).
    -----------
    Salida:
    -----------
    return : pd.DataFrame : Datos del activo donde se encontró al indicador/patrón.
    """
    
    # Calcular las series desplazadas
    O, H, L, C = df["Open"], df["High"], df["Low"], df["Close"]
    O1, H1, L1, C1 = O.shift(periods=1), H.shift(periods=1), L.shift(periods=1), C.shift(periods=1)
    O2, H2, L2, C2 = O.shift(periods=2), H.shift(periods=2), L.shift(periods=2), C.shift(periods=2)
    
    # Definir al patrón Evening Star
    es = (
        
        ((C2 - O2) / (H2 - L2) >= 0.70) &
        (O1 > H2) & 
        (abs(C1 - O1) / (H1 - L1) <= 0.50) & 
        (abs(C1 - O1) / (H1 - L1) >= 0.10) &
        ((H1 - L1) / (H2 - L2) <= 0.30) &
        (L1 > (H2 - 0.30 * (H2 - L2))) &
        ((O - C) / (H - L) >= 0.70) & 
        ((H - L) / (H2 - L2) <= 1.0) & 
        ((H2 - L2) / (H - L) <= 1.3) &
        ((H - L) / (H2 - L2) >= 0.70) &
        (H > L1) & 
        (O < np.min([O1, C1], axis=0)) & 
        (L > L2) &
        (C > O2) &
        (H1 == H1.rolling(window=longitud, min_periods=longitud).max())
        
        )
    
    return df[es]

# Identificar Patrones
df_evening_star = evening_star(df, longitud=10)
print(df_evening_star)

# Graficar Evening Star si hay datos
if len(df_evening_star) > 0:
    fig, axes = mpf.plot(df_evening_star, type="candle", style="yahoo", volume=True, figsize=(22, 10), title="Patrón Evening Star",
                         ylabel="Precio", ylabel_lower="Volumen", panel_ratios=(2, 1), returnfig=True)
    plt.show()
    
# Recordatorio:
#   - El patrón Morning Star es un patrón de reversión alcista que indica un posible cambio de tendencia de bajista a alcista.
#   - El patrón Evening Star es un patrón de reversión bajista que indica un posible cambio de tendencia de alcista a bajista.
#   - La flexibilidad en la programación de ciertos patrones dependerá del fin que uno busque. Si quieres enfocarte en la calidad
#     del patrón para maximizar la probabilidad de que cuando se encuentre sea confiable, entonces se recomienda ser más estricto
#     al determinar la lógica en su codificación. Sin embargo, si te interesa más encontrar una mayor cantidad de señales para explorar
#     diferentes escenarios en el mercado, puedes permitir ciertos márgenes de error en la identificación de los patrones.

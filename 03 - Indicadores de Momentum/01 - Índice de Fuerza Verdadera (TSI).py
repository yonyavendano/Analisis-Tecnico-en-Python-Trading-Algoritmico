# -*- coding: utf-8 -*-
# Importar librerías
import pandas as pd
import yfinance as yf
import mplfinance as mpf
import matplotlib.pyplot as plt

# Indicador: Indicador Fuerza Verdadera (TSI)
def Indicador_Fuerza_Verdadera(df: pd.DataFrame, longitud_rapida: int = 13, longitud_lenta: int = 25, señal: int = 13, columna: str = "Close") -> pd.DataFrame:
    
    """
    El Indicador de Fuerza Verdadera (TSI) es un oscilador de impulso técnico utilizado para identificar tendencias y reversiones.
    Es útil para determinar condiciones de sobrecompra y sobreventa, indicando posibles cambios de dirección de la tendencia a través
    de cruces de la línea central o de la línea de señal, y advirtiendo sobre debilidad en la tendencia mediante divergencias.
    
    Cómo Operarlo:
        
        El TSI fluctúa entre números positivos y negativos. Territorio positivo significa que los alcistas tienen más control sobre el 
        activo, mientras que números negativos indican que los bajistas tienen más control. Cuando el indicador diverge con el precio,
        el TSI podría estar señalando que la tendencia del precio se está debilitando y podría revertirse.
        
        Se puede aplicar una línea de señal al indicador TSI. Cuando el TSI cruza por encima de la línea de señal, puede ser utilizado 
        como una señal de compra; cuando cruza por debajo, como una señal de venta. Los niveles de sobrecompra y sobreventa variarán
        según el activo que se esté operando.
        
    -----------
    Parámetros:
    -----------
    param : int : longitud_rapida : Ventana rápida a usar en el cálculo del TSI (por defecto, se establece en 13).
    -----------
    param : int : longitud_lenta : Ventana lenta a usar en el cálculo del TSI (por defecto, se establece en 25).
    -----------
    param : int : señal : Ventana de señal a usar en el cálculo del TSI (por defecto, se establece en 13).
    -----------
    param : str : columna : Columna a utilizar para el cálculo del TSI (por defecto, se establece 'Close').
    -----------
    Salida:
    -----------
    return : pd.DataFrame : Cálculo del Indicador de Fuerza Verdadera.
    """
    
    # Calcular
    Momento = df[columna].diff(periods=1)
    # EMA de Momento
    EMA_lenta = Momento.ewm(span=longitud_lenta, min_periods=longitud_lenta, adjust=False).mean()
    EMA_rapida = EMA_lenta.ewm(span=longitud_rapida, min_periods=longitud_rapida, adjust=False).mean()
    # EMA del Momentum Abs
    Momento_abs = abs(Momento)
    EMA_lenta_abs = Momento_abs.ewm(span=longitud_lenta, min_periods=longitud_lenta, adjust=False).mean()
    EMA_rapida_abs = EMA_lenta_abs.ewm(span=longitud_rapida, min_periods=longitud_rapida, adjust=False).mean()
    # Calcular TSI
    TSI_df = 100 * (EMA_rapida / EMA_rapida_abs)
    Señal = TSI_df.ewm(span=señal, min_periods=señal, adjust=False).mean()
    TSI = pd.concat([TSI_df, Señal], axis=1)
    TSI.columns = ["TSI", "Señal"]
    
    # Determinar tendencia alcista o bajista
    TSI["Tendencia"] = TSI["TSI"] > TSI["Señal"]
    
    return TSI

# Descargar datos
ticker = "QCOM"
df = yf.download(ticker, start="2021-01-01", end="2024-01-01", interval="1d")

# Calcular el TSI
tsi_df = Indicador_Fuerza_Verdadera(df)
    
# Colores de la tendencia
tsi_colores = ["green" if tendencia else "red" for tendencia in tsi_df["Tendencia"]] 

# Niveles de sobrecompra y sobreventa
sobrecomprayventa = [
    
    mpf.make_addplot([25] * len(tsi_df), panel=2, color="black", linestyle="--"),
    mpf.make_addplot([-25] * len(tsi_df), panel=2, color="black", linestyle="--")
    
    ]    

ap = [
      
    mpf.make_addplot(tsi_df["TSI"], panel=2, color="blue", ylabel="TSI"),
    mpf.make_addplot(tsi_df["Señal"], panel=2, color="red"),
    mpf.make_addplot(tsi_df["TSI"], panel=2, type="bar", color=tsi_colores, alpha=0.40)
    
] + sobrecomprayventa

mpf.plot(df, type="candle", style="yahoo", volume=True, addplot=ap, title="Indicador de Fuerza Verdadera (TSI)",
         ylabel="Precio", ylabel_lower="Volumen", figsize=(22, 10), figscale=3.0, warn_too_much_data=df.shape[0])

plt.show()
    
# Recordatorio:
#   - El TSI es un oscilador de impulso que ayuda a identificar tendencias y posibles reversiones en el mercado.
#   - Los cruces de la línea TSI con la línea de señal pueden ser utilizados como señales de compra (cruce hacia arriba) o venta (cruce hacia abajo).
#   - El histograma proporciona una representación visual de la fuerza de la tendencia, con barras verdes indicando un impulso alcista y barras rojas 
#     señalando un impulso bajista.
#   - Los niveles de sobrecompra y sobreventa, marcados por las líneas negras discontínuas, son puntos críticos donde el mercado puede estar listo
#     para una reversión.

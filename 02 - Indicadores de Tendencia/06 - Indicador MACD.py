# -*- coding: utf-8 -*-
# Importar librerías
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

# Indicador: Convergencia-Divergencia de Promedios Móviles (MACD)
def MACD(df: pd.DataFrame, longitud_rapida: int = 12, longitud_lenta: int = 26, longitud_señal: int = 9, columna: str = "Close") -> pd.DataFrame:
    
    """
    La Convergencia-Divergencia de Promedios Móviles (MACD) es un indicador de seguimiento de tendencias que muestra la relación entre
    dos promedios móviles del precio de un activo. El MACD se calcula restando el promedio móvil exponencial de largo plazo (usualmente 26 periodos)
    del promedio móvil exponencial de corto plazo (usualmente de 12 periodos).
    
    Cómo Operarlo:
        
        El resultado del cálculo es la línea MACD. Un EMA de n-periodos de la MACD, llamada "línea de señal", se traza sobre la línea MACD,
        que puede funcionar como un desencadenante para señales de compra y venta. Los traders pueden comprar el activo cuando la MACD cruza
        por encima de su línea de señal y vender en corto plazo cuando la MACD cruza por debajo de la línea de señal.
        
    -----------
    Parámetros:
    -----------
    param : pd.DataFrame : df : Datos del instrumento o activo financiero.
    -----------
    param : int : longitud_rapida : Ventana rápida a utilizar en el cálculo del MACD (por defecto, se establece en 12).
    -----------
    param : int : longitud_lenta : Ventana lenta a utilizar en el cálculo del MACD (por defecto, se establece en 26).
    -----------
    param : int : longitud_señal : Ventana de la señal a utilizar en el cálculo del MACD (por defecto, se establece en 9).
    -----------
    param : str : columna : Columna a utilizar en el cálculo del MACD (por defecto, se establece en 'Close').
    -----------
    Salida:
    -----------
    return : pd.DataFrame : Cálculo de la Convergencia-Divergencia de Promedios Móviles
    """
    
    # Calcular los promedios móviles exponenciales
    MA_Rapida = df[columna].ewm(span=longitud_rapida, min_periods=longitud_rapida, adjust=False).mean()
    MA_Lenta = df[columna].ewm(span=longitud_lenta, min_periods=longitud_lenta, adjust=False).mean()
    # Determinar la línea MACD como la diferencia entre el EMA corto y el EMA largo
    MACD_d = MA_Rapida - MA_Lenta
    # Calcular la línea de señal como el EMA de la línea MACD
    señal = MACD_d.ewm(span=longitud_señal, min_periods=longitud_señal, adjust=False).mean()
    MACD = pd.concat([MACD_d, señal], axis=1)
    MACD.columns = ["MACD", "Señal"]
    
    return MACD

# Obtener Datos Históricos
df = yf.download("SQ", start="2025-01-01", end="2025-07-01", interval="1d", multi_level_index=False)

# Calcular Indicador
macd = MACD(df, longitud_rapida=12, longitud_lenta=26, longitud_señal=9)

# Graficar Indicador
fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(22, 10), sharex=True)

# Gráfico del Precio de Cierre
ax1.plot(df.index, df["Close"], label="Precio de Cierre", color="blue")
ax1.set_title("Precio de Cierre", size=18, fontweight="bold")
ax1.set_ylabel("Precio")
ax1.legend(loc="upper left")
ax1.grid(True)

# Gráfico del MACD
ax2.plot(macd.index, macd["MACD"], label="MACD", color="blue")
ax2.plot(macd.index, macd["Señal"], label="Línea de la Señal", color="red")
ax2.bar(macd.index, macd["MACD"] - macd["Señal"], color=np.where(macd["MACD"] > macd["Señal"], "green", "red"), label="Histograma")
ax2.set_title("Convergencia-Divergencia de Promedios Móviles (MACD)", size=18, fontweight="bold")
ax2.set_xlabel("Fecha")
ax2.set_ylabel("Valor")
ax2.legend(loc="lower left")
ax2.grid(True) 

plt.tight_layout()
plt.show()   
    
# Recordatorio:
#   - El MACD se utiliza para identificar posibles señales de compra y venta. Un cruce de la línea MACD por encima de la línea de la señal
#     puede sugerir una oportunidad de compra.
#   - Un cruce por debajo de la línea de la señal puede indicar una señal de venta. El histograma, que muestra la diferencia entre el MACD y
#     la línea de la señal, puede ayudar a visualizar la fuerza de la tendencia.

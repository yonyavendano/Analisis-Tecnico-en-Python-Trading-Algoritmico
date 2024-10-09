# -*- coding: utf-8 -*-
# Importar librerías
import pandas as pd
import yfinance as yf
import mplfinance as mpf
import matplotlib.pyplot as plt
from copy import deepcopy

# Indicador: Bandas de Bollinger
def Bandas_Bollinger(df: pd.DataFrame, longitud: int = 20, std_dev: float = 2.0, ddof: int = 0, columna: str = "Close") -> pd.DataFrame:
    
    """
    Las Bandas de Bollinger son una herramienta de análisis técnico que ayuda a identificar condiciones de sobrecompra o sobreventa.
    Están compuestas por tres líneas: una media móvil simple (banda media) y dos bandas superior e inferior. Las bandas superior e
    inferior están típicamente a 2 desviaciones estándar +/- de una media móvil simple de 20 días.
    
    Cómo Operarlo:
        
        Cuando el precio rompe por debajo de la banda inferior, puede indicar que el activo ha caído demasiado y está en posición de
        rebotar. Por otro lado, cuando el precio rompe por encima de la banda superior, el mercado puede estar sobrecomprado y listo
        para una corrección. Utilizar las bandas como indicadores de sobrecompra/sobreventa se basa en el concepto de reversión a la
        media.
        
    -----------
    Parámetros:
    -----------
    param : pd.DataFrame : df : Datos históricos del instrumento financiero.
    -----------
    param : int : longitud : Ventana para realizar el cálculo de las BB (por defecto, se establece en 20).
    -----------
    param : float : std_dev : Número de desviaciones estándar a utilizar en el cálculo de las bandas (por defecto, se establece en 2.0).
    -----------
    param : int : ddof : Grados de libertad en las desviaciones estándar (por defecto, se establece en 0).
    -----------
    param : str : columna : Columna a utilizar en el cálculo (por defecto, se establece 'Close').
    -----------
    Salida:
    -----------
    return : pd.DataFrame : Cálculo de las Bandas de Bollinger.
    """
    
    data = deepcopy(df)
    rolling = data[columna].rolling(window=longitud, min_periods=longitud)
    data["MA"] = rolling.mean()
    calc_intermedio = std_dev * rolling.std(ddof=ddof)
    data["BB_Up"] = data["MA"] + calc_intermedio
    data["BB_Down"] = data["MA"] - calc_intermedio
    
    return data[["MA", "BB_Up", "BB_Down"]]

# Descargar datos
ticker = "PG"
df = yf.download(ticker, start="2022-06-01", end="2024-06-01")
    
# Calcular Indicador
bb_df = Bandas_Bollinger(df, longitud=20, std_dev=2.0)
    
# Crear el gráfico
add_plots = [
    
    mpf.make_addplot(bb_df["BB_Up"], color="red", linestyle="--", label="Banda Superior"),
    mpf.make_addplot(bb_df["BB_Down"], color="red", linestyle="--", label="Banda Inferior"),
    mpf.make_addplot(bb_df["MA"], color="blue", label="Media Móvil")
    
    ]

fig, ax = mpf.plot(df, type="candle", addplot=add_plots, style="yahoo", volume=True, returnfig=True, figscale=3.0)

fig.set_size_inches(22, 10)

ax[0].set_xlabel("Fecha", fontsize=14)
ax[0].set_ylabel("Precio", fontsize=14)
ax[0].set_title("Bandas de Bollinger", fontsize=16, weight="bold")

ax[0].legend(loc="lower right", fontsize=10)
ax[0].grid()
plt.show()

# Recordatorio:
#   - Las Bandas de Bollinger se basan en una media móvil y desviaciones estándar para medir la volatilidad e identificar
#     condiciones de sobrecompra y sobreventa.
#   - Una ruptura de la banda superior puede indicar un mercado sobrecomprado, mientras que una ruptura de la banda inferior
#     puede sugerir que el activo está sobrevendido.

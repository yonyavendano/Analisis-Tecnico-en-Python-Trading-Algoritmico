# -*- coding: utf-8 -*-
# Importar librerías
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# Indicador: Rango Porcentual de Williams
def Williams_PerR(df: pd.DataFrame, longitud: int = 14) -> pd.Series:
    
    """
    Williams %R, también conocido como el Rango Porcentual de Williams, es un tipo de indicador de momentum que se mueve entre 0 y -100
    y mide los niveles de sobrecompra y sobreventa. Una lectura por encima de -20 se considera sobrecomprada y una lectura por debajo
    de -80 se considera sobrevendida. Una lectura de sobrecompra o sobreventa no significa que el precio se revertirá. Sobrecompra 
    simplemente significa que el precio está cerca del máximo de su rango reciente y sobreventaa significa que el precio está en el 
    extremo inferior de su rango reciente.
    
    Cómo Operarlo:
        
        El comercio con Williams %R es bastante sencillo; se coloca una posición larga cuando el valor está por debajo de -80 y una posición
        corta cuando el valor está por encima de -20. Para evitar señales falsas, es mejor usarlo en combinación con otros indicadores.
        
    -----------
    Parámetros:
    -----------
    param : pd.DataFrame : df : Datos del instrumento financiero.
    -----------
    param : int : longitud : Ventana a utilizar en el cálculo de Williams %R (por defecto, se establece en 14).
    -----------
    Salida:
    -----------
    return : pd.Series : Cálculo de Williams %R.
    """
    
    # Calcular
    High = df["High"]
    maximo_rolling_H = High.rolling(window=longitud, min_periods=longitud).max()
    minimo_rolling_L = df["Low"].rolling(window=longitud, min_periods=longitud).min()
    William_R = -100 * ((maximo_rolling_H - df["Close"]) / (maximo_rolling_H - minimo_rolling_L))
    William_R.name = "Williams %R"
    
    return William_R

# Obtener Datos
ticker = "NKE"
df = yf.download(ticker, start="2021-01-01", end="2024-01-01", interval="1d")

# Calcular Indicador
williams_r_df = Williams_PerR(df)

# Graficar
plt.figure(figsize=(26, 13))
plt.subplot(2, 1, 1)
plt.plot(df.index, df["Close"], label="Precio de Cierre", color="gold", lw=3)
plt.title("Precio de Cierre para el activo:" + ticker)
plt.grid(True)
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(williams_r_df.index, williams_r_df, label="Williams %R", color="blue")
plt.axhline(y=-20, color="red", linestyle="--", label="SobreCompra (-20)")
plt.axhline(y=-80, color="green", linestyle="--", label="SobreVenta (-80)")
plt.title("Williams %R de:" + ticker)
plt.legend(loc="lower right", fontsize=15)

plt.tight_layout()
plt.show()

# Recordatorio:
#   - Williams %R mide los niveles de sobrecompra y sobreventa en un rango de -100 a 0.
#   - Lecturas por encima de -20 indican sobrecompra, mientras que lecturas por debajo de -80 indican sobreventa.
#   - Las líneas discontinuas en rojo y verde representan los niveles críticos de sobrecompra y sobreventa, respectivamente.

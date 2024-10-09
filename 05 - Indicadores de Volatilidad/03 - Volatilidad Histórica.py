# -*- coding: utf-8 -*-
# Importar librerías
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# Indicador: Volatilidad Histórica
def Volatilidad_Historica(df: pd.DataFrame, longitud: int = 10, columna: str = "Close") -> pd.Series:
    
    """
    La Volatilidad Histórica es un indicador que mide la desviación estándar de los rendimientos porcentuales
    de los precios de un activo durante un período de tiempo determinado. Este indicador refleja cómo fluctúan
    los precios de un activo en comparación con su media en un rango de tiempo específico.
    
    Cuando la volatilidad Histórica de un activo aumenta, indica que los precios están experimentando mayores 
    fluctuaciones de lo habitual, lo que puede ser un indicio de cambios importantes en el mercado. Por otro lado,
    una disminución en la volatilidad sugiere un retorno a la estabilidad o normalidad.
    
    Cómo Operarlo:
        
        La Volatilidad Histórica no es un indicador que genere señales de compra/venta por sí mismo, pero es una
        herramienta esencial para la gestión de riesgos. Puede ayudar a los operadores a determinar cuándo es más 
        seguro o más económico realizar operaciones, especialmente cuando se busca reducir costos de transacción o
        ajustar los niveles de stop-loss en función de la volatilidad actual del mercado.
        
    -----------
    Parámetros:
    -----------
    param : pd.DataFrame : df : Datos del activo.
    -----------
    param : int : longitud : Ventana para el cálculo de la Volatilidad Histórica (por defecto, se establece en 10).
    -----------
    param : str : columna : Columna a utilizar en el cálculo (por defecto, se establece en 'Close').
    -----------
    Salida:
    -----------
    return : pd.Series : Cálculo de la Volatilidad Histórica.
    """
    
    # Calcular
    precios = df[columna]
    volatilidad_historica = precios.pct_change().rolling(window=longitud, min_periods=longitud).std()
    volatilidad_historica.name = "Volatilidad Histórica"
    
    return volatilidad_historica
    
# Descargar datos
ticker = "WMT" 
df = yf.download(ticker, start="2022-01-01", end="2024-01-01")

# Calcular la Volatilidad Histórica
volatilidad_historica = Volatilidad_Historica(df, longitud=14)

# Calcular estadísticas de la volatilidad histórica
media_volatilidad = volatilidad_historica.mean()
desviacion_estandar_volatilidad = volatilidad_historica.std()
    
# Crear gráfico de la volatilidad histórica
fig, ax = plt.subplots(figsize=(22, 10))

# Graficar la volatilidad histórica
ax.plot(volatilidad_historica.index, volatilidad_historica, label="Volatilidad Histórica", color="blue", lw=2)

umbral_1 = media_volatilidad + 1 * desviacion_estandar_volatilidad
umbral_2 = media_volatilidad + 2 * desviacion_estandar_volatilidad
umbral_3 = media_volatilidad + 3 * desviacion_estandar_volatilidad

# Colorear las áreas de fondo por encima del promedio
ax.axhspan(media_volatilidad, umbral_1, color="yellow", alpha=0.3, label="1 Desviación Estándar arriba del promedio")
ax.axhspan(umbral_1, umbral_2, color="orange", alpha=0.5, label="2 Desviación Estándar arriba del promedio")
ax.axhspan(umbral_2, volatilidad_historica.max(), color="red", alpha=0.3, label="Más de 3 Desviación Estándar arriba del promedio")

# Colorear el fondo por debajo del promedio
ax.axhspan(volatilidad_historica.min(), media_volatilidad, color="green", alpha=0.5, label="Por debajo del promedio")

ax.set_xlabel("Fecha", fontsize=14)
ax.set_ylabel("Volatilidad Histórica", fontsize=14)
ax.set_title("Volatilidad Histórica de: " + ticker)
ax.grid()
ax.legend()
ax.set_ylim([volatilidad_historica.min(), volatilidad_historica.max()])
plt.show()
    
# Recordatorio:
#   - La Volatilidad Histórica mide la desviación estándar de los rendimientos porcentuales de un activo.
#   - Una mayor volatilidad indica fluctuaciones de precios más amplias, mientras que una menor volatilidad sugiere estabilidad.
#   - Es crucial para la gestión de riesgos, ayudando a ajustar estrategias de inversión y niveles de stop loss según la volatilidad
#     del mecado.

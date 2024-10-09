# -*- coding: utf-8 -*-
# Importar librerías
import pandas as pd
import numpy as np
import yfinance as yf
import mplfinance as mpf
import matplotlib.pyplot as plt

# Indicador: Estimador Nadaraya-Watson
def Estimador_Nadaraya_Watson(df: pd.DataFrame, longitud: int = 500, ancho_banda: float = 8.0, factor: float = 3.0,
                              columna: str = "Close") -> pd.DataFrame:
    
    """
    El Estimador Nadaraya-Watson es una técnica no paramétrica utilizada en la estimación de regresión, que sirve para suavizar
    una serie de datos. Se basa en el principio de promediar los valores observados en función de una distribución de pesos, donde
    los puntos más cercanos al valor que se está estimando reciben más peso que los puntos más lejanos. Esto se logra utilizando
    un núcleo (kernel) que asigna estos pesos, suavizando así las variaciones bruscas en los datos. En el contexto del análisis técnico,
    este estimador se aplica para identificar tendencias en los precios de activos financieros, permitiendo detectar posibles puntos
    de reversión. Al ajustar la banda de anchura, se controla el grado de suavidad de la estimación, lo que puede resultar en una 
    mayor o menor sensibilidad a las fluctuaciones del mercado, dependiendo de los parámetros utilizados.
    
    Cómo Operarlo:
        
        Operar con el Estimador NW se basa en observar los cambios de dirección en el estimador. Cuando la dirección del estimador
        cambia de negativa a positiva, se puede considerar una señal de compra, ya que sugiere un cambio hacia una tendencia 
        alcista. Por el contrario, cuando la dirección cambia de positiva a negativa, indica una posible reversión hacia una 
        tendencia bajista, lo que puede ser interpretado como una señal de venta.
        
    -----------
    Parámetros:
    -----------
    param : int : longitud : Determina el número de observaciones de precios recientes a utilizar para ajustar el Estimador NW
                             (por defecto, se establece en 500).
    -----------
    param : float : ancho_banda : Controla el grado de suavizado de los sobres. Valores más altos devuelven resultados más suaves
                                  (por defecto, se establece en 8.0).
    -----------
    param : float : factor : Controla el ancho del sobre (por defecto, se establece en 3.0).
    -----------
    param : str : columna : Columna del DataFrame que se utilizará para el cálculo del ENW (por defecto, se establece en 'Close').
    -----------
    Salida:
    -----------
    return : pd.DataFrame : DataFrame con el cálculo del Estimador de Nadaraya Watson.
    """
    
    # Calcular Indicador
    assert df.shape[0] >= longitud, "La longitud de los datos debe de ser >= longitud"
    precios = df[-longitud:][columna]
    filas = np.arange(0, longitud)
    # Calcular la matriz de pesos utilizando el Kernel Gaussiano
    matriz_pesos = np.array(np.exp(-np.power((np.matrix(filas).T - np.matrix(filas)), 2) / ((ancho_banda ** 2) * 2)))
    # Calcular el Estimador de NW
    suma_x = (matriz_pesos * np.tile(precios.values, (longitud, 1))).sum(axis=1)
    estimacion = suma_x / matriz_pesos.sum(axis=1)
    # Almacenar los resultados del estimador
    nwe = pd.DataFrame(data=estimacion, index=precios.index, columns=["Estimador"])
    
    # Calculaar la dirección del estimador
    direccion = nwe - nwe.shift(periods=1)
    direccion_shift = direccion.shift(periods=1)
    
    # Asignar etiquetas de dirección en base a los cambios
    nwe["Direccion_Estimador"] = np.where((direccion > 0) & (direccion_shift < 0), 1,
                                 np.where((direccion < 0) & (direccion_shift > 0), -1, np.nan))
    nwe["Direccion_Estimador"] = nwe["Direccion_Estimador"].shift(periods=-1)
    
    return nwe

# Obtener Datos Financieros
ticker = "SPY"
datos = yf.download(ticker, start="2022-01-01", end="2024-01-01", interval="1d")

# Calcular Estimador NW
nwe_resultados = Estimador_Nadaraya_Watson(datos)
    
# Filtrar Estimador según su dirección
nwe_positivo = nwe_resultados["Estimador"].where(nwe_resultados["Direccion_Estimador"].ffill() > 0, np.nan)
nwe_negativa = nwe_resultados["Estimador"].where(nwe_resultados["Direccion_Estimador"].ffill() < 0, np.nan) 
    
# Calcular puntos de cambio de dirección (alcista y bajista)
nwe_cambio_alcista = datos["Low"].where(nwe_resultados["Direccion_Estimador"] == 1, np.nan)[-500:] * 0.99 
nwe_cambio_bajista = datos["High"].where(nwe_resultados["Direccion_Estimador"] == -1, np.nan)[-500:] * 1.01 

graficos_nwe = [
    
    mpf.make_addplot(nwe_positivo, label="Estimador Positivo", color="green"),
    mpf.make_addplot(nwe_negativa, label="Estimador Negativo", color="red"),
    mpf.make_addplot(nwe_cambio_alcista, label="Señal Alcista", type="scatter", color="green", marker="^", markersize=100),
    mpf.make_addplot(nwe_cambio_bajista, label="Señal Bajista", type="scatter", color="red", marker="v", markersize=100)
    
    ]

fig, ax = mpf.plot(datos[-500:], type="candle", style="yahoo", volume=True, figsize=(22, 10), addplot=graficos_nwe, returnfig=True)
ax[0].legend(loc="lower left", fontsize=12)
plt.show()
    
# Recordatorio:
#   - El Estimador NW es un método de estimación no paramétrica. Se utiliza para suavizar datos y hacer predicciones sin asumir
#     una forma específica para la función subyacente que genera los datos. En lugar de basarse en un modelo paramétrico con un
#     número fijo de parámetros, el estimador de NW calcula una serie de promedios ponderados utilizando un kernel, lo que le permite
#     adaptarse de manera flexible a la estructura de los datos. Esto lo hace particularmente útil para situaciones en las que se desea
#     capturar patrones de datos ruidosos o con comportamientos no lineales.

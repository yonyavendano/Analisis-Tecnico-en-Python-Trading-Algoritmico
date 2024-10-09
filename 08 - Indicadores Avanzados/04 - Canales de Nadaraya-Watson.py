# -*- coding: utf-8 -*-
# Importar librerías
import pandas as pd
import numpy as np
import yfinance as yf
import mplfinance as mpf
import matplotlib.pyplot as plt

# Indicador: Nadaraya Watson Envelope
def Nadaraya_Watson_Envelope(df: pd.DataFrame, longitud: int = 500, ancho_banda: float = 8.0, factor: float = 3.0,
                             columna: str = "Close") -> pd.DataFrame:
    
    """
    El Envolvente Nadaraya-Watson es un indicador técnico que destaca los extremos de los precios dentro de una ventana de tiempo 
    seleccionada. Su función es identificar posibles puntos de reversión en el mercado al estimar la tendencia subyacente de los
    precios mediante un suavizado por núcleo. Este suavizado se realiza calculando una tendencia general a partir de los datos
    históricos y ajustando esta estimación con bandas que reflejan las desviaciones absolutas medias (MAE) desde la tendencia
    estimada.
    
    El cálculo de este indicador comienza con la estimación de la tendencia subyacente mediante la aplicación de una función de
    suavizado, como la gaussiana, que asigna diferentes pesos a las observaciones en función de su proximidad al punto de interés.
    Luego, se calculan dos bandas alrededor de esta tendencia: una banda superior y una banda inferior. La banda superior se obtiene
    sumando un múltiplo del MAE a la tendencia, mientras que la banda inferior se calcula restando este múltiplo. Estas bandas forman
    un canal que resalta los extremos de los precios, ayudando a identificar posibles señales de compra o venta.
    
    Cómo Operarlo:
        
        El Envolvente Nadaraya-Watson es útil para identificar posibles puntos de reversión cuando el precio cruza una de las bandas
        del envolvente. En general, cuando el precio cruza la banda superior, puede indicar una sobrecompra o un potencial cambio 
        en la tendencia hacia la baja. Por otro lado, un cruce por debajo de la banda inferior puede señalar una sobreventa o una
        posible reversión hacia una tendencia alcista.
        
    -----------
    Parámetros:
    -----------
    param : pd.DataFrame : df : Datos del mercado.
    -----------
    param : int : longitud : Determina el número de observaciones recientes de precios a utilizar para ajustar el Estimador NW
                             (por defecto, se establece en 500).
    -----------
    param : float : ancho_banda : Controla el grado de suavizado de los envolventes, con valores más altos dando como salida un resultado
                                  más suavizado (por defecto, se establece en 8.0).
    -----------
    param : float : factor : Controla el ancho de los envolventes (por defecto, se establece en 3.0).
    -----------
    param : str : columna : Columna a utilizar en el cálculo del Envolvente NW (por defecto, se establece en 'Close').
    -----------
    Salida:
    -----------
    return : pd.DataFrame : Cálculo del Envolvente de Nadaraya Watson.
    """
    
    # Calcular Bandas de NW
    assert df.shape[0] >= longitud, "La longitud del DataFrame debe de ser mayor o igual a la longitud especificada"
    
    # Seleccionar la columna de precios y preparar matrices
    precios_columna = df[-longitud:][columna]
    filas = np.arange(0, longitud)
    
    # Crear la matriz de pesos utilizando la función de suavizado por núcleo
    matriz_pesos = np.array(np.exp(-np.power((np.matrix(filas).T - np.matrix(filas)), 2) / ((ancho_banda ** 2) * 2)))
    
    # Calcular el estimador aplicando los pesos
    suma_x = (matriz_pesos * np.tile(precios_columna.values, (longitud, 1))).sum(axis=1)
    estimador_y2 = suma_x / matriz_pesos.sum(axis=1)
    
    # Almacenar los resultados
    envelope_df = pd.DataFrame(data=estimador_y2, index=precios_columna.index, columns=["Estimador"])
    
    # Calcular las bandas superior e inferior
    mae = (precios_columna - estimador_y2).abs().mean() * factor
    envelope_df["Banda_Superior"] = estimador_y2 + mae
    envelope_df["Banda_Inferior"] = estimador_y2 - mae
    
    # Determinar la dirección de las bandas
    precios_columna_desplzado = precios_columna.shift(periods=1)
    direccion_bandas = np.where(
        
        ((precios_columna_desplzado < (estimador_y2 - mae))) & ((precios_columna > (estimador_y2 - mae))), 1,
        np.where(((precios_columna_desplzado > (estimador_y2 + mae))) & ((precios_columna < (estimador_y2 + mae))), -1, np.nan)
        
        )
    envelope_df["Direccion_Bandas"] = direccion_bandas
    envelope_df["Direccion_Bandas"] = envelope_df["Direccion_Bandas"].shift(periods=-1)
    
    return envelope_df
    
# Obtener Datos
ticker = "AAPL"
df = yf.download(ticker, start="2022-01-01", end="2024-01-01", interval="1d")

# Calcular Indicador
nwe = Nadaraya_Watson_Envelope(df)
nwe_bajista = nwe["Direccion_Bandas"][nwe["Direccion_Bandas"] == -1]
nwe_alcista = nwe["Direccion_Bandas"][nwe["Direccion_Bandas"] == 1]

nwe_plots = [
    
    mpf.make_addplot(df["High"].where(df.index.isin(nwe_bajista.index), np.nan)[-500:] * 1.01, label="Señal Bajista", color="red",
                     type="scatter", marker="v", markersize=100),
    mpf.make_addplot(df["Low"].where(df.index.isin(nwe_alcista.index), np.nan)[-500:] * 0.99, label="Señal Alcista", color="green",
                     type="scatter", marker="^", markersize=100),
    mpf.make_addplot(nwe["Banda_Superior"], label="Banda Superior", color="green"),
    mpf.make_addplot(nwe["Banda_Inferior"], label="Banda Inferior", color="red")

    ]

mpf.plot(df[-500:], type="candle", style="yahoo", volume=True, figsize=(22, 10), addplot=nwe_plots, figscale=3.0, 
         title="Nadaraya-Watson Envoltura", panel_ratios=(3, 1))
plt.show()
    
# Recordatorio:
#   - El Envolvente de Nadaraya-Watson estima la tendencia de precios suavizando los datos con un núcleo, calculando la desviación media y
#     ajustando las bandas superior e inferior para identificar posibles puntos de reversión en el mercado.
#   - Las bandas superior e inferior del Envolvente de NW actúan como niveles dinámicos de soporte y resistencia. Los cruces del precio
#     con estas bandas pueden indicar señales de compra o venta, pero debemos esperar a que sean varias velas las que se encuentren
#     fuera de los canales de precios antes de tomar alguna decisión.

# -*- coding: utf-8 -*-
# Importar librerías
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

# Indicador: Flujo de Dinero de Chaikin (CMF)
def Flujo_Dinero_Chaikin(df: pd.DataFrame, longitud: int = 20) -> pd.Series:
    
    """
    Chaikin Money Flow (CMF) es un promedio ponderado por volumen de acumulación y distribución durante un periodo específicado.
    El principio detrás del CMF es que cuando más cerca está el precio del cierre del máximo, más acumulación ha tenido lugar.
    Por el contrario, cuando más ceca está el precio de cierre del mínimo, más distribución ha tenido lugar.
    Si el precio del activo cierra consistentemente por encima del punto medio de la barra con un volumen creciente, el CMF será positivo,
    pero si la acción del precio cierra consistentemente por debajo del punto medio de la barra con un volumen creciente, el CMF será negativo.
    
    Cómo Operarlo:
        
        Un valor de CMF por encima de la línea de cero es una señal de fortaleza en el mercado, y un valor por debajo de la línea de cero es una
        señal de debilidad en el mercado. Se recomienda esperar a que el CMF confirme la dirección de ruptura del activo a través de líneas
        de tendencia de soporte y resistenciaa. Por ejemplo, si un precio rompe hacia arriba a través de la resistencia, espera que el CMF tenga
        un valor positivo para confirmar la dirección de la ruptura.
        
        Una señal de venta del CMF ocurre cuando la acción del precio desarrolla un máximo más alto en zonas de sobrecompra, con el CMF divergiendo
        con un máximo más bajo y comenzando a caer.
        
        Una señal de compra del CMF ocurre cuando la acción del precio desarolla un mínimo más bajo en zonas de sobreventa, con el CMF divergiendo
        con un mínimo más alto y comenzando a subir.
        
    -----------
    Parámetros:
    -----------
    param : pd.DataFrame : df : Datos del activo.
    -----------
    param : int : length : Ventana a ser utilizada en el cálculo del CMF (por defecto, se establece en 20).
    -----------
    Salida:
    -----------
    return : pd.Series : Cálculo del Chaikin Money Flow.
    """
    
    # Calcular
    High, Low, Close = df["High"], df["Low"], df["Close"]
    MF = (((Close - Low) - (High - Close)) / (High - Low)) * df["Volume"]
    CMF = (MF.rolling(window=longitud, min_periods=longitud).sum() / df["Volume"].rolling(window=longitud, min_periods=longitud).sum())
    CMF.name = "CMF"
    
    return CMF
    
# Obtener Datos
ticker = "COIN"
df = yf.download(ticker, start="2022-01-01", end="2024-01-01")

# Calcular Indicador
cmf = Flujo_Dinero_Chaikin(df, longitud=20)
    
# Grafico
fig, ax = plt.subplots(figsize=(22, 7))

# Configurar los límites del gráfico
y_min, y_max = cmf.min(), cmf.max()

# Colorear el área del fondo
for i in range(len(cmf) - 1):
    if cmf.iloc[i] > 0:
        ax.axvspan(cmf.index[i], cmf.index[i + 1], ymin=0, ymax=1, color="lightgreen", alpha=0.5, zorder=-1)
    else:
        ax.axvspan(cmf.index[i], cmf.index[i + 1], ymin=0, ymax=1, color="lightcoral", alpha=0.5, zorder=-1)
        
# Graficar a nuestro Indicador
ax.plot(df.index, cmf, color="darkviolet", linestyle="--", linewidth=2, label="Chaikin Money Flow (CMF)")
ax.axhline(y = 0, color="gray", linestyle="--", linewidth=3.0, label="Línea de Cero")
ax.set_title("Chaikin Money Flow de:" + " " + ticker)
ax.legend(loc="upper left")
plt.tight_layout()
plt.show()
    
# Recordatorio:
#   - El CMF se utiliza para evaluar la acumulación y distribución de un activo, con valores positivos indicando acumulación y valores negativos
#     indicando distribución.
#   - La línea en cero actúa como referencia para la fortaleza o debilidad del mercado.
#   - Las señales de compra o venta se pueden confirmar observando la dirección del CMF en relación con el movimiento del precio.

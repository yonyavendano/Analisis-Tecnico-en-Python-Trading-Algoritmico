# -*- coding: utf-8 -*-
# Importar librerías
import pandas as pd
import numpy as np
import yfinance as yf
import mplfinance as mpf
import matplotlib.pyplot as plt

# Indicador: Canales de Trading de Tortuga
def Canales_Trading_Tortuga(df: pd.DataFrame, longitud_entrada: int = 20, longitud_salida: int = 10) -> pd.DataFrame:
    
    """
    El Indicador de Canales de Trading de Tortuga es un indicador técnico derivado de la famosa estrategia de trading de las Tortugas,
    un experimento realizado en los años 80 que demostró la eficacia de un enfoque sistemático para el trading. Este indicador traza
    dos canales en un gráfico: uno superior, que marca el nivel más alto alcanzado por el precio en un determinado número de períodos,
    y uno inferior, que marca el nivel más bajo. La estrategia sugiere comprar cuando el precio rompe por encima del canal superior
    y vender cuando cae por debajo del canal inferior, capturando así posibles tendencias emergentes.
    
    Cómo Operarlo:
        
        Para operar con el Indicador de Canales de Trading de Tortuga espera a que el precio rompa el canal superior o inferior.
        Si el precio supera el canal superior, entra en una posición larga, esperando que la tendencia continúe al alza. Si el precio
        cae por debajo del canal inferior, toma una posición corta, anticipando una tendencia bajista. Mantén la posición mientras el
        precio se mantenga en la dirección de la ruptura, y considera salir cuando el precio vuelva a entrar en el canal o se acerque
        al canal opuesto, lo que podría indicar un cambio de tendencia.
        
    -----------
    Parámetros:
    -----------
    param : pd.DataFrame : df : Datos de entrada (DataFrame con precios del activo).
    -----------
    param : int : longitud_entrada : Ventana para puntos de entrada (por defecto, se establece en 20).
    -----------
    param : int : longitud_salida : Ventana para puntos de salida (por defecto, se establece en 10).
    -----------
    Salida:
    -----------
    return : pd.DataFrame : Cálculo del Indicador de Canales de Trading de Tortuga.
    """
    
    # Calcular los niveles más altos y bajos durante las ventanas definidas
    High, Low = df["High"], df["Low"]
    entrada_low = Low.rolling(window=longitud_entrada, min_periods=longitud_entrada).min() # Mínimo para entrada
    entrada_high = High.rolling(window=longitud_entrada, min_periods=longitud_entrada).max() # Máximo para entrada
    salida_low = Low.rolling(window=longitud_salida, min_periods=longitud_salida).min() # Mínimo para salida
    salida_high = High.rolling(window=longitud_salida, min_periods=longitud_salida).max() # Máximo para salida
    
    # Contar condiciones de ruptura
    condicion_High = High >= entrada_high.shift(periods=1)
    condicion_Low = Low <= entrada_low.shift(periods=1)
    contador_high, contador_low = 0, 0
    lista_contador_high, lista_contador_low = [], []
    
    # Iterar sobre las condiciones para contar las barras desde la última señal
    for i in range(0, condicion_High.shape[0]):
        # Si se genera una ruptura superior, reiniciar el contador
        if condicion_High.iat[i]:
            contador_high = 0
            lista_contador_high.append(0)
        else:
            contador_high += 1
            lista_contador_high.append(contador_high)
        # Si se genera una ruptura inferior, reiniciar el contador
        if condicion_Low.iat[i]:
            contador_low = 0
            lista_contador_low.append(0)
        else:
            contador_low += 1
            lista_contador_low.append(contador_low)
            
    # Determinar cuál condición es válida para establecer las líneas de tendencia y salida
    condicion = np.array(lista_contador_high) <= np.array(lista_contador_low)
    K1 = np.where(condicion, entrada_low, entrada_high) # Línea de tedencia según la condición válida
    K2 = np.where(condicion, salida_low, salida_high) # Línea de salida según la condición válida
    
    # Definición de señales de compra y venta
    señal_compra = (High == entrada_high.shift(periods=1)) | \
        (np.where((High > entrada_high.shift(periods=1)) & (High.shift(periods=1) < entrada_high.shift(periods=2)), True, False))
    señal_venta = (Low == entrada_low.shift(periods=1)) | \
        (np.where((entrada_low.shift(periods=1) > Low) & (entrada_low.shift(periods=2) < Low.shift(periods=2)), True, False))
    salida_compra = (Low == salida_low.shift(periods=1)) | \
        (np.where((salida_low.shift(periods=1) > Low) & (salida_low.shift(periods=2) < Low.shift(periods=2)), True, False))
    salida_venta = (High == salida_high.shift(periods=1)) | \
        (np.where((High > salida_high.shift(periods=1)) & (High.shift(periods=1) < salida_high.shift(periods=2)), True, False))
        
    # Desplazar señales y salidas para el análisis
    señal_compra_desplazada = señal_compra.shift(periods=1)
    señal_venta_desplazada = señal_venta.shift(periods=1)
    salida_compra_desplazada = salida_compra.shift(periods=1)
    salida_venta_desplazada = salida_venta.shift(periods=1)
    
    # Inicializar contadores para las barras desde la última señal
    contador_O1, contador_O2, contador_O3, contador_O4 = 0, 0, 0, 0
    contador_E1, contador_E2, contador_E3, contador_E4 = 0, 0, 0, 0
    O1, O2, O3, O4 = [], [], [], []
    E1, E2, E3, E4 = [], [], [], []
    
    # Contar las barras desde la última señal de compra o venta
    for i in range(0, señal_compra.shape[0]):
        # Señal de Compra
        if señal_compra.iat[i]:
            contador_O1 = 0
            O1.append(0)
        else:
            contador_O1 += 1
            O1.append(contador_O1)
        # Señal de Venta
        if señal_venta.iat[i]:
            contador_O2 = 0
            O2.append(0)
        else:
            contador_O2 += 1
            O2.append(contador_O2)
        # Salida de Compra
        if salida_compra.iat[i]:
            contador_O3 = 0
            O3.append(0)
        else:
            contador_O3 += 1
            O3.append(contador_O3)
        # Salida de Venta
        if salida_venta.iat[i]:
            contador_O4 = 0
            O4.append(0)
        else:
            contador_O4 += 1
            O4.append(contador_O4)
            
        # Señal de Compra Desplazada
        if señal_compra_desplazada.iat[i]:
            contador_E1 = 0
            E1.append(0)
        else:
            contador_E1 += 1
            E1.append(contador_E1)
        # Señal de Venta Desplazada
        if señal_venta_desplazada.iat[i]:
            contador_E2 = 0
            E2.append(0)
        else:
            contador_E2 += 1
            E2.append(contador_E2)
        # Salida de Compra Desplazada
        if salida_compra_desplazada.iat[i]:
            contador_E3 = 0
            E3.append(0)
        else:
            contador_E3 += 1
            E3.append(contador_E3)
        # Salida de Venta Desplazada
        if salida_venta_desplazada.iat[i]:
            contador_E4 = 0
            E4.append(0)
        else:
            contador_E4 += 1
            E4.append(contador_E4)
            
    # Crear un DataFrame para almacenar las señales
    señales_df = pd.DataFrame(index=df.index)
    señales_df["O1"] = O1
    señales_df["O2"] = O2
    señales_df["O3"] = O3
    señales_df["O4"] = O4
    señales_df["E1"] = E1
    señales_df["E2"] = E2
    señales_df["E3"] = E3
    señales_df["E4"] = E4
       
    # Craer un DataFrame para los Canales de Trading de Tortuga
    TDC = pd.DataFrame(index=df.index)
    TDC["Superior"] = entrada_high   # Canal Superior
    TDC["Inferior"] = entrada_low    # Canal Inferior
    TDC["Linea_Tendencia"] = K1      # Línea de Tendencia
    TDC["Linea_Salida"] = K2         # Línea de Salida
    # Señales de Compra y Venta
    TDC["señal_compra"] = np.where(señal_compra & (señales_df["O3"] < señales_df["O1"].shift(periods=1)), entrada_low, np.nan)
    TDC["señal_venta"] = np.where(señal_venta & (señales_df["O4"] < señales_df["O2"].shift(periods=1)), entrada_high, np.nan)
    TDC["salida_compra"] = np.where(salida_compra & (señales_df["O1"] < señales_df["O3"].shift(periods=1)), entrada_high, np.nan)
    TDC["salida_venta"] = np.where(salida_venta & (señales_df["O2"] < señales_df["O4"].shift(periods=1)), entrada_high, np.nan)
    
    return TDC

# Descargar datos históricos
ticker = "AMZN"
df = yf.download(ticker, start="2022-01-01", end="2024-01-01")

# Calcular Indicador
tdc = Canales_Trading_Tortuga(df)
        
# Señal de Compra
compras = tdc[["señal_compra", "salida_compra"]].dropna(how="all")
# Omitir la primera fila por si se encuentra primera una salida de compra
compras = compras.iloc[1:] if pd.isna(compras["señal_compra"].iloc[0]) else compras

compras_copia = compras.copy() 
compras_copia["segundaFecha"] = compras_copia.index  
compras_copia[["salida_compra", "segundaFecha"]] = compras_copia.shift(periods=-1)[["salida_compra", "segundaFecha"]]  
compras_copia = compras_copia.dropna()    
    
# Llenar DataFrame con la Dirección de Compra (Tendencia Alcista)
tdc["DireccionCompra"] = 0
for i in range(compras_copia.shape[0]):
    tdc.loc[compras_copia.index[i]: compras_copia["segundaFecha"].iloc[i], "DireccionCompra"] = 1
    
# Si se generó una última señal de compra, pero sigue vigente, poner la fecha más reciente
if not pd.isna(compras["señal_compra"].iloc[-1]):
    tdc["DireccionCompra"].loc[compras.index[-1]:] = 1
    

# Señal de Venta
ventas = tdc[["señal_venta", "salida_venta"]].dropna(how="all")
# Omitir la primera fila por si se encuentra primero una salida de venta
ventas = ventas.iloc[1:] if pd.isna(ventas["señal_venta"].iloc[0]) else ventas

ventas_copia = ventas.copy() 
ventas_copia["segundaFecha"] = ventas_copia.index  
ventas_copia[["salida_venta", "segundaFecha"]] = ventas_copia.shift(periods=-1)[["salida_venta", "segundaFecha"]]  
ventas_copia = ventas_copia.dropna()    
    
# Llenar DataFrame con la Dirección de Venta (Tendencia Bajista)
tdc["DireccionVenta"] = 0
for i in range(ventas_copia.shape[0]):
    tdc.loc[ventas_copia.index[i]: ventas_copia["segundaFecha"].iloc[i], "DireccionVenta"] = 1
    
# Si se generó una última señal de venta, pero sigue vigente, poner la fecha más reciente
if not pd.isna(ventas["señal_venta"].iloc[-1]):
    tdc["DireccionVenta"].loc[ventas.index[-1]:] = 1
    
# Gráficos Adicionales
graficos_adicionales = [
    
    mpf.make_addplot(tdc[["Superior"]], color="blue", label="Superior", width=2, 
                     fill_between=dict(y1=tdc["Superior"].values, y2=tdc["Linea_Salida"].values, color="green", 
                                       where=(tdc["Superior"] > tdc["Linea_Salida"]) & (tdc["DireccionCompra"] == 1),
                                       facecolor="lightgreen", alpha=0.6)),
    mpf.make_addplot(tdc[["Inferior"]], color="blue", label="Inferior", width=2, 
                     fill_between=dict(y1=tdc["Linea_Salida"].values, y2=tdc["Inferior"].values, color="red", 
                                       where=(tdc["Linea_Salida"] > tdc["Inferior"]) & (tdc["DireccionVenta"] == 1),
                                       facecolor="lightcoral", alpha=0.6)),
    mpf.make_addplot(tdc["Linea_Salida"], color="blue", label="Linea de Salida", width=1.0, type="scatter", alpha=1.0),
    mpf.make_addplot(tdc["Linea_Tendencia"], color="red", label="Linea de Tendencia", width=2.0),
    mpf.make_addplot(df["High"].where(tdc.index.isin(compras_copia.index)) * 1.03, type="scatter", marker="^", markersize=100,
                     color="green", label="Entrada de Señales de Compra"),
    mpf.make_addplot(df["High"].where(tdc.index.isin(compras_copia["segundaFecha"])) * 1.03, type="scatter", marker="v", markersize=100,
                     color="green", label="Salida de Señales de Compra"),
    mpf.make_addplot(df["Low"].where(tdc.index.isin(ventas_copia.index)) * 0.97, type="scatter", marker="^", markersize=100,
                     color="red", label="Entrada de Señales de Venta"),
    mpf.make_addplot(df["Low"].where(tdc.index.isin(ventas_copia["segundaFecha"])) * 0.97, type="scatter", marker="v", markersize=100,
                     color="red", label="Salida de Señales de Venta")
    
    ]  
    
    
fig, ax = mpf.plot(df, type="candle", style="yahoo", volume=True, figsize=(22, 10), figscale=3.0, addplot=graficos_adicionales, returnfig=True)
plt.show() 
    
# Recordatorio:
#   - El indicador se basa en la estrategia de ruputura, donde se generan señales de compra cuando el precio supera el canal superior
#     y señales de venta cuando cae por debajo del canal inferior. Esta técnica busca capitalizar tendencias emergentes, facilitando
#     la identificación de puntos de entrada y salida efectivos en el mercado.
#   - Los canales superior e inferior actúan como niveles de soporte y resistencia dinámicos. Los traders pueden utilizar estos niveles
#     para establecer órdenes de stop-loss o para planificar salidas, mejorando la gestión de riesgo y la efectividad en sus decisiones.

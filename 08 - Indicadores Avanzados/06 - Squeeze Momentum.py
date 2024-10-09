# -*- coding: utf-8 -*-
# Importar librerías
import pandas as pd
import numpy as np
from copy import deepcopy
import yfinance as yf
import matplotlib.pyplot as plt

# Indicador: Squeeze Momentum
def Squeeze_Momentum(df: pd.DataFrame, longitud_bb: int = 20, desviacion_std_bb: float = 2.0, longitud_kc: int = 20, multiplicador_kc: float = 1.5,
                     periodos_momentum: int = 12, longitud_momentum: int = 6, columna: str = "Close") -> pd.DataFrame:
    
    """
    El indicador Squeeze Momentum es una herramienta técnica que detecta períodos de baja volatilidad y consolidación en los mercados
    financieros, cuando el precio está 'oprimido' en un rango estrecho. Utiliza Bandas de Bollinger y Canales de Keltner para identificar
    estas fases de compresión. Cuando el precio rompe fuera de este rango, el indicador sugiere un posible cambio en la tendencia. El 
    histograma del Squeeze Momentum muestra la fuerza y dirección del movimiento después de una consolidación, ayudando a los traders a
    identificar oportunidades de entrada y salida basadas en la expansión de la volatilidad.
    
    Cómo Operarlo:
        
        Si el histograma está por encima de cero, se debe abrir una posición larga; si está por debajo de cero, se debe abrir una posición
        corta. El movimiento promedio dura entre 8 y 10 barras.
        
        Si los movimientos en diferentes marcos de tiempo coinciden, se intensifican las señales.
        
        Para salir de la posición, se pueden usar niveles de Fibonacci y Soporte y Resistencia.
        
        A pesar de la indicación simple en forma de color del histograma, los traders pueden experimentar dificultades en identificar la
        dirección en la que se moverá el precio después de una ruptura. Por eso, es recomendable aplicar filtros adicionales para identificar
        la dirección del comercio, como el indicador ADX:
            
            - Si +DMI está por encima de -DMI, se trata de una tendencia alcista y si el -DMI está por encima de +DMI, se trata de una 
            tendencia bajista.
        
    -----------
    Parámetros:
    -----------
    param : pd.DataFrame : df : Datos financieros.
    -----------
    param : int : longitud_bb : Ventana a usar de BB para el cálculo del SM (por defecto, se establece en 20).
    -----------
    param : float : desviacion_std_bb : Número de desviaciones estándar para BB en el cálculo del SM (por defecto, se establece en 2.0).
    -----------
    param : int : longitud_kc : Ventana a usar de KC par el cálculo del SM (por defecto, se establece en 20).
    -----------
    param : float : multiplicador_kc : Multiplicador para KC en el cálculo del SM (por defecto, se establece en 1.5).
    -----------
    param : int : periodos_momentum : Períodos para el cálculo del SM (por defecto, se establece en 12).
    -----------
    param : int : longitud_momentum : Ventana a usar en el Momentum para el cálculo del SM (por defecto, se establece en 6).
    -----------
    param : str : columna : Columna a usar en el cálculo del SM (por defecto, se establece en 'Close').
    -----------
    Salida:
    -----------
    return : pd.DataFrame : Cálculo del Squeeze Momentum.
    """
    
    # Calcular
    df = deepcopy(df)
    
    # Calcular Bandas de Bollinger
    rolling = df[columna].rolling(window=longitud_bb, min_periods=longitud_bb)
    df["MA"] = rolling.mean()
    calc_intermedio = desviacion_std_bb * rolling.std()
    df["BB_Up"] = df["MA"] + calc_intermedio
    df["BB_Lw"] = df["MA"] - calc_intermedio
    
    # Calcular Canales de Keltner
    EMA = df[columna].ewm(span=longitud_kc, min_periods=longitud_kc, adjust=False).mean()
    
    # Subpaso: Calcular Indicador TR
    High, Low = df["High"], df["Low"]
    H_minus_L = High - Low
    prev_cl = df["Close"].shift(periods=1)
    H_minus_PC = abs(High - prev_cl)
    L_minus_PC = abs(prev_cl - Low)
    TR = pd.Series(np.max([H_minus_L, H_minus_PC, L_minus_PC], axis=0), index=df.index, name="TR")
    TR_EMA = TR.ewm(span=longitud_kc, min_periods=longitud_kc, adjust=True).mean()
    
    # Cálculo de las Bandas de Keltner
    Banda_KC_Media_Alta = EMA + multiplicador_kc * TR_EMA
    Banda_KC_Media_Baja = EMA - multiplicador_kc * TR_EMA
    KC = pd.concat([Banda_KC_Media_Alta, EMA, Banda_KC_Media_Baja], axis=1)
    KC.columns = ["Banda_KC_Media_Alta", "EMA", "Banda_KC_Media_Baja"]
    
    # Calcular el Indicador de Squeeze Momentum
    squeeze = df["Close"].diff(periods=periodos_momentum).rolling(window=longitud_momentum, min_periods=longitud_momentum).mean()
    
    # Verificar las bandas para obtener distintas condiciones de Squeeze
    func_on = (df["BB_Lw"] > KC["Banda_KC_Media_Baja"]) & (df["BB_Up"] < KC["Banda_KC_Media_Alta"])
    func_off = (df["BB_Lw"] < KC["Banda_KC_Media_Baja"]) & (df["BB_Up"] > KC["Banda_KC_Media_Alta"])
    no_squeeze = ~func_on & ~func_off
    
    # Concatenar los resultados
    SQM = pd.concat([squeeze, func_on, func_off, no_squeeze], axis=1)
    SQM.columns = ["SQZ", "SQZ_ON", "SQZ_OFF", "SQZ_NO"]

    return SQM

# Descargar datos
ticker = "AMZN"
df = yf.download(ticker, start="2018-01-01", end="2024-01-01")

# Calcular Indicador
sq = Squeeze_Momentum(df)

# Plot Indicador
fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(36, 12))

# "SQZ" (Squeeze Momentum):
    
# Significado: Representa el valor del histograma del Squeeze Momentum. Este valor indica la fuerza del movimiento del precio.

# Interpretación: Un valor positivo indica un movimiento al alza, mientras que un valor negativo indica un movimiento a la baja.

# Plot Squeeze
Squeeze_Momentum_Completo = sq.dropna()
index = Squeeze_Momentum_Completo.index
for i in range(Squeeze_Momentum_Completo.shape[0]):
    ax[0, 0].bar(index[i], Squeeze_Momentum_Completo.iat[i, 0],
                 color="#33FF5B" if Squeeze_Momentum_Completo.iat[i, 0] > 0 else "red")
ax0 = ax[0, 0].twinx()
ax0.plot(df["Close"])
ax[0, 0].set_title("Squeeze Momentum Completo", size=20)
ax[0, 0].grid(axis = "y")

# "SQZ_ON" (Squeeze Momentum Activado):
    
# Significado: Esta columna indica cuando el mercado está en un período de baja volatilidad, es decir, cuando las Bandas de Bollinger
# están dentro de las Bandas de Keltner.

# Interpretación: Un valor de True en esta columna sugiere que el mercado está en una fase de compresión, y es probable que se esté
# preparando para un movimiento significativo (es decir, una ruptura).

# Plot Squeeze
Squeeze_Momentum_ON = sq[sq["SQZ_ON"]]
index = Squeeze_Momentum_ON.index
for i in range(Squeeze_Momentum_ON.shape[0]):
    ax[0, 1].bar(index[i], Squeeze_Momentum_ON.iat[i, 0],
                 color="#33FF5B" if Squeeze_Momentum_ON.iat[i, 0] > 0 else "red")
ax1 = ax[0, 1].twinx()
ax1.plot(df["Close"])
ax[0, 1].set_title("Squeeze Momentum ON Activado", size=20)
ax[0, 1].grid(axis = "y")

# "SQZ_OFF" (Squeeze Momentum Desactivado):
    
# Significado: Indica cuando el mercado ha salido de la fase de compresión, es decir, cuando las Bandas de Bollinger
# se encuentran fuera de las Bandas de Keltner.

# Interpretación: Un Valor True en esta columna sugiere que el mercado ha comenzado un movimiento significativo, ya sea
# a la alza o a la baja, y la fase de compresión ha terminado.
    
# Plot Squeeze
Squeeze_Momentum_OFF = sq[sq["SQZ_OFF"]]
index = Squeeze_Momentum_OFF.index
for i in range(Squeeze_Momentum_OFF.shape[0]):
    ax[1, 0].bar(index[i], Squeeze_Momentum_OFF.iat[i, 0],
                 color="#33FF5B" if Squeeze_Momentum_OFF.iat[i, 0] > 0 else "red")
ax2 = ax[1, 0].twinx()
ax2.plot(df["Close"])
ax[1, 0].set_title("Squeeze Momentum OFF Desactivado", size=20)
ax[1, 0].grid(axis = "y")

# "SQZ_NO" (Sin Squeeze):
    
# Significado: Esta columna muestra cuando no hay condiciones de squeeze en el mercado, es decir, cuando las Bandas de Bollinger
# no están completamente dentro ni fuera de las Bandas de Keltner.

# Interpretación: Un valor True en esta columna indica que el mercado no se encuentra ni en una fase de compresión ni ha salido
# recientemente de una. Se puede considerar como un estado neutral o de transición.
    
# Plot Squeeze
Squeeze_Momentum_NO = sq[sq["SQZ_NO"]]
index = Squeeze_Momentum_NO.index
for i in range(Squeeze_Momentum_NO.shape[0]):
    ax[1, 1].bar(index[i], Squeeze_Momentum_NO.iat[i, 0],
                 color="#33FF5B" if Squeeze_Momentum_NO.iat[i, 0] > 0 else "red")
ax3 = ax[1, 1].twinx()
ax3.plot(df["Close"])
ax[1, 1].set_title("NO Squeeze Momentum", size=20)
ax[1, 1].grid(axis = "y")

plt.show()

# Recordatorio:
#   - El Indicador de SM es eficaz para detectar períodos en los que el mercadao están en compresión o baja volatilidad (SQZ_ON). Estos períodos
#     suelen preceder a movimientos significativos, lo que permite a los traders prepararse para rupturas inminentes.

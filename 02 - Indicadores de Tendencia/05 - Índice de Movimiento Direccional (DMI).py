# -*- coding: utf-8 -*-
# Importar librerías
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np

# Indicador: Índice de Movimiento Direccional
def Indice_Movimiento_Direccional(df: pd.DataFrame, suavizado_ADX: int = 14, longitud_DI: int = 14) -> pd.DataFrame:
    
    """
    El Índice de Movimiento Direccional (DMI) es un indicador que identifica en qué dirección se está moviendo el precio
    de un activo. El indicador hace esto comparando los máximos y mínimos previos y dibujando dos líneas: una línea de 
    movimiento direccional positivo (+DI) y una línea de movimiento direccional negativo (-DI). Se añade una tercera línea,
    llamada Índice Direccional Promedio (ADX), para medir la fuerza de la tendencia alcista o bajista.
    
    Cómo Operarlo:
        
        Cuando +DI está por encima de -DI, hay más presión alcista que bajista en el precio. Por el contrario, si -DI está
        por encima de +DI, entonces hay más presión bajista sobre el precio. Este indicador puede ayudar a evaluar la 
        dirección de la tendencia. Los cruces entre las líneas también se utilizan a veces como señales de compra o venta.
        
    -----------
    Parámetros:
    -----------
    param : pd.DataFrame : df : Datos históricos del instrumento financiero.
    -----------
    param : int : suavizado_ADX : Ventana a utilizar en el cálculo de los Movimientos Direccionales (+DM y -DM) (por defecto, se establece en 14).
    -----------
    param : int : longtiud_DI : Ventana a utilizar en el cálculo de los Indicadores Direccionales (+DI y -DI) (por defecto, se establece en 14).
    -----------
    Salida:
    -----------
    return : pd.DataFrame : Cálculo del Índice de Movimiento Direccional.
    """
    
    # Calcular el Rango Verdadero
    High, Low = df["High"], df["Low"]
    H_minus_L = High - Low
    prev_clo = df["Close"].shift(periods=1)
    H_minus_PC = abs(High - prev_clo)
    L_minus_PC = abs(prev_clo - Low)
    TR = pd.Series(np.max([H_minus_L, H_minus_PC, L_minus_PC], axis=0), index=df.index, name="TR")
    
    # Calcular los Movimientos Direccionales (+DM y -DM)
    pre_PDM = df["High"].diff().dropna()
    pre_MDM = df["Low"].diff(periods=-1).dropna()
    plus_DM = pre_PDM.where((pre_PDM > pre_MDM.values) & (pre_PDM > 0), 0)
    minus_DM = pre_MDM.where((pre_MDM > pre_PDM.values) & (pre_MDM > 0), 0)
    
    # Calcular los valores iniciales para las sumas suavizadas de TR, +DM, -DM
    TRL = [np.nansum(TR[:suavizado_ADX + 1])]
    PDML = [plus_DM[:suavizado_ADX].sum()]
    MDML = [minus_DM[:suavizado_ADX].sum()]
    factor = 1 - 1 / suavizado_ADX

    # Calcular las sumas suavizadas de TR, +DM y -DM utilizando el método Wilder
    for i in range(0, int(df.shape[0] - suavizado_ADX - 1)):
        TRL.append(TRL[i] * factor + TR[suavizado_ADX + i + 1])
        PDML.append(PDML[i] * factor + plus_DM[suavizado_ADX + i])
        MDML.append(MDML[i] * factor + minus_DM[suavizado_ADX + i])
        
    # Calcular los Indicadores Direccionales (+DI y -DI)
    PDI = np.array(PDML) / np.array(TRL) * 100
    MDI = np.array(MDML) / np.array(TRL) * 100
    # Calcular el Indice Direccional (DX)
    DX = np.abs(PDI - MDI) / (PDI + MDI) * 100
    ADX = [DX[:suavizado_ADX].mean()]
    
    # Calcular el Índice Direccional Promedio (ADX) utilizando la longitud_DI
    _ = [ADX.append((ADX[i] * (longitud_DI - 1) + DX[longitud_DI + i])/longitud_DI) for i in range(int(len(DX) - longitud_DI))]
    ADXI = pd.DataFrame(PDI, columns=["+DI"], index=df.index[-len(PDI):])
    ADXI["-DI"] = MDI
    ADX = pd.DataFrame(ADX, columns=["ADX"], index=df.index[-len(ADX):])
    
    return ADX.merge(ADXI, how="outer", left_index=True, right_index=True)

# Obtener Datos
df = yf.download("SQ", start="2025-01-01", end="2025-07-01", interval="1d", multi_level_index=False)

# Calcular Indicador
dmi = Indice_Movimiento_Direccional(df, suavizado_ADX=14, longitud_DI=14)

# Graficar Indicador
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(22, 8), sharex=True)

# Graficar el Índice Direccional (+DI y -DI)
ax.plot(dmi.index, dmi["+DI"], label="+DI", color="blue")
ax.plot(dmi.index, dmi["-DI"], label="-DI", color="red")
ax.plot(dmi.index, dmi["ADX"], label="ADX", color="green")

ax.fill_between(dmi.index, y1=0, y2=dmi["+DI"], where=(dmi["+DI"] > dmi["-DI"]), color="lightblue", alpha=0.5)
ax.fill_between(dmi.index, y1=0, y2=dmi["-DI"], where=(dmi["+DI"] < dmi["-DI"]), color="lightcoral", alpha=0.5)
ax.legend(fontsize=15, loc="upper right")
ax.set_title("Índice de Movimiento Direccional (+DI, -DI y ADX)", size=20, fontweight="bold")
ax.grid(True)

plt.tight_layout()
plt.show()

# Recordatorio:
#   - El ADX solo mide la fuerza de la tendencia y no su dirección. Un valor alto de ADX indica una tendencia fuerte, ya sea alcista o bajista.
#   - Los cruces entre +DI y -DI pueden ser señales de compra o venta, pero siempre es recomendable utilizarlos jutno con otros indicadores
#     para evitar señales falsas.

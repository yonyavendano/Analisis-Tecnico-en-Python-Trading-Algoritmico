# -*- coding: utf-8 -*-
# Importar librerías
import pandas as pd
import numpy as np
from copy import deepcopy
import yfinance as yf
import mplfinance as mpf
import matplotlib.pyplot as plt

# Indicador: Chandelier Exit
def Chandelier_Exit(df: pd.DataFrame, CE_longitud: int = 22, ATR_longitud: int = 22, multiplicador: float = 3.0) -> pd.DataFrame:
    
    """
    El Chandelier Exit es un indicador técnico diseñado para gestionar el riesgo en el trading. Utiliza el Rango Verdadero Promedio (ATR)
    para ajustar dinámicamente los niveles de stop-loss según la volatilidad del mercado. Para posiciones largas, el nivel de stop-loss
    se calcula restando el ATR multiplicado por un factor específico del máximo de los precios altos en una venta de tiempo. Para
    posiciones cortas, se suma el ATR al mínimo de los precios bajos. Este enfoque ayuda a proteger las ganancias y limitar las pérdidas,
    adaptándose a los cambios en la volatilidad del activo.
    
    Cómo Operarlo:
        
        Para operar con el CE, se debe observar el indicador en combinación con la dirección de la tendencia. En una tendencia alcista,
        se utiliza el nivel de stop-loss superior para proteger las ganancias; se realiza una compra cuando el precio supera este nivel.
        En una tendencia bajista, el nivel de stop-loss inferior se usa para limitar las pérdidas; se realiza una venta cuando el precio
        cae por debajo de este nivel. Las señales de compra y venta se generan cuando el precio cruza estos niveles de stop.
        
    -----------
    Parámetros:
    -----------
    param : pd.DataFrame : df : Datos del activo financiero.
    -----------
    param : int : CE_longitud : Ventana a usar en el cálculo del CE (por defecto, se establece en 22).
    -----------
    param : int : ATR_longitud : Ventana a usar en el cálculo del ATR (por defecto, se establece en 22).
    -----------
    param : float : multiplicador : Multiplicador del ATR para el cálculo del CE (por defecto, se establece en 3.0).
    -----------
    Salida:
    -----------
    return : pd.DataFrame : Cálculo del Chandelier Exit.
    """
    
    # Calcular
    data = deepcopy(df)
    # Calcular ATR
    High, Low = data["High"], data["Low"]
    H_minus_L = High - Low
    prev_cl = df["Close"].shift(periods=1)
    H_minus_PC = abs(High - prev_cl)
    L_minus_PC = abs(prev_cl - Low)
    TR = pd.Series(np.max([H_minus_L, H_minus_PC, L_minus_PC], axis=0), index=df.index, name="TR")
    ATR = TR.ewm(alpha=1/ATR_longitud, min_periods=ATR_longitud, adjust=False).mean()
    
    data["Chand_Exit_Long"] = High.rolling(window=CE_longitud, min_periods=CE_longitud).max() - multiplicador * ATR
    data["Chand_Exit_Short"] = Low.rolling(window=CE_longitud, min_periods=CE_longitud).min() + multiplicador * ATR
    
    # Incorporar Señal
    long_stop_prev = data["Chand_Exit_Long"].shift(periods=1)
    short_stop_prev = data["Chand_Exit_Short"].shift(periods=1)
    
    # Actualizar los stops basados en las condiciones
    data["long_stop"] = np.where(data["Close"].shift(periods=1) > long_stop_prev,
                                 np.maximum(data["Chand_Exit_Long"], long_stop_prev), data["Chand_Exit_Long"])
    data["short_stop"] = np.where(data["Close"].shift(periods=1) < short_stop_prev,
                                  np.minimum(data["Chand_Exit_Short"], short_stop_prev), data["Chand_Exit_Short"])
    
    # Determinar la dirección
    data["dir"] = np.where(data["Close"] > short_stop_prev, 1, np.where(data["Close"] < long_stop_prev, -1, np.nan))
    data["dir"] = data["dir"].ffill().fillna(1)
    
    # Generar las señales de compra y venta
    data["buy_signals"] = (data["dir"] == 1) & (data["dir"].shift(periods=1) == -1)
    data["sell_signals"] = (data["dir"] == -1) & (data["dir"].shift(periods=1) == 1)
    
    return data[["Chand_Exit_Long", "Chand_Exit_Short", "dir", "buy_signals", "sell_signals"]]

# Descargar los datos históricos
ticker = "AMZN"
df = yf.download(ticker, start="2022-01-01", end="2024-01-01")

# Calcular CE
ce = Chandelier_Exit(df)
    
# Señales
señal_bajista = ce["sell_signals"][ce["sell_signals"]]
señal_alcista = ce["buy_signals"][ce["buy_signals"]]

# Crear plots adicionales
addplots = [
    
    mpf.make_addplot(ce["Chand_Exit_Long"].where(ce["dir"] == 1, np.nan), panel=0, color="green", width=3, label="Chandelier Exit Long"),
    mpf.make_addplot(ce["Chand_Exit_Short"].where(ce["dir"] == -1, np.nan), panel=0, color="red", width=3, label="Chandelier Exit Short"),
    mpf.make_addplot(ce["Chand_Exit_Long"].where(df["High"].index.isin(señal_alcista.index.tolist()), np.nan) * 0.97, panel=0, color="green",
                     marker="^", markersize=100, type="scatter"),
    mpf.make_addplot(ce["Chand_Exit_Short"].where(df["Low"].index.isin(señal_bajista.index.tolist()), np.nan) * 1.03, panel=0, color="red",
                     marker="v", markersize=100, type="scatter")
    
    ]

mpf.plot(df, type="candle", style="yahoo", volume=True, addplot=addplots, figsize=(25, 10), title="Precios, Volumen e Indicador Chandelier Exit",
         warn_too_much_data=df.shape[0], ylabel="Precio", ylabel_lower="Volumen", panel_ratios=(2, 1), returnfig=True)
plt.show()
    
# Recordatorio:
#   - El CE ofrece señales claras para entrar o salir del mercado, utilizando niveles de salida largos y cortos basados en la volatilidad del mercado.
#   - Las líneas del indicador se ajustan dinámicamente en función de la volatilidad del mercado, actuando como barreras que protegen ganancias y limitan
#     pérdidas según en el movimiento del mercado.
#   - El indicador adapta sus niveles de salida en respuesta a cambios en la tendencia del mercado, permitiendo una estrategia de trading flexible y eficiente
#     para diferentes condiciones de mercado.

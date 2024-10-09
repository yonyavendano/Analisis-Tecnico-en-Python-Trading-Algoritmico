# -*- coding: utf-8 -*-
# Importar librerías
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# Indicador: Índice de Flujo de Dinero
def Indice_Flujo_Dinero(df: pd.DataFrame, longitud: int = 14) -> pd.Series:
    
    """
    El Índice de Flujo de Dinero (MFI) es un indicador técnico que genera señales de sobrecompra o sobreventa utilizando tanto datos de
    precios como de volumen. También se puede utilizar para detectar divergencias que adviertan de un cambio de tendencia en el precio.
    A diferencia de los osciladores convencionales como el Índice de Fuerza Relativa (RSI), el MFI incorpora datos de precios y volumen,
    en lugar de solo precios.
    
    Cómo Operarlo:
        
        Un valor por encima de 80 se considera sobrecomprado y un valor por debajo de 20 se considera sobrevendido, aunque los niveles
        de 90 y 10 también se utilizan como umbrales.
        
        Una divergencia entre el indicador y el precio es notable. Por ejemplo, si el indicador está subiendo mientras el precio está
        bajando o se mantiene plano, el precio podría comenzar a subir.
        
    -----------
    Parámetros:
    -----------
    param : pd.DataFrame : df : Datos del instrumento.
    -----------
    param : int : longitud : Ventana a ser utilizado en el cálculo del MFI (por defecto, se establece en 14).
    -----------
    Salida:
    -----------
    return : pd.Series : Cálculo del MFI.
    """
    
    # Calcular
    precio_tipico = (df["High"] + df["Low"] + df["Close"]) / 3
    diferencia = precio_tipico.diff(periods=1)
    flujo_dinero_bruto = precio_tipico * df["Volume"]
    razon_flujo_dinero = flujo_dinero_bruto.where(diferencia >= 0, 0).rolling(window=longitud, min_periods=longitud).sum() / \
                         flujo_dinero_bruto.where(diferencia <= 0, 0).rolling(window=longitud, min_periods=longitud).sum()
    Indice_FD = 100 - 100 / (1 + razon_flujo_dinero)
    Indice_FD.name = "MFI"
    
    return Indice_FD

# Obtener Datos
ticker = "COST"
df = yf.download(ticker, start="2020-01-01", end="2024-01-01")

# Calculo del Indicador
mfi = Indice_Flujo_Dinero(df, longitud=14)

# Grafico
fig, ax = plt.subplots(figsize=(22, 8))

# Graficar el Money Flow Index
ax.plot(mfi.index, mfi, color="teal", linestyle="--", linewidth=2, label="Money Flow Index")
ax.axhline(y=80, color="red", linestyle="--", label="Sobrecomprado")
ax.axhline(y=20, color="green", linestyle="--", label="Sobrevendido")
ax.axhline(y=50, color="grey", linestyle="--", label="Nivel Neutro")

ax.set_xlabel("Fecha", fontsize=14)
ax.set_ylabel("MFI", fontsize=14, color="teal")
ax.set_title("Índice de Flujo de Dinero (MFI): " + ticker)
ax.legend(loc="upper left", fontsize=10)
ax.grid(True)
ax.set_facecolor("#f5f5f5")

plt.tight_layout()
plt.show()

# Recordatorio:
#   - El MFI se utiliza para identificar condiciones de sobrecompra (valor > 80) y sobreventa (valor < 20) del activo.
#   - Los niveles extremos en el MFI pueden señalar correcciones o cambios en la tendencia del activo.
#   - La línea en 50 sirve como nivel neutro para evaluar el equilibrio entre el flujo de dinero positivo y negativo.
#   - Las divergencias entre el MFI y el precio pueden indicar posibles reversiones de la tendencia.

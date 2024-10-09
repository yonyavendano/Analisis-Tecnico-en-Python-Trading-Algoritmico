# -*- coding: utf-8 -*-
# Importar librerías
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# Indicador: Nube de Ichimoku
def Ichimoku_Cloud(df: pd.DataFrame, periodo_tenkan: int = 9, periodo_kijun: int = 26, offset: bool = False) -> pd.DataFrame:
    
    """
    El Ichimoku Cloud es una colección de indicadores técnicos que muestran niveles de soporte y resistencia, así como 
    dirección y momento de la tendencia. Calcula múltiples promedios y traza una "nube" para pronostricar dónde el precio
    puede encontrar soporte o resistencia en el futuro.
    
    Cómo Operarlo:
        
        La tendencia general es alcista cuando el precio está por encima de la nube (posiciones largas), bajista cuando
        el precio está por debajo de la nube (posiciones cortas) y sin tendencia o en transición cuando el precio está en 
        la nube.
        
        Cuando el Span A (Senkou Span A) está en aumento y por encima del Span B (Senkou Span B), esto ayuda a confirmar la
        tendencia alcista y el espacio entre las líneas se colorea típicamente de verde. Cuando el Span A está en disminución
        y por debajo del Span B, esto confirma la tendencia bajista y el espacio entre las líneas se colorea de rojo.
        
    -----------
    Parámetros:
    -----------
    param : pd.DataFrame : df : Datos del activo.
    -----------
    param : int : periodo_tenkan : Ventana a utilizar en el cálculo de Ichimoku Cloud (por defecto, se establece en 9).
    -----------
    param : int : periodo_kijun : Ventana a utilizar en el cálculo de Ichimoku Cloud (por defecto, se establece en 26).
    -----------
    param : bool : offset : Mostrar datos desplazados (por defecto, se establece en False).
    -----------
    Salida:
    -----------
    return : pd.DataFrame : Cálculo del Ichimoku Cloud.
    """
    
    # Calcular
    High, Low = df["High"], df["Low"]
    
    # Tenkan Sen: Línea de Señal a corto plazo
    rolling_min_tenkan = Low.rolling(window=periodo_tenkan, min_periods=periodo_tenkan).min()
    rolling_max_tenkan = High.rolling(window=periodo_tenkan, min_periods=periodo_tenkan).max()
    tenkan_sen = (rolling_max_tenkan + rolling_min_tenkan) / 2
    
    # Kijun Sen: Línea de señal a largo plazo
    rolling_min_kijun = Low.rolling(window=periodo_kijun, min_periods=periodo_kijun).min()
    rolling_max_kijun = High.rolling(window=periodo_kijun, min_periods=periodo_kijun).max()
    kijun_sen = (rolling_max_kijun + rolling_min_kijun) / 2
    
    # Senkou Span A - Nube
    senkou_span_a = ((tenkan_sen + kijun_sen) / 2)
    
    # Senkou Span B - Nube
    rolling_min_senkou = Low.rolling(window=periodo_kijun * 2, min_periods=periodo_kijun * 2).min()
    rolling_max_senkou = High.rolling(window=periodo_kijun * 2, min_periods=periodo_kijun * 2).max()
    senkou_span_b = ((rolling_min_senkou + rolling_max_senkou) / 2)
    
    # Chikou Span: Línea de confirmación
    chikou_span = df["Close"].shift(periods=-periodo_kijun)
    
    # Crear un DataFrame con los resultados
    IC = pd.concat([tenkan_sen, kijun_sen, senkou_span_a, senkou_span_b, chikou_span], axis=1)
    IC.columns = ["tenkan_sen", "kijun_sen", "senkou_span_a", "senkou_span_b", "chikou_span"]
    
    # Desplazar los Span para la nube
    if not offset:
        IC["senkou_span_a"] = senkou_span_a.shift(periods=periodo_kijun)
        IC["senkou_span_b"] = senkou_span_b.shift(periods=periodo_kijun)
    else:
        IC["senkou_span_a"] = senkou_span_a
        IC["senkou_span_b"] = senkou_span_b
        
    return IC

# Descargar los datos históricos
df = yf.download("TSLA", start="2020-01-01", end="2024-01-01", interval="1d")

# Calcular Indicador
ichimoku = Ichimoku_Cloud(df, periodo_tenkan=9, periodo_kijun=26)

# Graficar Ichimoku Cloud
fig, ax = plt.subplots(figsize=(22, 10))

ax.plot(df.index, df["Close"], label="Precio de Cierre", color="black", linewidth=1.0)

# Graficar la nube
ax.plot(ichimoku.index, ichimoku["senkou_span_a"], label="Senkou Span A", color="blue")
ax.plot(ichimoku.index, ichimoku["senkou_span_b"], label="Senkou Span B", color="red")
ax.fill_between(ichimoku.index, ichimoku["senkou_span_a"], ichimoku["senkou_span_b"], where=ichimoku["senkou_span_a"] > ichimoku["senkou_span_b"],
                color="lightgreen", alpha=0.5, label="Nube Alcista")
ax.fill_between(ichimoku.index, ichimoku["senkou_span_a"], ichimoku["senkou_span_b"], where=ichimoku["senkou_span_a"] <= ichimoku["senkou_span_b"],
                color="lightcoral", alpha=0.5, label="Nube Bajista")
ax.plot(ichimoku.index, ichimoku["tenkan_sen"], label="Tenkan Sen", color="purple", linestyle="--", lw=2)
ax.plot(ichimoku.index, ichimoku["kijun_sen"], label="Kijun Sen", color="orange", linestyle="--", lw=2)

ax.legend(fontsize=10)
ax.set_title("Nube Ichimoku con Precio de Cierre", fontsize=16)
ax.set_xlabel("Fecha")
ax.set_ylabel("Precio")
ax.grid(True)

plt.tight_layout()
plt.show()

# Recordatorio:
#   - El Ichimoku Cloud es una herramienta completa para el análisis técnico que proporciona información sobre niveles de soporte y resistencia,
#     así como la dirección y momento de la tendencia. Utiliza varias líneas para trazar una "nube" que ayuda a prever posibles niveles futuros de
#     soporte y resistencia.
#   - La tendencia es considerada alcista cuando el precio está por encima de la nube, bajista cuando está por debajo, y neutral o en transición
#     cuando el precio está dentro de la nube.
#   - El área entre el Senkou Span A y el Senkou Span B se colorea para indicar las condiciones del mercado: verde claro para condiciones alcistas
#     y rojo coral para condiciones bajistas. La combinación de estas líneas y la nube ayuda a los traders a visualizar la fuerza de la tendencia
#     y a tomar decisiones informadas sobre sus operaciones.

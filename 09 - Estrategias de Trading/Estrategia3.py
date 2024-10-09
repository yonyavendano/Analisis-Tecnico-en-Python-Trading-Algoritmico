# -*- coding: utf-8 -*-
# Librerías Estándar
import pandas as pd
import numpy as np
from itertools import product
from copy import deepcopy
import mplfinance as mpf
import matplotlib.pyplot as plt
from warnings import filterwarnings
filterwarnings("ignore")
# Librerías Propias
...

# Clase Estrategia
class Estrategia3:
    
    """ 
    Estrategia 3: Estrategia de Trading con RSI, Bandas de Bollinger y MACD
    
        Descripción:
            
            Esta estrategia combina tres indicadores técnicos ampliamente utilizados: El Índice de Fuerza
            Relativa (RSI), las Bandas de Bollinger (BB) y el MACD (Convergencia/Divergencia de Medias Móviles).
            Su objetivo es identificar puntos de entrada y salida en los mercados financieros basándose en la 
            relación entre la fuerza de la tendencia, los niveles de sobrecompra o sobreventa, y el cruce de
            medias móviles.
    
    Estrategia Para:
        
        - Acciones
        - ETFs
        - Índices
        - Divisas
        - Materias Primas
        - Criptomonedas
        
    Frecuencias (Ventanas de Tiempo):
        
        - Intradía (minutos).
        - Diaria.
        - Semanal.
        - Mensual.
        
    Periodo de Retención:
        
        - Variable (En esta Estrategia, este puede ser un factor optimizable)
        
    Análisis Usado: 
        
        - Análisis Técnico:
            * RSI (Obligatorio)
            * Bandas de Bollinger (Obligatorio)
            * MACD (Obligatorio)
    
    Descripción Detallada de la Estrategia:    
        
        La estrategia utiliza los tres indicadores de manera conjunta. El RSI se utiliza para detectar si el
        activo está en una zona de sobrecompra o sobreventa, mientras que el MACD se encarga de confirmar la 
        tendencia. Las Bandas de Bollinger actúan como guía para saber si el precio está en niveles extremos y 
        potencialmente reversibles. Las señales de entrada ocurren cuando se combina un cruce de MACD positivo
        con un RSI en zona de sobreventa y un precio de cierre por debajo del promedio de las Bandas de Bollinger,
        mientras que las señales de salida se basan en un cruce de MACD negativo, un RSI en sobrecompra y un 
        precio de cierre por encima del promedio de las Bandas de Bollinger.
                        
        Descripción de Stop Loss y Take Profit:
            
            Take Profit:
                
                Sañales alcistas:
                    
                    ((MACD["MACD"] > MACD["Señal"]) & (RSI < 50) & (df["Close"] < data["MA"]))
                    
                Señales bajistas:
                    
                    ((MACD["MACD"] < MACD["Señal"]) & (RSI > 50) & (df["Close"] > data["MA"]))
                
            Stop Loss:
                
                Las posiciones se cierran a medida que se crean señales contrarias a las actuales (esto puede ser
                                                                                                   optimizado).
            
    Co-Integración (Si se usan múltiples Indicadores):
        
        Señales:
            
            Las señales se producen a medida que se reunen las condiciones necesarias.
            
            Alcistas:
                
                RSI < 50 -> Se debe de ubicar en una zona de sobreventa.
                MACD > Señal -> Indicando una dirección de compra
                Close < Promedio de BB -> Se busca un momento donde el precio pueda subir significativamente.
                
            Bajistas:
                
                RSI > 50 -> Se debe de ubicar en una zona de sobrecompra.
                MACD < Señal -> Indicando una dirección de venta
                Close > Promedio de BB -> Se busca un momento donde el precio pueda bajar significativamente.
            
        Salida del Trade:
            
            Las posiciones se cierran a medida que se crean señales contrarias a las actuales.
            
    Supuestos Generales:
        
        - Esta estrategia no considera costos, comisiones o gastos derivados de las operaciones (Comisiones de apertura, rollovers, 
                                                                                                 entre otros).
        
    Notas:
        
        - La optimización de esta estrategia se puede extender todavía más (no solo los parámetros de los indicadores). Hay
          factores internos que pueden ser optimizados para mejorar más la rentabilidad de nuestra estrategia.
    """
    
    __version__ = 1.0
    
    
    # __init__
    def __init__(self, df: pd.DataFrame, **kwargs) -> None:
        
        """
        Constructor
        
        Parámetros
        ----------
        df : pd.DataFrame
            Datos del instrumento financiero.
            
        ** kwargs : dict, opcional
        
            Posibles argumentos:
                
                RSI = {
                    
                    "longitud": 14,
                    "columna": 'Close',
                    ... -> Todos los argumentos disponibles para este Indicador
                    
                    },
                
                BB = {
                    
                    "longitud": 20,
                    "std_dev": 2.0,
                    ... -> Todos los argumentos disponibles para este Indicador
                    
                    },
                
                MACD = {
                    
                    "longitud_rapida": 12,
                    "longitud_lenta": 26,
                    ... -> Todos los argumentos disponibles para este Indicador
                    
                    }
            
        Salida
        -------
        return: NoneType : None.
        """
        
        # Atributos
        self.df = df
        self.RSI = kwargs.get("RSI", {})
        self.BB = kwargs.get("BB", {})
        self.MACD = kwargs.get("MACD", {})
        self.estrategia_calculo = None
        self.direccion_mercado = None
        self.rendimiento_final_estrategia = 0.0
        # Atributos Privados
        ...
    
    # __repr__
    def __repr__(self) -> str:
        return self.__class__.__name__ + ".class"
    
    
    # Backtest
    def backtest(self) -> pd.Series:
        
        """
        Ejecuta un backtest de la estrategia para conocer la rentabilidad durante todo el periodo
        
        Salida
        -------
        return: pd.Series : Retorno Acumulado de la Estrategia.
        """
        
        # Calcular
        if self.estrategia_calculo is None:
            raise RuntimeError("Ejecutar el método de .calcular() antes de correr el backtest")
        # Obtener rendimiento
        rendimiento = self.df["Close"].pct_change()
        # Rendimiento Acumulado
        direccion_mercado = self.direccion_mercado.replace({0: np.nan}).ffill()
        rendimiento_acumulado = (1 + direccion_mercado.shift(periods=1) * rendimiento).cumprod()
        # Almacenar esto atributo
        self.rendimiento_final_estrategia = rendimiento_acumulado
        
        return rendimiento_acumulado
    
    
    # Calcular
    def calcular(self) -> dict:
        
        """
        Calcula cada indicador que se usará en la estrategia e identifica la tendencia actual del mercado.
        
        Salida
        -------
        return: dict|bool : Regresa un diccionario con la tendencia actual del mercado, o False si no se detectó nada.
        """
        
        ######################### Calcular Índice de Fuerza Relativa (RSI) #########################
        
        Delta = self.df[self.RSI.get("columna", "Close")].diff(periods=1)
        Ganancia = Delta.where(Delta >= 0, 0)
        Perdida = np.abs(Delta.where(Delta < 0, 0))
        # Valores en la posición de la longitud
        media_ganancia = Ganancia.ewm(span=self.RSI.get("longitud", 14), min_periods=self.RSI.get("longitud", 14), adjust=False).mean()
        media_perdida = Perdida.ewm(span=self.RSI.get("longitud", 14), min_periods=self.RSI.get("longitud", 14), adjust=False).mean()
        RS = media_ganancia / media_perdida
        RSI = pd.Series(np.where(RS == 0, 100, 100 - (100 / (1 + RS))), name="RSI", index=self.df.index)
        
        ############################################################################################
        
        ######################### Calcular Bandas de Bollinger #################################
        
        data = deepcopy(self.df)
        rolling = data[self.BB.get("columna", "Close")].rolling(window=self.BB.get("longitud", 20), min_periods=self.BB.get("longitud", 20))
        data["MA"] = rolling.mean()
        calc_intermedio = self.BB.get("std_dev", 2.0) * rolling.std(ddof=self.BB.get("ddof", 0))
        data["BB_Up"] = data["MA"] + calc_intermedio
        data["BB_Down"] = data["MA"] - calc_intermedio
        
        BB = data[["MA", "BB_Up", "BB_Down"]]
        
        ########################################################################################
        
        ################################# Calcular MACD #################################
        
        MA_Rapida = self.df[self.MACD.get("columna", "Close")].ewm(span=self.MACD.get("longitud_rapida", 12), 
                                                              min_periods=self.MACD.get("longitud_rapida", 12), adjust=False).mean()
        MA_Lenta = self.df[self.MACD.get("columna", "Close")].ewm(span=self.MACD.get("longitud_lenta", 26), 
                                                                  min_periods=self.MACD.get("longitud_lenta", 26), adjust=False).mean()
        # Determinar la línea MACD como la diferencia entre el EMA corto y el EMA largo
        MACD_d = MA_Rapida - MA_Lenta
        # Calcular la línea de señal como el EMA de la línea MACD
        señal = MACD_d.ewm(span=self.MACD.get("longitud_señal", 9), min_periods=self.MACD.get("longitud_señal", 9), adjust=False).mean()
        MACD = pd.concat([MACD_d, señal], axis=1)
        MACD.columns = ["MACD", "Señal"]
        
        #################################################################################
        
        # Guardar cálculos
        self.estrategia_calculo = {"RSI": RSI, "BB": BB, "MACD": MACD}
        
        # Generar señales
        buy_signals = ((MACD["MACD"] > MACD["Señal"]) & (RSI < 50) & (self.df["Close"] < BB["MA"])).astype(int)
        sell_signals = ((MACD["MACD"] < MACD["Señal"]) & (RSI > 50) & (self.df["Close"] > BB["MA"])).astype(int) * -1
        
        # Almacenar la dirección del mercado
        direccion = buy_signals + sell_signals
        self.direccion_mercado = direccion
        
        # Detectar Tendencia Actual
        if direccion.iloc[-1] == 1:
            tendencia_actual = {"tendencia_actual": "alcista"}
        elif direccion.iloc[-1] == -1:
            tendencia_actual = {"tendencia_actual": "bajista"}
        else:
            tendencia_actual = False
        

        return tendencia_actual
    
    
    # Optimizar
    def optimizar(self, rsi_rangos: list, bb_rangos: list, macd_rangos: list, max_iteraciones: int = 10_000) -> pd.DataFrame:
        
        """
        Este método optimiza los parámetros de la Estrategia que maximizan la rentabilidad.
        
        Parámetros
        ----------
        rsi_rangos : list
            Rango de valores que se probarán en el Indicador RSI.
        
        bb_rangos : list
            Rango de valores que se probarán en el Indicador de Bandas de Bollinger.
            
        macd_rangos : list
            Rango de valores que se probarán en el Indicador MACD.
            
        max_iteraciones : int, opcional
            Máximo número de combinaciones que se probarán (por defecto, se establece en 10,000).
        
        Salida
        -------
        return: pd.DataFrame : Conjunto de combinaciones con el rendimiento obtenido.
        """
        
        # Optimizar
        params_originales = [self.RSI, self.BB, self.MACD]
        resultados = []
        combinaciones = np.array(list(product(*rsi_rangos, *bb_rangos, *macd_rangos)))
        # Seleccionar las combinaciones
        if len(combinaciones) > max_iteraciones:
            # Elegir índices
            indices_seleccionados = np.random.choice(np.arange(0, len(combinaciones)), size=max_iteraciones, replace=False)
            combinaciones = combinaciones[indices_seleccionados]
        for long_rsi, long_bb, long_rap_macd, long_len_macd, long_señ_macd in combinaciones:
            # Reasignar parámetros
            self.RSI = {"longitud": long_rsi}
            self.BB = {"longitud": long_bb}
            self.MACD = {"longitud_rapida": long_rap_macd, "longitud_lenta": long_len_macd, "longitud_señal": long_señ_macd}
            self.calcular()
            retorno_final = self.backtest()
            resultados.append([long_rsi, long_bb, long_rap_macd, long_len_macd, long_señ_macd, retorno_final.iloc[-1]])
        # Almacenar en un DataFrame
        resultados = pd.DataFrame(data=resultados, columns=["Longitud_RSI", "Longitud_BB", "Longitud_Rap_MACD",
                                                            "Longitud_Len_MACD", "Longitud_Señ_MACD", "Rendimiento"])
        resultados = resultados.sort_values(by="Rendimiento", ascending=False)
        # Regresar todo al estado original
        self.RSI = params_originales[0]
        self.BB = params_originales[1]
        self.MACD = params_originales[2]
        self.calcular()
        self.backtest()
        
        return resultados
    
    
    # Plot
    def plot(self, ruta: str = "Estrategia3.png") -> None:
        
        """
        Genera un plot que muestra el rendimiento acumulado, los indicadores usados y los datos históricos.
        
        Salida
        -------
        return: NoneType : None.
        """
        
        # Graficar
        fig, axes = plt.subplots(nrows=5, ncols=1, figsize=(18, 14), gridspec_kw={"height_ratios": [1, 4, 1, 1, 1]},
                                 dpi=300)
        
        # Subplot 1: Rendimiento Acumulado
        axes[0].plot(self.rendimiento_final_estrategia.fillna(value=1), label="Rendimiento Acumulado")
        axes[0].set_title(f"Rendimiento Acumulado (Periodo {self.df.index[0].strftime('%Y/%m/%d')} - {self.df.index[-1].strftime('%Y/%m/%d')})",
                          fontsize=18, fontweight="bold", loc="left")
        axes[0].legend()
        axes[0].grid()
        axes[0].set_facecolor("#F7F7F7")
        
        # Subplot 2: Gráfico de Velas
        axes[1].set_title("Gráfico de Velas", loc="center", fontsize=18, fontweight="bold")
        mpf.plot(self.df, type="candle", style="yahoo", ax=axes[1])
        min_ytick, max_ytick = axes[1].get_yticks().min(), axes[1].get_yticks().max()
        yticks = np.linspace(start=min_ytick, stop=max_ytick, num=15)
        axes[1].set_yticks(yticks)
        axes[1].grid()
        axes[1].set_ylim([self.df["Low"].min() * 0.99, self.df["High"].max() * 1.01])
        axes[1].set_xticklabels(self.df.index.strftime("%Y/%m/%d"), rotation=0)
        axes[1].set_facecolor("#F7F7F7")
        
        # Subplot 3: RSI
        axes[2].plot(self.estrategia_calculo["RSI"])
        axes[2].axhline(y=70, label="Sobrecompra", color="gray", lw=2, linestyle="--")
        axes[2].axhline(y=30, label="Sobreventa", color="gray", lw=2, linestyle="--")
        axes[2].set_title("Índice de Fuerza Relativa (RSI)", fontsize=18, loc="left", weight="bold")
        axes[2].legend(loc="lower left")
        axes[2].grid()
        
        # Subplot 4: Bandas de Bollinger
        axes[3].plot(self.estrategia_calculo["BB"], label=["Media Móvil", "Banda Superior", "Banda Inferior"])
        axes[3].plot(self.df["Close"], label="Precios de Cierre")
        axes[3].set_title("Bandas de Bollinger", fontsize=18, loc="left", weight="bold")
        axes[3].legend(loc="lower left")
        axes[3].grid()
        
        # Subplot 5: MACD
        axes[4].plot(self.estrategia_calculo["MACD"], label=["MACD", "Señal"])
        axes[4].set_title("MACD", fontsize=18, loc="left", weight="bold")
        axes[4].legend(loc="lower left")
        axes[4].grid()
        
        # Grosor el marco
        for ax in axes:
            ax.spines["top"].set_linewidth(2.5)
            ax.spines["right"].set_linewidth(2.5)
            ax.spines["bottom"].set_linewidth(2.5)
            ax.spines["left"].set_linewidth(2.5)
            
        # Estilos generales del gráfico
        plt.tight_layout()
        plt.savefig(ruta)
        plt.close()


# Recordatorio:
if __name__ == "__main__":
    # Importar librerías adicionales
    import yfinance as yf
    import time
    # Obtener Datos
    df = yf.download("AAPL", start="2022-01-01", end="2024-01-01", interval="1d")
    # Definir parámetros
    rsi = {"longitud": 14, "columna": "Close"}
    bb = {"longitud": 20, "std_dev": 2.0, "ddof": 0, "columna": "Close"}
    macd = {"longitud_rapida": 12, "longitud_lenta": 26, "longitud_señal": 9, "columna": "Close"}
    est3 = Estrategia3(df, RSI=rsi, BB=bb, MACD=macd)
    print(est3)
    # Calcular
    calculo = est3.calcular()
    print("Tendencia Actual:\n\n", calculo)
    print("Cálculo de los Indicadores:\n\n", est3.estrategia_calculo)
    # Backtest
    retorno_final = est3.backtest()
    print("Retorno Final Acumulado:\n\n", retorno_final)
    # Optimización
    rsi_rango = [range(9, 22)]
    bb_rango = [range(9, 50)]
    macd_rangos = [range(9, 15), range(21, 31), range(9, 15)]
    total_combinaciones = product(*rsi_rango, *bb_rango, *macd_rangos)
    no_combinaciones = len(list(total_combinaciones))
    print("Número total de combinaciones:", no_combinaciones)
    tiempo_inicial = time.time()
    optimizacion = est3.optimizar(rsi_rangos=rsi_rango, bb_rangos=bb_rango, macd_rangos=macd_rangos)
    tiempo_final = time.time()
    print("La optimización tomo {} segundos".format(tiempo_final - tiempo_inicial))
    print("Optimización:\n\n", optimizacion)
    # Seleccionar los mejores parámetros
    rsi = {"longitud": optimizacion["Longitud_RSI"].iloc[0], "columna": "Close"}
    bb = {"longitud": optimizacion["Longitud_BB"].iloc[0], "std_dev": 2.0, "ddof": 0, "columna": "Close"}
    macd = {"longitud_rapida": optimizacion["Longitud_Rap_MACD"].iloc[0], "longitud_lenta": optimizacion["Longitud_Len_MACD"].iloc[0], 
            "longitud_señal": optimizacion["Longitud_Señ_MACD"].iloc[0], "columna": "Close"}
    est3 = Estrategia3(df, RSI=rsi, BB=bb, MACD=macd)
    print(est3)
    _ = est3.calcular()
    # Backtest
    retorno_final = est3.backtest()
    print("Retorno Final Acumulado:\n\n", retorno_final)
    # Graficar
    est3.plot()

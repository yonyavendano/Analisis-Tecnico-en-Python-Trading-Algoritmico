# -*- coding: utf-8 -*-
# Librerías Estándar
import pandas as pd
import numpy as np
from copy import deepcopy
from itertools import product
import mplfinance as mpf
import matplotlib.pyplot as plt
from warnings import filterwarnings
filterwarnings("ignore")
# Librerías Propias
...

# Clase Estrategia
class Estrategia2:
    
    """ 
    Estrategia 2: Estrategia Basada en Squeeze Momentum y DMI
    
        Descripción:
            
            Esta estrategia combina el Squeeze Momentum Y el Índice de Movimiento Direccional (DMI)
            para identificar oportunidades de trading basadas en tendencias y momentos de mercado.

    Estrategia Para:
        
        - Acciones
        - ETFs
        - Índices
        - Divisas
        - Materias Primas
        - Criptomonedas
        
    Frecuencias (Ventanas de Tiempo):
        
        - Intradía (minutos).
        - Diario.
        - Semanal.
        - Mensual.
        
    Periodo de Retención:
        
        - Corto (días).
        - Medio (días a semanas).
        - Largo (semanas a meses).
    
    Análisis Usado: 
        
        - Análisis Técnico:
            * Squeeze Momentum (Obligatorio)
            * Índice de Movimiento Direccional (Opcional)
    
    Descripción Detallada de la Estrategia:    
        
        Esta estrategia de trading se centra en la detección de tendencias utilizando principalmente el Squeeze Momentum 
        Indicator (SMI), que es crucial para identificar momentos de consolidación y anticipar posibles rupturas en el 
        precio. El SMI se basa en la volatilidad y mide la fuerza del movimiento del precio, lo que permite detectar 
        cuándo el mercado está en un período de baja actividad antes de una explosión de movimiento.

        Cuando el SMI muestra un "squeeze", indica que el mercado se encuentra en un rango estrecho, lo que sugiere una 
        próxima ruptura. Una vez que se produce esta ruptura, se observa el cambio en el color del histograma del SMI 
        para confirmar la dirección del movimiento. Si el histograma cambia a positivo, se considera una señal de compra,
        mientras que un cambio a negativo sugiere una señal de venta.

        Adicionalmente, se incluye el uso opcional del DMI (Directional Movement Index) para validar la dirección y la 
        fuerza de la tendencia. El DMI proporciona información sobre si el mercado está en una fase alcista o bajista, 
        utilizando la relación entre el +DI y el -DI. Si el +DI se encuentra por encima del -DI, esto confirma una tendencia
        alcista, lo que refuerza las señales generadas por el SMI. Por el contrario, si el -DI está por encima del +DI, 
        se confirma una tendencia bajista.

        Descripción de Stop Loss y Take Profit:
            
            Take Profit:
                
                Hay obtención de beneficios cuando las condiciones de la Estrategia se cumplan. 
                
                Si se usa el Squeeze Momentum en combinación con el DMI:
                    
                    Para una tendencia alcista: (SQ > 0) & (+DI > -DI)
                    Para una tendencia bajista: (SQ < 0) & (+DI < -DI)
                    
                Si solo se usa el Squeeze Momentum:
                    
                    Para una tendencia alcista: (SQ > 0)
                    Para una tendencia bajista: (SQ < 0)
                    
            Stop Loss:
                
                Cerrar la posición cuando se produce una señal contraria a la actual.
            
    Co-Integración (Si se usan múltiples Indicadores):
        
        Señales:
            
            - Compra cuando el DMI indica una tendencia alcista y el Squeeze Momentum genera una señal de 
              ruptura al alza.
              
            - Venta cuando el DMI indica una tendencia bajista y el Squeeze Momentum genera una señal de 
              ruptura a la baja.
            
        Salida del Trade:
            
            - Cerrar la posición cuando se produce una señal contraria a la actual.
            
    Supuestos Generales:
        
        - Esta estrategia no considera costos, comisiones o gastos derivados de las operaciones (Comisiones de apertura, rollovers, 
                                                                                                 entre otros).
        
    Notas:
        - Esta estrategia esta construida para funcionar solo con el Indicador de Squeeze Momentum o para trabajar en 
          combinación con el DMI.
    """
    
    __version__ = 1.0
    
    # __init__
    def __init__(self, df: pd.DataFrame, usar_dmi: bool = True, **kwargs) -> None:
        
        """
        Constructor.
        
        Parámetros
        ----------
        df : pd.DataFrame
            Datos del instrumento financiero.
            
        usar_dmi : bool, opcional
            Define si el Índice de Movimiento Direccional (DMI) será usado como confirmador de señales (True por defecto).
            
        **kwargs : dict, opcional
        
            Posibles argumentos:
                
                DMI = {
                    
                    "suavizado_ADX": 14,
                    "longitud_DI": 14,
                    ... -> Todos los argumentos disponibles para este Indicador
                    
                    },
                
                SM = {
                    
                    "longitud_bb": 20,
                    "desviacion_std_bb": 2.0,
                    ... -> Todos los argumentos disponibles para este Indicador
                    
                    }
                
        Salida
        -------
        return: NoneType : None.
        """
        
        # Atributos
        self.df = df
        self.usar_dmi = usar_dmi
        self.DMI = kwargs.get("DMI", {})
        self.SM = kwargs.get("SM", {})
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
        Realiza un backtest de la estrategia de trading para detectar tendencias y calcular el rendimiento acumulado.
        
        Salida
        -------
        return: pd.Series : Rendimiento Acumulado de la Estrategia.
        """
        
        # Calcular
        if self.estrategia_calculo is None:
            raise RuntimeError("Se debe de ejecutar primero el método de .calcular()")
        DMI = self.estrategia_calculo["DMI"]
        SQ = self.estrategia_calculo["SM"]
        # Detectar tendencias
        if self.usar_dmi:
            # Reasignar 1 para Tendencias Alcistas
            alcista = ((DMI["+DI"] > DMI["-DI"]) & (SQ["SQZ"] > 0)).replace({True: 1, False: 0})
            # Reasignar -1 para Tendencias Bajistas
            bajista = ((DMI["+DI"] < DMI["-DI"]) & (SQ["SQZ"] < 0)).replace({True: -1, False: 0})
        else:
            # Reasignar 1 para Tendencias Alcistas
            alcista = ((SQ["SQZ"] > 0)).replace({True: 1, False: 0})
            # Reasignar -1 para Tendencias Bajistas
            bajista = ((SQ["SQZ"] < 0)).replace({True: -1, False: 0})
        # Direccion del Mercado
        direccion = alcista + bajista
        # Obtener Rendimiento
        rendimiento = self.df["Close"].pct_change()
        # Rendimiento Acumulado
        rendimiento_acumulado = (1 + direccion.shift(periods=1) * rendimiento).cumprod()
        # Almacenar Resultado
        self.rendimiento_final_estrategia = rendimiento_acumulado
        self.direccion_mercado = direccion
        
        return rendimiento_acumulado
    
    
    # Calcular
    def calcular(self) -> dict:
        
        """
        Calculo el Índice de Movimiento Direccional (DMI) y el Squeeze Momentum (SM) para identificar la dirección de
        la tendencia en función de los movimientos del mercado
        
        Salida
        -------
        return: dict|bool : Un diccionario con la tendencia actual ('alcista' o 'bajista') basado en los cálculos de DMI
                            y Squeeze Momentum si se genera una señal, o False si no se detecta ninguna señal.
        """
        
        #################### Calcular Índice de Movimiento Direccional ####################
        
        # Revisar si debe usar DMI
        if self.usar_dmi:
            # Calcular el Rango Verdadero
            High, Low = self.df["High"], self.df["Low"]
            H_minus_L = High - Low
            prev_clo = self.df["Close"].shift(periods=1)
            H_minus_PC = abs(High - prev_clo)
            L_minus_PC = abs(prev_clo - Low)
            TR = pd.Series(np.max([H_minus_L, H_minus_PC, L_minus_PC], axis=0), index=self.df.index, name="TR")
            
            # Calcular los Movimientos Direccionales (+DM y -DM)
            pre_PDM = self.df["High"].diff().dropna()
            pre_MDM = self.df["Low"].diff(periods=-1).dropna()
            plus_DM = pre_PDM.where((pre_PDM > pre_MDM.values) & (pre_PDM > 0), 0)
            minus_DM = pre_MDM.where((pre_MDM > pre_PDM.values) & (pre_MDM > 0), 0)
            
            # Calcular los valores iniciales para las sumas suavizadas de TR, +DM, -DM
            TRL = [np.nansum(TR[:self.DMI.get("suavizado_ADX", 14) + 1])]
            PDML = [plus_DM[:self.DMI.get("suavizado_ADX", 14)].sum()]
            MDML = [minus_DM[:self.DMI.get("suavizado_ADX", 14)].sum()]
            factor = 1 - 1 / self.DMI.get("suavizado_ADX", 14)
    
            # Calcular las sumas suavizadas de TR, +DM y -DM utilizando el método Wilder
            for i in range(0, int(self.df.shape[0] - self.DMI.get("suavizado_ADX", 14) - 1)):
                TRL.append(TRL[i] * factor + TR[self.DMI.get("suavizado_ADX", 14) + i + 1])
                PDML.append(PDML[i] * factor + plus_DM[self.DMI.get("suavizado_ADX", 14) + i])
                MDML.append(MDML[i] * factor + minus_DM[self.DMI.get("suavizado_ADX", 14) + i])
                
            # Calcular los Indicadores Direccionales (+DI y -DI)
            PDI = np.array(PDML) / np.array(TRL) * 100
            MDI = np.array(MDML) / np.array(TRL) * 100
            # Calcular el Indice Direccional (DX)
            DX = np.abs(PDI - MDI) / (PDI + MDI) * 100
            ADX = [DX[:self.DMI.get("suavizado_ADX", 14)].mean()]
            
            # Calcular el Índice Direccional Promedio (ADX) utilizando la longitud_DI
            _ = [ADX.append((ADX[i] * (self.DMI.get("longitud_DI", 14) - 1) + \
                             DX[self.DMI.get("longitud_DI", 14) + i])/self.DMI.get("longitud_DI", 14)) for i in range(int(len(DX) - self.DMI.get("longitud_DI", 14)))]
            ADXI = pd.DataFrame(PDI, columns=["+DI"], index=self.df.index[-len(PDI):])
            ADXI["-DI"] = MDI
            ADX = pd.DataFrame(ADX, columns=["ADX"], index=self.df.index[-len(ADX):])
            
            ADX = ADX.merge(ADXI, how="outer", left_index=True, right_index=True)
        else:
            ADX = None
        
        ###################################################################################
        
        ######################### Calcular Squeeze Momentum (SM) #########################
        
        df = deepcopy(self.df)
        
        # Calcular Bandas de Bollinger
        rolling = df[self.SM.get("columna", "Close")].rolling(window=self.SM.get("longitud_bb", 20), min_periods=self.SM.get("longitud_bb", 20))
        df["MA"] = rolling.mean()
        calc_intermedio = self.SM.get("desviacion_std_bb", 2.0) * rolling.std()
        df["BB_Up"] = df["MA"] + calc_intermedio
        df["BB_Lw"] = df["MA"] - calc_intermedio
        
        # Calcular Canales de Keltner
        EMA = df[self.SM.get("columna", "Close")].ewm(span=self.SM.get("longitud_kc", 20), 
                                                      min_periods=self.SM.get("longitud_kc", 20), adjust=False).mean()
        
        # Subpaso: Calcular Indicador TR
        High, Low = df["High"], df["Low"]
        H_minus_L = High - Low
        prev_cl = df["Close"].shift(periods=1)
        H_minus_PC = abs(High - prev_cl)
        L_minus_PC = abs(prev_cl - Low)
        TR = pd.Series(np.max([H_minus_L, H_minus_PC, L_minus_PC], axis=0), index=df.index, name="TR")
        TR_EMA = TR.ewm(span=self.SM.get("longitud_kc", 20), min_periods=self.SM.get("longitud_kc", 20), adjust=True).mean()
        
        # Cálculo de las Bandas de Keltner
        Banda_KC_Media_Alta = EMA + self.SM.get("multiplicador_kc", 1.5) * TR_EMA
        Banda_KC_Media_Baja = EMA - self.SM.get("multiplicador_kc", 1.5) * TR_EMA
        KC = pd.concat([Banda_KC_Media_Alta, EMA, Banda_KC_Media_Baja], axis=1)
        KC.columns = ["Banda_KC_Media_Alta", "EMA", "Banda_KC_Media_Baja"]
        
        # Calcular el Indicador de Squeeze Momentum
        squeeze = df["Close"].diff(periods=self.SM.get("periodos_momentum", 12)).rolling(window=self.SM.get("longitud_momentum", 6),
                                                                                         min_periods=self.SM.get("longitud_momentum", 6)).mean()
        
        # Verificar las bandas para obtener distintas condiciones de Squeeze
        func_on = (df["BB_Lw"] > KC["Banda_KC_Media_Baja"]) & (df["BB_Up"] < KC["Banda_KC_Media_Alta"])
        func_off = (df["BB_Lw"] < KC["Banda_KC_Media_Baja"]) & (df["BB_Up"] > KC["Banda_KC_Media_Alta"])
        no_squeeze = ~func_on & ~func_off
        
        # Concatenar los resultados
        SQM = pd.concat([squeeze, func_on, func_off, no_squeeze], axis=1)
        SQM.columns = ["SQZ", "SQZ_ON", "SQZ_OFF", "SQZ_NO"]
        
        ##################################################################################
        
        # Guardar cálculos
        self.estrategia_calculo = {"DMI": ADX, "SM": SQM}
        
        # Revisar si se generó una señal
        if self.usar_dmi:
            if ((ADX["+DI"] > ADX["-DI"]) & (SQM["SQZ"] > 0)).iloc[-1]:
                valor = {"tendencia_actual": "alcista"}
            elif ((ADX["+DI"] < ADX["-DI"]) & (SQM["SQZ"] < 0)).iloc[-1]:
                valor = {"tendencia_actual": "bajista"}
            else:
                valor = False
        else:
            valor = {"tendencia_actual": "alcista"} if SQM["SQZ"].iloc[-1] >= 0 else {"tendencia_actual": "bajista"}

        return valor
    
    
    # Optimizar
    def optimizar(self, rangos_SM: list, rangos_DMI: list = []) -> pd.DataFrame:
        
        """
        Optimiza los parámetros de la estrategia de trading.
        
        Parámetros
        ----------
        rangos_SM: list
            Lista de rangos para las longitudes de las Bandas de Bollinger y los canales de Keltner (BB y KC)
            a probar durante la optimización.
            
        rangos_DMI: list, opcional
            Lista de rangos para los parámetros del ADX y el DI (suavizado del ADX y la longitud del DI), utilizado
            si el indicador DMI está habilitado -usar_dmi=True- (por defecto es una lista vacía).
        
        Salida
        -------
        return: pd.DataFrame : DataFrame con las combinaciones de parámetros probadas y su rendimiento asociado.
        """
        
        # Optimizar
        params_originales = [self.DMI, self.SM]
        resultados = []
        if self.usar_dmi:
            parametros_combinaciones = product(*rangos_SM, *rangos_DMI)
            for long_bb, long_kc, suav_ADX, long_DI in parametros_combinaciones:
                # Reasignar las variables 
                self.DMI = {"suavizado_ADX": suav_ADX, "longitud_DI": long_DI}
                self.SM = {"longitud_bb": long_bb, "longitud_kc": long_kc}
                self.calcular()
                retorno_final = self.backtest()
                # Almacenar valores
                resultados.append([long_bb, long_kc, suav_ADX, long_DI, retorno_final.iloc[-1]])
        else:
            parametros_combinaciones = product(*rangos_SM)
            for long_bb, long_kc in parametros_combinaciones:
                # Reasignar las variables 
                self.SM = {"longitud_bb": long_bb, "longitud_kc": long_kc}
                self.calcular()
                retorno_final = self.backtest()
                # Almacenar valores
                resultados.append([long_bb, long_kc, retorno_final.iloc[-1]])
        # Dar estructura a los resultados y ordenarlos
        columnas = ["longitud_bb", "long_kc",
                    "suavizado_ADX", "longitud_DI"] if self.usar_dmi else ["longitud_bb", "longitud_kc"]
        columnas = columnas + ["Rendimiento"]
        resultados = pd.DataFrame(data=resultados, columns=columnas)
        resultados = resultados.sort_values(by="Rendimiento", ascending=False)
        # Regresar parámetros originales
        self.DMI = params_originales[0]
        self.SM = params_originales[1]
        # Ejecutar y Backtest
        self.calcular()
        self.backtest()
        
        return resultados
    
    
    # Plot
    def plot(self, ruta: str = "Estrategia2_SM_DMI.png") -> None:
        
        """
        Este método produce un gráfico que ilustra los datos, los indicadores y el rendimiento acumulado
        
        Parámetros
        ----------
        ruta: str, opcional
            Indica la dirección donde se almacenerá el gráfico creado (por defecto, se establece 'Estrategia2_SM_DMI.png').
        
        Salida
        -------
        return: NoneType: None.
        """
        
        # Graficar
        fig, axes = plt.subplots(nrows=3 + self.usar_dmi, ncols=1, figsize=(18, 14), 
                                 gridspec_kw={"height_ratios": [1, 4, 1] + [1] * self.usar_dmi}, dpi=300)
        
        # Subplot 1: Rendimiento Acumulado
        axes[0].plot(self.rendimiento_final_estrategia.fillna(value=1), label="Rendimiento Acumulado")
        axes[0].set_title(f"Rendimiento Acumulado (Periodo {self.df.index[0].strftime('%Y/%m/%d')} - {self.df.index[-1].strftime('%Y/%m/%d')})",
                          fontsize=18, fontweight="bold", loc="left")
        axes[0].legend()
        axes[0].grid()
        axes[0].set_facecolor("#F7F7F7")
        
        # Subplot 2: Gráfico de Velas
        axes[1].set_title("Gráfico de Velas", loc="center", fontsize=18, fontweight="bold")
        mpf.plot(self.df, type="candle", style="yahoo", ax=axes[1], warn_too_much_data=self.df.shape[0])
        min_ytick, max_ytick = axes[1].get_yticks().min(), axes[1].get_yticks().max()
        yticks = np.linspace(start=min_ytick, stop=max_ytick, num=15)
        axes[1].set_yticks(yticks)
        axes[1].grid()
        axes[1].set_ylim([self.df["Low"].min() * 0.99, self.df["High"].max() * 1.01])
        axes[1].set_xticklabels(self.df.index.strftime("%Y/%m/%d"), rotation=0)
        axes[1].set_facecolor("#F7F7F7")
        
        # Subplot 3: Squeeze Momentum
        index = self.estrategia_calculo["SM"].index
        for i in range(self.estrategia_calculo["SM"].shape[0]):
            axes[2].bar(index[i], self.estrategia_calculo["SM"].iat[i, 0], width=3.0,
                        color="#33FF5B" if self.estrategia_calculo["SM"].iat[i, 0] > 0 else "red")
        axes[2].set_title(f"Indicador Squeeze Momentum (Periodo {self.df.index[0].strftime('%Y/%m/%d')} - {self.df.index[-1].strftime('%Y/%m/%d')})",
                          fontsize=18, fontweight="bold", loc="left")
        axes[2].set_xticklabels(self.df.index.strftime("%Y/%m/%d"), rotation=0)
        axes[2].grid()
        axes[2].set_facecolor("#F7F7F7")
        
        # Subplot 4: DMI
        if self.usar_dmi:
            dmi = self.estrategia_calculo["DMI"]
            indice = dmi.index
            adx = dmi["ADX"]
            plusDI = dmi["+DI"]
            minusDI = dmi["-DI"]
            
            axes[3].plot(indice, plusDI, label="+DI", color="blue")
            axes[3].plot(indice, minusDI, label="-DI", color="red")
            axes[3].plot(indice, adx, label="ADX", color="green")
            
            axes[3].fill_between(indice, y1=0, y2=plusDI, where=(plusDI > minusDI), color="lightblue", alpha=0.5)
            axes[3].fill_between(indice, y1=0, y2=minusDI, where=(plusDI < minusDI), color="lightcoral", alpha=0.5)
            axes[3].legend(fontsize=10, loc="upper right")
            axes[3].set_title("Índice de Movimiento Direccional (+DI, -DI, ADX)", size=20, fontweight="bold", loc="left")
            axes[3].grid()
        
        # Grosor el marco
        for ax in axes:
            ax.spines["top"].set_linewidth(2.5)
            ax.spines["right"].set_linewidth(2.5)
            ax.spines["bottom"].set_linewidth(2.5)
            ax.spines["left"].set_linewidth(2.5)
            
        # Estilos generales del gráfico
        plt.tight_layout()
        plt.subplots_adjust(hspace=0.20)
        plt.savefig(ruta)
        plt.close()
        

# Recordatorio:
if __name__ == "__main__":
    # Importar librerías adicionales
    import yfinance as yf
    import time
    # Obtener Datos
    df = yf.download("TSLA", start="2019-01-01", end="2024-01-01", interval="1d")
    # Instanciar Estrategia 
    dmi = {"suavizado_ADX": 14, "longitud_DI": 14}
    sm = {"longitud_bb": 20, "desviacion_std_bb": 2.0, "longitud_kc": 20, "multiplicador_kc": 1.5,
          "periodos_momentum": 12, "longitud_momentum": 6, "columna": "Close"}
    est2 = Estrategia2(df, DMI = dmi, SM = sm)
    print(est2)
    # Calcular Estrategia
    calc = est2.calcular()
    print("Tendencia del Mercado Actual:\n\n", calc)
    print("Cálculo de los Indicadores:\n\n", est2.estrategia_calculo)
    # Backtest
    rendimiento_final = est2.backtest()
    print("Retorno Final:\n\n", rendimiento_final)
    # Optimización
    rangos_SM = [range(10, 101, 10), range(10, 101, 10)]
    rangosDMI = [range(9, 22), range(9, 22)]
    total_combinaciones = product(*rangos_SM, *rangosDMI)
    print("Total de combinaciones:", len(list(total_combinaciones)))
    tiempo_inicial = time.time()
    optimizacion = est2.optimizar(rangos_SM=rangos_SM, rangos_DMI=rangosDMI)
    tiempo_final = time.time()
    print("La optimización tomó un total de {} segundos".format(tiempo_final - tiempo_inicial))
    print("Optimización:\n\n", optimizacion)
    # Ejecutar con los mejores parámetros
    dmi = {"suavizado_ADX": optimizacion["suavizado_ADX"].iloc[0], "longitud_DI": optimizacion["longitud_DI"].iloc[0]}
    sm = {"longitud_bb": optimizacion["longitud_bb"].iloc[0], "desviacion_std_bb": 2.0, 
          "longitud_kc": optimizacion["long_kc"].iloc[0], "multiplicador_kc": 1.5,
          "periodos_momentum": 12, "longitud_momentum": 6, "columna": "Close"}
    est2 = Estrategia2(df, DMI = dmi, SM = sm)
    _ = est2.calcular()
    rendimiento_final_optimizado = est2.backtest()
    print("Retorno Final Optimizado:\n\n", rendimiento_final_optimizado)
    # Ejecutar usando únicamente SQM (Usando parámetros optimizados)
    est2.usar_dmi = False
    _ = est2.calcular()
    rendimiento_final_optimizado_sm = est2.backtest()
    print("Retorno Final Optimizado:\n\n", rendimiento_final_optimizado_sm)
    # Graficar (con y sin usar DMI)
    est2 = Estrategia2(df, DMI=dmi, SM=sm)
    _ = est2.calcular()
    rendimiento_final_optimizado = est2.backtest()
    est2.plot("Estrategia2_SM_DMI.png")
    est2.usar_dmi = False
    rendimiento_final_optimizado = est2.backtest()
    est2.plot("Estrategia2_SM.png")

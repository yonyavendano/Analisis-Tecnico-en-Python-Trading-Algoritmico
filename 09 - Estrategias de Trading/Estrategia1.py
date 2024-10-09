# -*- coding: utf-8 -*-
# Librerías Estándar
import pandas as pd
import numpy as np
from itertools import product
import mplfinance as mpf
import matplotlib.pyplot as plt
from warnings import filterwarnings
filterwarnings("ignore")
# Librerías Propias
...

# Clase Estrategia
class Estrategia1:
    
    """ 
    Estrategia 1: Estrategia Chop Zone
    
        Descripción:
            
            La Estrategia Chop Zone (CZ) busca identificar momentos clave en el mercado en los que el activo se
            encuentra en una tendencia alcista o bajista pronunciada. La estrategia está diseñada para determinar 
            puntos de entrada y salida basados en el ángulo de la Media Móvil Exponencial (EMA) y el comportamiento 
            del precio típico (TP). Se clasifica a través de valores de indicadores que oscilan entre una fuerte 
            tendencia alcista y bajista.
    
    Estrategia Para:
        
        - Acciones
        - ETFs
        - Índices
        - Divisas
        - Materias Primas
        - Criptomonedas
        
    Frecuencias (Ventanas de Tiempo):
        
        - Intradía
        - Diaria
        - Semanal
        - Mensual
        
    Periodo de Retención:
        
        - Variable (Dependerá de la fuerza de la tendencia y la venta utilizada)
    
    Análisis Usado: 
        
        - Análisis Técnico:
            * Indicador Chop Zone
    
    Descripción Detallada de la Estrategia:    
        
        La estrategia asigna valores de tendencia a partir del ángulo calculado de la EMA. Estos valores se agrupan 
        en un indicador Chop Zone (CZ), donde se identifican varias fases: desde una tendencia alcista muy fuerte (0) 
        hasta una bajista muy fuerte (4). Las señales se basan en los ángulos derivados de la diferencia entre la EMA 
        y el precio típico (TP).
        
        La estrategia utiliza la pendiente o el ángulo de la Media Móvil Exponencial (EMA) para determinar la fuerza y
        la dirección de la tendencia del mercado. El ángulo calculado refleja la velocidad con la que el precio está
        cambiando en relación con la EMA. A partir de este ángulo, se asignan diferentes valores de tendencia que
        indican la fuerza de la misma.
                        
        Descripción de Stop Loss y Take Profit:
            
            Take Profit:
                
                Los puntos de take profit se activan cuando el indicador CZ alcanza valores de tendencia contrarios 
                al sentido de la operación, es decir, cuando se pasa de una tendencia alcista fuerte (valor 0) a una 
                fase de neutralidad o tendencia bajista (valor 4).
                
            Stop Loss:
                
                El Stop-loss se activa cuando surge una señal opuesta a la posición actual. Si se está en una tendencia
                alcista y aparece una señal bajista, se cierra la posición automáticamente para limitar pérdidas. De igual
                forma, si se está en una tendencia bajista y aparece una señal alcista, se procede a cerrar la posición en
                corto. Este mecanismo garantiza que las posiciones se ajusten a los cambios de tendencia y protege el capital
                frente a movimientos adversos del mercado.
            
        Co-Integración (Si se usan múltiples Indicadores):
            
            Señales:
                
                La señal principal se genera cuando el indicador CZ muestra un valor de 0 (tendencia alcista) o 4 
               (tendencia bajista). 
                
            Salida del Trade:
                
                La salida se recomienda cuando la tendencia pierde fuerza, es decir, cuando el indicador CZ muestra 
                un cambio a valores intermedios o neutrales.
                
    Supuestos Generales:
        
        - Esta estrategia no considera costos, comisiones o gastos derivados de las operaciones (Comisiones de apertura, rollovers, 
                                                                                                 entre otros).
        - El activo opera en un mercado con volatilidad suficiente para generar movimientos fuertes en ambas direcciones.
        
    Notas:
        
        - La estrategia puede necesitar ajustes según la frecuencia temporal seleccionada. Por ejemplo, al operar en marcos 
          temporales intradía, podría ser conveniente reducir la ventana de tiempo utilizada para adaptarse mejor a la dinámica 
          del mercado y captar movimientos más rápidos.
    """
    
    __version__ = 1.0
    
    
    # __init__
    def __init__(self, df: pd.DataFrame, longitud: int = 30, longitud_ema: int = 34, columna: str = "Close",
                 valores_indicador: list = [0, 4]) -> None:
        
        """
        Inicialización de la Clase
        
        Parámetros
        ----------
        param : pd.DataFrame : df : Datos históricos del activo a analizar.
        ----------
        param : int : longitud : Ventana a ser usada en el cálculo del CZ (por defecto, se establece en 30).
        ----------
        param : int : longitud_ema : Ventana a usar en la EMA (por defecto, se establece en 34).
        ----------
        param : str : columna : Columna a ser usada en el cálculo del CZ (por defecto, se establece en 'Close').
        ----------
        param : list : valores_indicador : Valores que definen las fases del indicador CZ (por defecto, se establece en [0, 4]).
        
        Salida
        -------
        return: NoneType : None
        """
        
        # Atributos
        self.df = df
        self.longitud = longitud
        self.longitud_ema = longitud_ema
        self.columna = columna
        self.valores_indicador = valores_indicador
        self.estrategia_calculo = None
        self.rendimiento_final_estrategia = 0.0
         
        # Atributos Privados
        self.__valores_tendencia = {
            
            0: "alcista",
            1: "alcista",
            2: "alcista",
            3: "alcista",
            4: "bajista",
            5: "bajista",
            6: "bajista",
            7: "bajista",
            8: "neutral"
            
            }
    
    # __repr__
    def __repr__(self) -> str:
        return self.__class__.__name__ + ".class"
    
    
    # Backtest
    def backtest(self) -> pd.Series:
        
        """
        Este método obtiene el retorno acumulado de la Estrategia aplicada al activo que hemos pasado.                
        
        Salida
        -------
        return: pd.Series : Retorno acumulado del activo durante el periodo analizado.
        """
        
        # Calcular
        if self.estrategia_calculo is None:
            raise RuntimeError("Debes ejecutar el método 'calcular' antes de llamar al método 'backtest'")
            
        # Reasignar tendencia (1 para Tendencia Alcista, -1 para Tendencia Bajista y 0 para los valores no usados)
        estrategia_calculo = self.estrategia_calculo.copy()
        valores_no_usados = set(range(0, 9)) - set(self.valores_indicador)
        indices_no_usados = estrategia_calculo.isin(list(valores_no_usados))
        estrategia_calculo.loc[indices_no_usados[indices_no_usados].index] = "N/A"
        estrategia_calculo = estrategia_calculo.replace(self.__valores_tendencia)
        estrategia_calculo = estrategia_calculo.replace({"alcista": 1, "bajista": -1, "N/A": 0})
        # Calcular Rendimientos
        rendimientos = self.df[self.columna].pct_change()
        # Rendimientos Acumulados
        retorno_acumulado = (1 + estrategia_calculo.shift(periods=1) * rendimientos).cumprod()
        
        # Guardar Rendimiento Acumulado
        self.rendimiento_final_estrategia = retorno_acumulado
        
        return retorno_acumulado
    
    
    # Calcular
    def calcular(self) -> dict:
        
        """
        Este método calculará el Indicador de Chop Zone y guardará este cálculo en el atributo 'estrategia_calculo'.                
        
        Salida
        -------
        return: dict|bool : Un diccionario si se ha generado una señal en la última vela o False si no se ha producido nada.
        """
        
        # Calcular precios típicos y rangos
        columna_precio = self.df[self.columna]
        TP = (self.df["High"] + self.df["Low"] + self.df["Close"]) / 3
        precio_suavizado = columna_precio.rolling(window = self.longitud, min_periods=self.longitud)
        max_suavizado = precio_suavizado.max()
        min_suavizado = precio_suavizado.min()
        rango_HL = 25 / (max_suavizado - min_suavizado) * min_suavizado
        
        # Calcular la EMA y el ángulo de la EMA
        ema = self.df[self.columna].ewm(span=self.longitud_ema, min_periods=self.longitud_ema, adjust=False).mean()
        x1_ema = 0
        x2_ema = 1
        y1_ema = 0
        y2_ema = (ema.shift(periods=1) - ema) / TP * rango_HL
        c_ema = np.sqrt((x2_ema - x1_ema) ** 2 + (y2_ema - y1_ema) ** 2)
        angulo_ema0 = round(np.rad2deg(np.arccos((x2_ema - x1_ema) / c_ema)))
        angulo_ema1 = np.where(y2_ema > 0, - angulo_ema0, angulo_ema0)[max(self.longitud, self.longitud_ema):]
        CZ = np.where(angulo_ema1 >= 5, 0,
             np.where((angulo_ema1 >= 3.57) & (angulo_ema1 < 5), 1,
             np.where((angulo_ema1 >= 2.14) & (angulo_ema1 < 3.57), 2,
             np.where((angulo_ema1 >= 0.71) & (angulo_ema1 < 2.14), 3,
             np.where(angulo_ema1 <= -5, 4,
             np.where((angulo_ema1 <= -3.57) & (angulo_ema1 > -5), 5,
             np.where((angulo_ema1 <= -2.14) & (angulo_ema1 > -3.57), 6,
             np.where((angulo_ema1 <= -0.71) & (angulo_ema1 > -2.14), 7, 8))))))))
        
        CZ = pd.Series([np.nan] * max(self.longitud, self.longitud_ema) + CZ.tolist(), index=self.df.index, name="CZ")
        
        # Guardar cálculo del indicador como atributo
        self.estrategia_calculo = CZ
        
        # Revisar si se generó una señal (alcista fuerte o bajista fuerte)
        ultimo_valor = CZ.iloc[-1]
        if ultimo_valor == 0:
            valor = {"tendencia_actual": self.__valores_tendencia[0]}
        elif ultimo_valor == 4:
            valor = {"tendencia_actual": self.__valores_tendencia[4]}
        else:
            valor = False

        return valor
    
    
    # Optimizar
    def optimizar(self, rango_longitud: list, rango_longitud_ema: list) -> pd.DataFrame:
        
        """
        Este método encuentra los parámetros que maximizan la rentabilidad de la estrategia.
        
        Parámetros
        ----------
        param : list : rango_longitud : Rango de valores que se usarán como parámetros para la estrategia en su cálculo.
        ----------
        param : list : rango_longitud_ema : Rango de valores que se usarán como parámetros para la estrategia en su cálculo.
        
        Salida
        -------
        return: pd.DataFrame : DataFrame con el rendimiento de cada combinación de parámetros que fue calculada.
        """
        
        # Optimizar
        combinaciones_posibles = product(rango_longitud, rango_longitud_ema)
        params_originales = [self.longitud, self.longitud_ema]
        # Iterar sobre parámetros (combinaciones)
        resultados = []
        for long, long_ema in combinaciones_posibles:
            self.longitud = long
            self.longitud_ema = long_ema
            # Calcular Estrategia y correr Backtest
            self.calcular()
            retorno_final = self.backtest()
            # Almacenar retorno final con parámetros
            resultados.append([long, long_ema, retorno_final.iloc[-1]])
        # Estructura Datos y Ordenarlos
        resultados = pd.DataFrame(resultados, columns=["longitud", "longitud_ema", "Rendimiento"])
        resultados = resultados.sort_values(by="Rendimiento", ascending=False)
        # Regresar valores originales
        self.longitud = params_originales[0]
        self.longitud_ema = params_originales[1]
        # Ejecutar y Backtest
        self.calcular()
        self.backtest()
        
        return resultados
    
    
    # Plot
    def plot(self, ruta: str = "Estrategia1_CZ.png") -> None:
        
        """
        Este método generará un gráfico de nuestros datos, el indicador y su rendimiento acumulado
        
        Parámetros
        ----------
        param : str : ruta : Ruta donde guardará el gráfico generado (por defecto, se establece en 'Estrategia1_CZ.png').
        
        Salida
        -------
        return: NoneType : None. 
        """
        
        # Graficar
        fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(18, 14), gridspec_kw={"height_ratios": [1, 4, 1]},
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
        
        #  Subplot 3: Chop Zone
        colores = {
            
            0: "#26C6DA", # Turquesa - Tendencia Alcista Fuerte
            1: "#43A047", # Verde Oscuro - Tendencia Alcista Moderada
            2: "#A5D6A7", # Verde Claro - Tendencia Alcista Leve
            3: "#009688", # Lima - Tendencia Alcista Débil 
            4: "#D50000", # Rojo Oscuro - Tendencia Bajista Fuerte
            5: "#E91E63", # Rojo - Tendencia Bajista Moderada
            6: "#FF6D00", # Naranja - Tendencia Bajista Leve
            7: "#FFB74D", # Naranja Claro - Tendencia Bajista Débil
            8: "#FDD835"  # Amarillo - Tendencia Neutral o sin Dirección Clara
            
            }
        
        # Generar plot de Barras
        axes[2].set_title(f"Indicador Chop Zone (Periodo {self.df.index[0].strftime('%Y/%m/%d')} - {self.df.index[-1].strftime('%Y/%m/%d')})",
                          fontsize=18, fontweight="bold", loc="left")
        for i in range(0, self.estrategia_calculo.shape[0]):
            # Evitar valores Nans
            if pd.isna(self.estrategia_calculo[i]):
                axes[2].bar(i, 0, color="white")
            else:
                axes[2].bar(i, 1, color=colores[int(self.estrategia_calculo[i])])
        axes[2].set_xticklabels(self.df.index.strftime("%Y/%m/%d"), rotation=0)
        axes[2].grid()
        axes[2].set_facecolor("#F7F7F7")
        
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
    df = yf.download("AMZN", start="2022-01-01", end="2024-01-01", interval="1d")
    # Inicializar nuestra estrategia
    est1 = Estrategia1(df, longitud=30, longitud_ema=34, columna="Close", valores_indicador=[0, 4])
    print(est1)
    # Calcularla
    calc = est1.calcular()
    print("Tendencia Actual:\n\n", calc)
    print("Cálculo del Indicador:\n\n", est1.estrategia_calculo)
    # Backtest (Retorno Histórico)
    retorno_acumulado = est1.backtest()
    print("Retorno Acumulado:\n\n", retorno_acumulado)                
    # Optimizar Estrategia 1 en función del rendimiento
    rango_longitud = range(10, 101)
    rango_longitud_ema = range(10, 101)
    no_combinaciones = len(list(product(rango_longitud, rango_longitud_ema)))
    print(f"¡Se ejecutarán {no_combinaciones} combinaciones diferentes de parámetros!")
    tiempo_inicio = time.time()
    optimizacion = est1.optimizar(rango_longitud=rango_longitud, rango_longitud_ema=rango_longitud_ema)
    tiempo_final = time.time()
    print("Tomo {} segundos".format(tiempo_final - tiempo_inicio))
    # Extraer y mostrar los mejores resultados
    print("Rendimientos Acumulados de cada combinación:\n\n", optimizacion)
    print(f"Mejores parámetros: [longitud -> {optimizacion.iloc[0, 0]} - longitud_ema -> {optimizacion.iloc[0, 1]}] - Rendimiento {optimizacion.iloc[0, 2]}")
    # Establecer nuestra Estrategia
    est1 = Estrategia1(df, longitud=optimizacion.iloc[0, 0], longitud_ema=optimizacion.iloc[0, 1], columna="Close", valores_indicador=[0, 4])    
    _ = est1.calcular()                
    # Backtest Optimizado (Retorno Histórico)
    retorno_acumulado_optimizado = est1.backtest()
    print("Retorno Acumulado:\n\n", retorno_acumulado_optimizado)           
    # Plot
    est1.plot()    
                
    # Análisis más detallado del rendimiento
    print("Rendimiento del Primer Año:", retorno_acumulado_optimizado.loc["2022-01-01":"2022-12-31"].iloc[-1] - 1)
    print("Rendimiento del Segundo Año:", retorno_acumulado_optimizado.iloc[-1] - retorno_acumulado_optimizado.loc["2022-01-01":"2022-12-31"].iloc[-1])
                
    # Conocer el tiempo que se ha estado inviertiendo
    print(f"La estrategia se ha ejecutado el {est1.estrategia_calculo.isin([0, 4]).mean()} del tiempo")
                
    # Ampliar valores del indicador
    est1 = Estrategia1(df, longitud=optimizacion.iloc[0, 0], longitud_ema=optimizacion.iloc[0, 1], columna="Close", valores_indicador=[0, 1, 2,
                                                                                                                                       3, 4, 5,
                                                                                                                                       6, 7])   
    _ = est1.calcular()                
    # Backtest Optimizado Ampliado (Retorno Histórico)
    retorno_acumulado_optimizado_ampliado = est1.backtest()
    print("Retorno Acumulado Ampliado:\n\n", retorno_acumulado_optimizado_ampliado)   

# -*- coding: utf-8 -*-
# Importar librerías
...
# Librerías Propias
from estrategias.Estrategia1 import Estrategia1
from estrategias.Estrategia2 import Estrategia2
from estrategias.Estrategia3 import Estrategia3

# Definir clase
class EstrategiasTrading:
    
    """
    Clase que integra y ejecuta todas las estrategias codificadas
    """
    
    # __init__
    def __init__(self, parametros_estrategias: dict) -> None:
        
        """
        Constructor.
        
        Parámetros:
        -----------
        parametros_estrategias : dict
            Diccionario con los parámetros específicos para cada estrategia
            
        Salida:
        -------
        return : NoneType : None
        """
        
        # Definir atributos e Inicializar Estrategias
        self.estrategias = {
            
            "Estrategia1": Estrategia1(**parametros_estrategias.get("Estrategia1", {})),
            "Estrategia2": Estrategia2(**parametros_estrategias.get("Estrategia2", {})),
            "Estrategia3": Estrategia3(**parametros_estrategias.get("Estrategia3", {}))
            
            }
        
    
    # __repr__
    def __repr__(self):
        return self.__class__.__name__ + ".class"
    
    # Ejecutar/Correr/Calcular Estrategia
    def calcular_estrategia(self, nombre_estrategia: str) -> dict:
        
        """
        Calcula una estrategia específica sobre un conjunto de datos
        
        Parámetros:
        -----------
        nombre_estrategia : str
            El nombre de la estrategia a ejecutar (debe coincidir con las claves definidas en el diccionario de estrategias)
            
        Salida:
        -------
        return : dict|bool : El resultado de la ejecución de la estrategia.
        """
        
        try: 
            estrategia = self.estrategias.get(nombre_estrategia, None)
            if estrategia is None:
                raise ValueError(f"Estrategia '{nombre_estrategia}' no ha sido encontrada.")
            return estrategia.calcular()
        except Exception as error:
            print(f"Error ejecutando {nombre_estrategia}: {error}")
        
        
    # Ejecutar/Correr/Calcular Todas las Estrategias
    def calcular_todas(self, verbose: bool = False) -> dict:
        
        """
        Ejecuta todas las estrategias sobre un conjunto de datos.
        
        
        Parámetros:
        -----------
        verbose : bool, opcional
            Si es True, entonces imprimirá por consola la estrategia que está calculando.
            
        Salida:
        -------
        return : dict : Diccionario con los resultados de cada estrategia
        """
        
        resultados = {}
        for nombre, estrategia in self.estrategias.items():
            if verbose:
                print(f"Ejecuntando {nombre}...")
            resultados[nombre] = self.calcular_estrategia(nombre)
        
        return resultados
        
# Recordatorio:
if __name__ == "__main__":
    # Importar librerías adicionales
    import yfinance as yf
    # Obtener Datos
    df_est1 = yf.download("AMZN", start="2023-06-01", end="2024-01-01")
    df_est2 = yf.download("TSLA", start="2023-06-01", end="2024-01-01")
    df_est3 = yf.download("AAPL", start="2023-06-01", end="2024-01-01")
    # Definir parámetros
    estrategia1_params = {"df": df_est1, "longitud": 30, "longitud_ema": 34, "columna": "Close", "valores_indicador": [0, 4]}
    estrategia2_params = {"df": df_est2, "DMI": {}, "SM": {}}
    estrategia3_params = {"df": df_est3, "RSI": {}, "BB": {}, "MACD": {}}
    estrategias_params = {"Estrategia1": estrategia1_params, "Estrategia2": estrategia2_params, "Estrategia3": estrategia3_params}
    # Generar Instancia
    Estrategias = EstrategiasTrading(estrategias_params)
    # Calcular cada Estrategia
    calc_est1 = Estrategias.calcular_estrategia("Estrategia1")
    print(calc_est1)
    calc_est2 = Estrategias.calcular_estrategia("Estrategia2")
    print(calc_est2)
    calc_est3 = Estrategias.calcular_estrategia("Estrategia3")
    print(calc_est3)
    # Calcular Todas las Estrategias
    calc_estrategias = Estrategias.calcular_todas(verbose=True)
    print(calc_estrategias)

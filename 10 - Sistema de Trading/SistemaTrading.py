# -*- coding: utf-8 -*-
# Importar librerías
import yfinance as yf
import time
# Librerías Propias
from config import config
from Estrategias import EstrategiasTrading

# Ejecutar Sistema
def EjecutarSistema():
    
    """
    Esta función tiene la responsabilidad de implementar diversas estrategias de trading para múltiples activos en una
    variedad de marcos de tiempo.
    """
    
    marcos_tiempo = config.marcos_tiempo
    tiempos_espera = {"1m": 60, "5m": 300, "15m": 900}
    tiempo_restante_ejecucion = {"1m": 60, "5m": 300, "15m": 900}
    periodo_descarga = {"1m": "5d", "5m": "1mo", "15m": "1mo", "1d": "1y", "1wk": "5y", "1mo": "max"}
    posiciones_intradia = []
    posiciones_no_intradia = []
    marcos_ejecutar = ["1m", "5m", "15m", "1d", "1wk", "1mo"]
    while True:
        for tipo_activo, instrumentos in config.activos.items():
            for horizonte, ventanas_tiempo in marcos_tiempo.items():
                for intervalo in ventanas_tiempo:
                    # Revisar si se debe de ejecutar
                    if intervalo not in marcos_ejecutar:
                        continue
                    # Descargar datos
                    df = yf.download(instrumentos, interval=intervalo, period=periodo_descarga[intervalo])
                    # Cambiar Nivel de Columnas
                    df.columns = df.columns.swaplevel(0, 1)
                    # Ejecutar Estrategias
                    for activo in instrumentos:
                        parametros_estrategias = config.parametros_estrategias
                        # Agregar datos a parámetros
                        parametros_estrategias["Estrategia1"]["df"] = df[activo].dropna()
                        parametros_estrategias["Estrategia2"]["df"] = df[activo].dropna()
                        parametros_estrategias["Estrategia3"]["df"] = df[activo].dropna()
                        # Crear Instancia
                        Estrategias = EstrategiasTrading(parametros_estrategias)
                        # Calcular Estrategias
                        calculo_estrategias = Estrategias.calcular_todas(verbose=False)
                        # Revisar si hay señales y almacenar información
                        if horizonte == "intradia":
                            if isinstance(calculo_estrategias["Estrategia1"], dict):
                                posiciones_intradia.append({activo: calculo_estrategias["Estrategia1"], "intervalo": intervalo,
                                                            "Estrategia": "Estrategia1"})
                            if isinstance(calculo_estrategias["Estrategia2"], dict):
                                posiciones_intradia.append({activo: calculo_estrategias["Estrategia2"], "intervalo": intervalo,
                                                            "Estrategia": "Estrategia2"})
                            if isinstance(calculo_estrategias["Estrategia3"], dict):
                                posiciones_intradia.append({activo: calculo_estrategias["Estrategia3"], "intervalo": intervalo,
                                                            "Estrategia": "Estrategia3"})
                        else:
                            if isinstance(calculo_estrategias["Estrategia1"], dict):
                                posiciones_no_intradia.append({activo: calculo_estrategias["Estrategia1"], "intervalo": intervalo,
                                                            "Estrategia": "Estrategia1"})
                            if isinstance(calculo_estrategias["Estrategia2"], dict):
                                posiciones_no_intradia.append({activo: calculo_estrategias["Estrategia2"], "intervalo": intervalo,
                                                            "Estrategia": "Estrategia2"})
                            if isinstance(calculo_estrategias["Estrategia3"], dict):
                                posiciones_no_intradia.append({activo: calculo_estrategias["Estrategia3"], "intervalo": intervalo,
                                                            "Estrategia": "Estrategia3"})
        
        # Imprimir Información
        print("\n\nSistema Intradía:\n\n", posiciones_intradia)
        print("\n\nSistema No-Intradía:\n\n", posiciones_no_intradia)
        
        # Reiniciar listas
        posiciones_intradia.clear()
        posiciones_no_intradia.clear()
        marcos_ejecutar.clear()
        
        # Calcular y Revisar Tiempos de Espera
        for clave in tiempo_restante_ejecucion:
            if (tiempo_restante_ejecucion[clave] - 60) <= 0:
                marcos_ejecutar.append(clave)
                tiempo_restante_ejecucion[clave] = tiempos_espera[clave]
            else:
                # Substraer diferencia en el tiempo de espera
                tiempo_restante_ejecucion[clave] = tiempo_restante_ejecucion[clave] - 60
                
        # Dormir entre cada iteración
        time.sleep(60)
                        
# Recordatorio:
if __name__ == "__main__":
    EjecutarSistema() 

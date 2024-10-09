# -*- coding: utf-8 -*-
# Importar librerías
from threading import Thread
import pytz # pip install pytz
from datetime import datetime
import time
# Librerías Propias
import SistemaTrading
from config import config

# Definir función
def Cesar_Ejecucion():
    
    """
    Cesa la ejecución del Sistema.
    """
    
    # Definir la zona horaria de Nueva York
    zona_nueva_york = pytz.timezone("America/New_York")
    hora_actual_ny = datetime.now(zona_nueva_york)
    hora_cadena = config.ejecucion["hora_operacion"]["fin"]
    hora_objeto = datetime.strptime(hora_cadena, "%H:%M")
    # Extraer las horas y minutos
    horas = hora_objeto.hour
    minutos = hora_objeto.minute
    hora_cierre_mercado = hora_actual_ny.replace(hour=horas, minute=minutos, second=0, microsecond=0)
    # Obtener Diferencia
    diferencia = (hora_cierre_mercado - hora_actual_ny).seconds + 1
    if diferencia > 0:
        time.sleep(diferencia)
        raise SystemExit("¡Mercados Cerrados!")
    else:
        raise RuntimeError("¡Los mercados están cerrados!")
        
# Ejecutar
if __name__ == "__main__":
    # Ejecutando en paralelo
    t = Thread(target=Cesar_Ejecucion)
    t.start()
    # Ejecutar Sistema de Trading
    SistemaTrading.EjecutarSistema()

# -*- coding: utf-8 -*-
# Importar librerías
import yfinance as yf # pip install yfinance
from datetime import datetime, timedelta
import os 

# Configuración de parámetros
ticker = "AAPL"
fecha_inicial = "2023-01-01"
fecha_final = "2024-01-01"
intervalo = "1d"

# Descargar datos históricos de Yahoo Finance
datos = yf.download(ticker, start=fecha_inicial, end=fecha_final, interval=intervalo)

# Mostrar los primeros registros
print("Datos Históricos:")
print(datos.head())

# Guardar los datos en un archivo csv
if not os.path.isdir("../datos"):
    os.mkdir("../datos")
datos.to_csv("../datos/datos_historicos.csv")

# Intervalos disponibles y sus limitaciones:

# |----------|------------|--------------|    
# |  Código  |   Tiempo   |  Limitación  |
# |----------|------------|--------------|
# |   1m     | 1 minuto   |    7 días    |
# |----------|------------|--------------|
# |   2m     | 2 minutos  |    60 días   |
# |----------|------------|--------------|
# |   5m     | 5 minutos  |    60 días   |
# |----------|------------|--------------|
# |   15m    | 15 minutos |    60 días   |
# |----------|------------|--------------|
# |   30m    | 30 minutos |    60 días   |
# |----------|------------|--------------|
# |   60m    | 1 hora     |    730 días  |
# |----------|------------|--------------|
# |   90m    | 90 minutos |    60 días   |
# |----------|------------|--------------|
# |   1h     | 1 hora     |    730 días  |
# |----------|------------|--------------|
# |   1d     | 1 día      |    Ninguna   |
# |----------|------------|--------------|
# |   5d     | 5 días     |    Ninguna   |
# |----------|------------|--------------|
# |   1wk    | 1 semana   |    Ninguna   |
# |----------|------------|--------------|
# |   1mo    | 1 mes      |    Ninguna   |
# |----------|------------|--------------|
# |   3mo    | 3 meses    |    Ninguna   |
# |----------|------------|--------------|


# Ejemplos de uso de diferentes activos e intervalos de tiempo

# Ejemplo 1: Descargar datos con intervalo de 1 minuto (limitado a aproximadamente 7 días)
intervalo_1m = yf.download(tickers="EURUSD=X", interval="1m")
print("Datos de 1 minuto:")
print(intervalo_1m)

# Ejemplo 2: Descargar datos con intervalo de 15 minutos (limitado a aproximadamente 60 días)
fecha_final = datetime.now()
fecha_inicial = fecha_final - timedelta(days=30)
fecha_final = fecha_final.strftime("%Y-%m-%d")
fecha_inicial = fecha_inicial.strftime("%Y-%m-%d")
intervalo_15m = yf.download(tickers="BTC-USD", start=fecha_inicial, end=fecha_final, interval="15m")
print("Datos de 15 minutos:")
print(intervalo_15m)

# Ejemplo 3: Descargar datos con intervalo de 1 día (no hay un límite establecido)
intervalo_1d = yf.download(tickers="CL=F", start="2010-01-01", end="2024-08-01", interval="1d")
print("Datos de 1 día:")
print(intervalo_1d)

# Ejemplo 4: Descargar todos los datos históricos para un instrumento
accion = yf.Ticker(ticker=ticker)
accion_hist = accion.history(period="max", end=fecha_final, interval="1d")
print("Total de datos históricos:")
print(accion_hist)
# Imprimir Fechas de Dividendos
print(accion_hist["Dividends"][accion_hist["Dividends"] != 0.0])
# Imprimir Splits
print(accion_hist["Stock Splits"][accion_hist["Stock Splits"] != 0.0])

# Recordatorio:
#   - Yahoo Finance es un proveedor de datos históricos por excelencia (es el más utilizado).
#   - Yahoo Finance puede limitar la frecuencia de las consultas si se realizan demasiadas peticiones
#     en un corto periodo de tiempo.

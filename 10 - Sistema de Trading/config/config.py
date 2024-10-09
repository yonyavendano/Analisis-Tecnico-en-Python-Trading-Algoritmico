# config.py

# Definición de activos
activos = {
    
    "divisas": [
        
        "EURUSD=X", "GBPUSD=X", "USDJPY=X"
        
        ],
    
    "acciones": [
        
        "AAPL", "GOOGL", "AMZN"
        
        ],
    
    "materias_primas": [
        
        "CL=F", "SI=F", "NG=F"
        
        ],
    
    "criptomonedas": [
        
        "BTC-USD", "ETH-USD", "ADA-USD"
        
        ],
    
    "indices": [
        
        "SPY", "QQQ", "DAX"
        
        ]
    
    }

# Definición de marcos de tiempo
marcos_tiempo = {
    
    "intradia": ["1m", "5m", "15m"],
    "diario": ["1d"],
    "semanal": ["1wk"],
    "mensual": ["1mo"]

    }

# Parámetros de estrategias
parametros_estrategias = {
    
    "Estrategia1": {
        
        "df": "",
        "longitud": 30, 
        "longitud_ema": 34,
        "columna": "Close",
        "valores_indicador": [0, 4]
        
        },
    
    "Estrategia2": {
        
        "df": "",
        "usar_dmi": True, 
        "DMI": {
            
            "suavizado_ADX": 14,
            "longitud_DI": 14
            
            },
        "SM": {
            
            "longitud_bb": 20,
            "desviacion_std_bb": 2.0,
            "longitud_kc": 20,
            "multiplicador_kc": 1.5,
            "periodos_momentum": 12,
            "longitud_momentum":6,
            "columna": "Close"
            
            }
    
        },
    "Estrategia3": {
        
        "df": "",
        "RSI": {
            
            "longitud": 14,
            "columna": "Close"
            
            },
        "BB": {
            
            "longitud": 20,
            "std_dev": 2.0,
            "ddof": 0,
            "columna": "Close"
            
            },
        "MACD": {
            
            "longitud_rapida": 12,
            "longitud_lenta": 26,
            "longitud_señal": 9,
            "columna": "Close"
            
            }
        
        }
    
    }

# Parámetros de Optimización de Estrategias
optimizacion = {
    
    "Estrategia1": {
        
        },
    "Estrategia2": {
        
        },
    "Estrategia3": {
        
        },
    
    }

# Configuración del Backtest
backtesting = {
    
    "fechas": {
        
        "inicio": "",
        "fin": ""
        
        }
    
    }

# Configuración de ejecución automática de operaciones
ejecucion = {
    
    "hora_operacion": {
        
        "inicio": "09:30",
        "fin": "16:00"
        
        }
    
    }

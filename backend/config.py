import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
    DEBUG = False
    TESTING = False
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'mysql+pymysql://root:password@localhost/monitoring_suhu_tanah'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # SocketIO
    SOCKETIO_ASYNC_MODE = 'threading'
    
    # Sensor Settings
    SENSOR_UPDATE_INTERVAL = 30  # seconds
    DATA_RETENTION_DAYS = 7
    
    # Thresholds
    SOIL_MOISTURE_MIN = 30  # %
    SOIL_MOISTURE_MAX = 80  # %
    TEMP_MIN = 15  # °C
    TEMP_MAX = 35  # °C
    HUMIDITY_MAX = 95  # %
    
    # Pump & Fertilizer
    PUMP_ACTIVATION_THRESHOLD = 30  # % soil moisture
    PUMP_AUTO_OFF_TIME = 300  # seconds (5 minutes)
    FERTILIZER_AUTO_OFF_TIME = 120  # seconds (2 minutes)

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

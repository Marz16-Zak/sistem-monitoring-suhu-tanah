from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class SensorData(db.Model):
    __tablename__ = 'sensor_data'
    
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    soil_moisture = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

class PumpControl(db.Model):
    __tablename__ = 'pump_control'
    
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(10), default='OFF')
    manual_mode = db.Column(db.Boolean, default=False)
    auto_mode = db.Column(db.Boolean, default=True)
    activation_threshold = db.Column(db.Integer, default=30)
    duration = db.Column(db.Integer, default=300)
    last_activated = db.Column(db.DateTime)
    last_deactivated = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class FertilizerControl(db.Model):
    __tablename__ = 'fertilizer_control'
    
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(10), default='OFF')
    manual_mode = db.Column(db.Boolean, default=False)
    auto_mode = db.Column(db.Boolean, default=False)
    schedule_type = db.Column(db.String(10), default='NONE')
    schedule_time = db.Column(db.Time)
    schedule_day = db.Column(db.Integer)
    duration = db.Column(db.Integer, default=120)
    last_activated = db.Column(db.DateTime)
    last_deactivated = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class PumpHistory(db.Model):
    __tablename__ = 'pump_history'
    
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(10), nullable=False)
    trigger_type = db.Column(db.String(10), nullable=False)
    soil_moisture_at_trigger = db.Column(db.Float)
    duration = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

class FertilizerHistory(db.Model):
    __tablename__ = 'fertilizer_history'
    
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(10), nullable=False)
    trigger_type = db.Column(db.String(10), nullable=False)
    duration = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

class SystemAlert(db.Model):
    __tablename__ = 'system_alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    alert_type = db.Column(db.String(50), nullable=False)
    severity = db.Column(db.String(10), default='WARNING')
    message = db.Column(db.Text)
    is_read = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

class SystemSetting(db.Model):
    __tablename__ = 'system_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    setting_key = db.Column(db.String(100), unique=True, nullable=False)
    setting_value = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class SystemLog(db.Model):
    __tablename__ = 'system_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    log_level = db.Column(db.String(10), default='INFO')
    message = db.Column(db.Text, nullable=False)
    details = db.Column(db.JSON)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()

def get_db():
    return db

from flask import Blueprint, jsonify
from datetime import datetime, timedelta
from database import db, SensorData, SystemAlert
import json

sensor_bp = Blueprint('sensor', __name__, url_prefix='/api/sensor')

@sensor_bp.route('/latest', methods=['GET'])
def get_latest():
    """Get latest sensor data"""
    try:
        latest = SensorData.query.order_by(SensorData.timestamp.desc()).first()
        
        if not latest:
            return jsonify({'error': 'No sensor data available'}), 404
        
        # Get pump and fertilizer status
        from database import PumpControl, FertilizerControl
        pump = PumpControl.query.first()
        fertilizer = FertilizerControl.query.first()
        
        return jsonify({
            'id': latest.id,
            'temperature': latest.temperature,
            'humidity': latest.humidity,
            'soil_moisture': latest.soil_moisture,
            'timestamp': latest.timestamp.isoformat(),
            'pump_status': pump.status if pump else 'OFF',
            'fertilizer_status': fertilizer.status if fertilizer else 'OFF'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@sensor_bp.route('/history', methods=['GET'])
def get_history():
    """Get sensor data history (last 24 hours by default)"""
    try:
        hours = 24
        since = datetime.utcnow() - timedelta(hours=hours)
        
        data = SensorData.query.filter(
            SensorData.timestamp >= since
        ).order_by(SensorData.timestamp.asc()).all()
        
        return jsonify({
            'data': [
                {
                    'temperature': d.temperature,
                    'humidity': d.humidity,
                    'soil_moisture': d.soil_moisture,
                    'timestamp': d.timestamp.isoformat()
                } for d in data
            ],
            'count': len(data)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@sensor_bp.route('/stats', methods=['GET'])
def get_stats():
    """Get sensor statistics"""
    try:
        since = datetime.utcnow() - timedelta(hours=24)
        data = SensorData.query.filter(
            SensorData.timestamp >= since
        ).all()
        
        if not data:
            return jsonify({'error': 'No data available'}), 404
        
        temps = [d.temperature for d in data]
        humidities = [d.humidity for d in data]
        moistures = [d.soil_moisture for d in data]
        
        return jsonify({
            'temperature': {
                'min': min(temps),
                'max': max(temps),
                'avg': sum(temps) / len(temps)
            },
            'humidity': {
                'min': min(humidities),
                'max': max(humidities),
                'avg': sum(humidities) / len(humidities)
            },
            'soil_moisture': {
                'min': min(moistures),
                'max': max(moistures),
                'avg': sum(moistures) / len(moistures)
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_latest_sensor_data():
    """Helper function to get latest sensor data for WebSocket"""
    try:
        latest = SensorData.query.order_by(SensorData.timestamp.desc()).first()
        
        if not latest:
            return {}
        
        from database import PumpControl, FertilizerControl
        pump = PumpControl.query.first()
        fertilizer = FertilizerControl.query.first()
        
        return {
            'temperature': latest.temperature,
            'humidity': latest.humidity,
            'soil_moisture': latest.soil_moisture,
            'timestamp': latest.timestamp.isoformat(),
            'pump_status': pump.status if pump else 'OFF',
            'fertilizer_status': fertilizer.status if fertilizer else 'OFF'
        }
    except Exception as e:
        print(f'Error getting sensor data: {e}')
        return {}

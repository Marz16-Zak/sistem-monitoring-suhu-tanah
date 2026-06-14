from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
from database import db, SensorData, PumpHistory, FertilizerHistory, SystemAlert, SystemLog

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')

@dashboard_bp.route('/summary', methods=['GET'])
def get_summary():
    """Get dashboard summary"""
    try:
        from database import PumpControl, FertilizerControl
        
        latest = SensorData.query.order_by(SensorData.timestamp.desc()).first()
        pump = PumpControl.query.first()
        fertilizer = FertilizerControl.query.first()
        
        # Get alerts count
        unread_alerts = SystemAlert.query.filter_by(is_read=False).count()
        
        # Get recent pump history
        pump_history = PumpHistory.query.order_by(
            PumpHistory.timestamp.desc()
        ).limit(5).all()
        
        # Get recent fertilizer history
        fert_history = FertilizerHistory.query.order_by(
            FertilizerHistory.timestamp.desc()
        ).limit(5).all()
        
        return jsonify({
            'current_sensor': {
                'temperature': latest.temperature if latest else None,
                'humidity': latest.humidity if latest else None,
                'soil_moisture': latest.soil_moisture if latest else None,
                'timestamp': latest.timestamp.isoformat() if latest else None
            },
            'pump_status': pump.status if pump else 'OFF',
            'fertilizer_status': fertilizer.status if fertilizer else 'OFF',
            'unread_alerts': unread_alerts,
            'recent_pump_history': [
                {'action': h.action, 'trigger': h.trigger_type, 'timestamp': h.timestamp.isoformat()}
                for h in pump_history
            ],
            'recent_fertilizer_history': [
                {'action': h.action, 'trigger': h.trigger_type, 'timestamp': h.timestamp.isoformat()}
                for h in fert_history
            ]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard_bp.route('/alerts', methods=['GET'])
def get_alerts():
    """Get system alerts"""
    try:
        limit = request.args.get('limit', 10, type=int)
        alerts = SystemAlert.query.order_by(
            SystemAlert.timestamp.desc()
        ).limit(limit).all()
        
        return jsonify({
            'alerts': [
                {
                    'id': a.id,
                    'type': a.alert_type,
                    'severity': a.severity,
                    'message': a.message,
                    'is_read': a.is_read,
                    'timestamp': a.timestamp.isoformat()
                } for a in alerts
            ]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard_bp.route('/logs', methods=['GET'])
def get_logs():
    """Get system logs"""
    try:
        limit = request.args.get('limit', 20, type=int)
        logs = SystemLog.query.order_by(
            SystemLog.timestamp.desc()
        ).limit(limit).all()
        
        return jsonify({
            'logs': [
                {
                    'id': l.id,
                    'level': l.log_level,
                    'message': l.message,
                    'timestamp': l.timestamp.isoformat()
                } for l in logs
            ]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard_bp.route('/export/csv', methods=['GET'])
def export_csv():
    """Export sensor data to CSV"""
    try:
        import csv
        from io import StringIO
        from flask import make_response
        
        hours = request.args.get('hours', 24, type=int)
        since = datetime.utcnow() - timedelta(hours=hours)
        
        data = SensorData.query.filter(
            SensorData.timestamp >= since
        ).order_by(SensorData.timestamp.asc()).all()
        
        si = StringIO()
        writer = csv.writer(si)
        writer.writerow(['Timestamp', 'Temperature (°C)', 'Humidity (%)', 'Soil Moisture (%'])
        
        for d in data:
            writer.writerow([
                d.timestamp.isoformat(),
                d.temperature,
                d.humidity,
                d.soil_moisture
            ])
        
        output = make_response(si.getvalue())
        output.headers['Content-Disposition'] = 'attachment; filename=sensor_data.csv'
        output.headers['Content-Type'] = 'text/csv'
        
        return output
    except Exception as e:
        return jsonify({'error': str(e)}), 500

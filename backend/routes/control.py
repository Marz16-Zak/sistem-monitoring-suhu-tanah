from flask import Blueprint, jsonify, request
from datetime import datetime
from database import db, PumpControl, FertilizerControl, PumpHistory, FertilizerHistory, SystemLog

control_bp = Blueprint('control', __name__, url_prefix='/api/control')

# ============= PUMP CONTROL =============

@control_bp.route('/pump/on', methods=['POST'])
def pump_on():
    """Turn on the pump (manual)"""
    try:
        pump = PumpControl.query.first()
        if not pump:
            return jsonify({'error': 'Pump control not initialized'}), 500
        
        pump.status = 'ON'
        pump.manual_mode = True
        pump.last_activated = datetime.utcnow()
        db.session.commit()
        
        # Log history
        history = PumpHistory(
            action='ON',
            trigger_type='MANUAL'
        )
        db.session.add(history)
        db.session.commit()
        
        # Log system
        log = SystemLog(message='Pump turned ON (manual)', log_level='INFO')
        db.session.add(log)
        db.session.commit()
        
        return jsonify({'status': 'success', 'message': 'Pump turned on', 'pump_status': 'ON'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@control_bp.route('/pump/off', methods=['POST'])
def pump_off():
    """Turn off the pump (manual)"""
    try:
        pump = PumpControl.query.first()
        if not pump:
            return jsonify({'error': 'Pump control not initialized'}), 500
        
        pump.status = 'OFF'
        pump.manual_mode = False
        pump.last_deactivated = datetime.utcnow()
        db.session.commit()
        
        # Log history
        history = PumpHistory(
            action='OFF',
            trigger_type='MANUAL'
        )
        db.session.add(history)
        db.session.commit()
        
        # Log system
        log = SystemLog(message='Pump turned OFF (manual)', log_level='INFO')
        db.session.add(log)
        db.session.commit()
        
        return jsonify({'status': 'success', 'message': 'Pump turned off', 'pump_status': 'OFF'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@control_bp.route('/pump/status', methods=['GET'])
def pump_status():
    """Get pump status"""
    try:
        pump = PumpControl.query.first()
        if not pump:
            return jsonify({'error': 'Pump control not initialized'}), 500
        
        return jsonify({
            'status': pump.status,
            'manual_mode': pump.manual_mode,
            'auto_mode': pump.auto_mode,
            'activation_threshold': pump.activation_threshold,
            'last_activated': pump.last_activated.isoformat() if pump.last_activated else None,
            'last_deactivated': pump.last_deactivated.isoformat() if pump.last_deactivated else None
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============= FERTILIZER CONTROL =============

@control_bp.route('/fertilizer/on', methods=['POST'])
def fertilizer_on():
    """Turn on the fertilizer (manual)"""
    try:
        fertilizer = FertilizerControl.query.first()
        if not fertilizer:
            return jsonify({'error': 'Fertilizer control not initialized'}), 500
        
        fertilizer.status = 'ON'
        fertilizer.manual_mode = True
        fertilizer.last_activated = datetime.utcnow()
        db.session.commit()
        
        # Log history
        history = FertilizerHistory(
            action='ON',
            trigger_type='MANUAL'
        )
        db.session.add(history)
        db.session.commit()
        
        # Log system
        log = SystemLog(message='Fertilizer turned ON (manual)', log_level='INFO')
        db.session.add(log)
        db.session.commit()
        
        return jsonify({'status': 'success', 'message': 'Fertilizer turned on', 'fertilizer_status': 'ON'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@control_bp.route('/fertilizer/off', methods=['POST'])
def fertilizer_off():
    """Turn off the fertilizer (manual)"""
    try:
        fertilizer = FertilizerControl.query.first()
        if not fertilizer:
            return jsonify({'error': 'Fertilizer control not initialized'}), 500
        
        fertilizer.status = 'OFF'
        fertilizer.manual_mode = False
        fertilizer.last_deactivated = datetime.utcnow()
        db.session.commit()
        
        # Log history
        history = FertilizerHistory(
            action='OFF',
            trigger_type='MANUAL'
        )
        db.session.add(history)
        db.session.commit()
        
        # Log system
        log = SystemLog(message='Fertilizer turned OFF (manual)', log_level='INFO')
        db.session.add(log)
        db.session.commit()
        
        return jsonify({'status': 'success', 'message': 'Fertilizer turned off', 'fertilizer_status': 'OFF'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@control_bp.route('/fertilizer/status', methods=['GET'])
def fertilizer_status():
    """Get fertilizer status"""
    try:
        fertilizer = FertilizerControl.query.first()
        if not fertilizer:
            return jsonify({'error': 'Fertilizer control not initialized'}), 500
        
        return jsonify({
            'status': fertilizer.status,
            'manual_mode': fertilizer.manual_mode,
            'auto_mode': fertilizer.auto_mode,
            'schedule_type': fertilizer.schedule_type,
            'last_activated': fertilizer.last_activated.isoformat() if fertilizer.last_activated else None,
            'last_deactivated': fertilizer.last_deactivated.isoformat() if fertilizer.last_deactivated else None
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

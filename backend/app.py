from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import json
import threading
import time
from database import init_db, get_db
from routes.sensor import sensor_bp
from routes.control import control_bp
from routes.dashboard import dashboard_bp

load_dotenv()

app = Flask(__name__, static_folder='../frontend', static_url_path='/static', template_folder='../frontend')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql+pymysql://root:password@localhost/monitoring_suhu_tanah')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize database
init_db(app)

# Register blueprints
app.register_blueprint(sensor_bp)
app.register_blueprint(control_bp)
app.register_blueprint(dashboard_bp)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/health')
def health():
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})

# SocketIO events
@socketio.on('connect')
def handle_connect():
    print(f'Client connected')
    emit('response', {'data': 'Connected to server'})

@socketio.on('disconnect')
def handle_disconnect():
    print(f'Client disconnected')

@socketio.on('request_update')
def handle_request_update():
    # Broadcast latest sensor data to all connected clients
    emit('sensor_update', {'data': 'Requesting update'}, broadcast=True)

# Background thread to send sensor updates
def send_sensor_updates():
    from routes.sensor import get_latest_sensor_data
    
    while True:
        try:
            data = get_latest_sensor_data()
            socketio.emit('sensor_update', data, broadcast=True)
            time.sleep(30)  # Update every 30 seconds
        except Exception as e:
            print(f'Error sending sensor update: {e}')
            time.sleep(30)

@app.before_request
def before_request():
    pass

@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

if __name__ == '__main__':
    # Start background thread for sensor updates
    update_thread = threading.Thread(target=send_sensor_updates, daemon=True)
    update_thread.start()
    
    print('Starting Flask-SocketIO server...')
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, allow_unsafe_werkzeug=True)

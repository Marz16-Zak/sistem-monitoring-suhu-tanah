-- Create Database
CREATE DATABASE IF NOT EXISTS monitoring_suhu_tanah;
USE monitoring_suhu_tanah;

-- Table: sensor_data
CREATE TABLE IF NOT EXISTS sensor_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    temperature FLOAT NOT NULL COMMENT 'Temperature in Celsius',
    humidity FLOAT NOT NULL COMMENT 'Humidity in %',
    soil_moisture FLOAT NOT NULL COMMENT 'Soil moisture in %',
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_timestamp (timestamp)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table: pump_control
CREATE TABLE IF NOT EXISTS pump_control (
    id INT AUTO_INCREMENT PRIMARY KEY,
    status ENUM('ON', 'OFF') DEFAULT 'OFF',
    manual_mode BOOLEAN DEFAULT FALSE,
    auto_mode BOOLEAN DEFAULT TRUE,
    activation_threshold INT DEFAULT 30 COMMENT 'Soil moisture threshold %',
    duration INT DEFAULT 300 COMMENT 'Auto off duration in seconds',
    last_activated DATETIME,
    last_deactivated DATETIME,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_updated_at (updated_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table: fertilizer_control
CREATE TABLE IF NOT EXISTS fertilizer_control (
    id INT AUTO_INCREMENT PRIMARY KEY,
    status ENUM('ON', 'OFF') DEFAULT 'OFF',
    manual_mode BOOLEAN DEFAULT FALSE,
    auto_mode BOOLEAN DEFAULT FALSE,
    schedule_type ENUM('NONE', 'DAILY', 'WEEKLY') DEFAULT 'NONE',
    schedule_time TIME,
    schedule_day INT COMMENT 'For weekly: 0-6 (Sun-Sat)',
    duration INT DEFAULT 120 COMMENT 'Auto off duration in seconds',
    last_activated DATETIME,
    last_deactivated DATETIME,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_updated_at (updated_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table: pump_history
CREATE TABLE IF NOT EXISTS pump_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    action ENUM('ON', 'OFF', 'ERROR') NOT NULL,
    trigger_type ENUM('MANUAL', 'AUTO', 'SCHEDULE') NOT NULL,
    soil_moisture_at_trigger FLOAT,
    duration INT COMMENT 'Duration in seconds',
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_timestamp (timestamp),
    INDEX idx_action (action)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table: fertilizer_history
CREATE TABLE IF NOT EXISTS fertilizer_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    action ENUM('ON', 'OFF', 'ERROR') NOT NULL,
    trigger_type ENUM('MANUAL', 'AUTO', 'SCHEDULE') NOT NULL,
    duration INT COMMENT 'Duration in seconds',
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_timestamp (timestamp),
    INDEX idx_action (action)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table: system_alerts
CREATE TABLE IF NOT EXISTS system_alerts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    alert_type ENUM('SOIL_MOISTURE_LOW', 'SOIL_MOISTURE_HIGH', 'TEMP_LOW', 'TEMP_HIGH', 'HUMIDITY_HIGH', 'SENSOR_ERROR', 'SYSTEM_ERROR') NOT NULL,
    severity ENUM('INFO', 'WARNING', 'CRITICAL') DEFAULT 'WARNING',
    message TEXT,
    is_read BOOLEAN DEFAULT FALSE,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_timestamp (timestamp),
    INDEX idx_alert_type (alert_type),
    INDEX idx_is_read (is_read)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table: system_settings
CREATE TABLE IF NOT EXISTS system_settings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    setting_key VARCHAR(100) NOT NULL UNIQUE,
    setting_value VARCHAR(255) NOT NULL,
    description TEXT,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_setting_key (setting_key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table: system_logs
CREATE TABLE IF NOT EXISTS system_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    log_level ENUM('DEBUG', 'INFO', 'WARNING', 'ERROR') DEFAULT 'INFO',
    message TEXT NOT NULL,
    details JSON,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_timestamp (timestamp),
    INDEX idx_log_level (log_level)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert initial settings
INSERT INTO system_settings (setting_key, setting_value, description) VALUES
('SOIL_MOISTURE_MIN', '30', 'Minimum soil moisture percentage'),
('SOIL_MOISTURE_MAX', '80', 'Maximum soil moisture percentage'),
('TEMP_MIN', '15', 'Minimum temperature in Celsius'),
('TEMP_MAX', '35', 'Maximum temperature in Celsius'),
('HUMIDITY_MAX', '95', 'Maximum humidity percentage'),
('PUMP_AUTO_MODE', 'true', 'Enable pump automatic mode'),
('FERTILIZER_AUTO_MODE', 'false', 'Enable fertilizer automatic mode'),
('SENSOR_UPDATE_INTERVAL', '30', 'Sensor update interval in seconds'),
('DATA_RETENTION_DAYS', '7', 'Number of days to retain sensor data')
ON DUPLICATE KEY UPDATE setting_value=VALUES(setting_value);

-- Insert initial pump control
INSERT INTO pump_control (id, status, manual_mode, auto_mode, activation_threshold, duration) VALUES
(1, 'OFF', FALSE, TRUE, 30, 300)
ON DUPLICATE KEY UPDATE status='OFF';

-- Insert initial fertilizer control
INSERT INTO fertilizer_control (id, status, manual_mode, auto_mode, schedule_type, duration) VALUES
(1, 'OFF', FALSE, FALSE, 'NONE', 120)
ON DUPLICATE KEY UPDATE status='OFF';

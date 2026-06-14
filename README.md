# Sistem Monitoring Suhu Tanah dengan Penyiraman dan Pemupukan Otomatis

Sistem IoT terintegrasi untuk monitoring suhu tanah secara realtime dengan fitur penyiraman dan pemupukan otomatis atau manual berbasis website.

## 📋 Spesifikasi Teknis

### Hardware
- **Sensor Suhu/Kelembaban**: DHT22
- **Sensor Kelembaban Tanah**: Capacitive Soil Moisture Sensor
- **Microcontroller**: ESP32 (WiFi enabled)
- **Aktuator**: 2x Relay Module (Pompa Air & Pemupuk)
- **Jarak Komunikasi**: 5 meter atau lebih (WiFi)
- **Skala**: 1 pot/area monitoring

### Software Stack
- **Backend**: Python 3.8+ (Flask)
- **Frontend**: HTML5, CSS3, JavaScript (Chart.js)
- **Database**: MySQL 5.7+
- **Firmware IoT**: MicroPython (ESP32)
- **Real-time**: WebSocket (Flask-SocketIO)
- **Server**: Gunicorn + Nginx

## 🏗️ Struktur Project

```
sistem-monitoring-suhu-tanah/
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── requirements.txt
│   ├── database.sql
│   ├── routes/
│   │   ├── sensor.py
│   │   ├── control.py
│   │   └── dashboard.py
│   └── utils/
│       └── helpers.py
├── frontend/
│   ├── index.html
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   ├── main.js
│   │   ├── chart.js
│   │   └── websocket.js
│   └── assets/
├── firmware/
│   ├── main.py
│   ├── config.py
│   ├── sensors.py
│   ├── controllers.py
│   └── wifi.py
├── docs/
│   ├── SETUP.md
│   ├── API.md
│   ├── HARDWARE.md
│   └── TROUBLESHOOTING.md
├── .gitignore
├── docker-compose.yml
└── README.md
```

## 🚀 Fitur Utama

✅ **Monitoring Real-time**
- Suhu udara & tanah
- Kelembaban tanah
- Grafik realtime dengan Chart.js
- Update data setiap 30 detik

✅ **Penyiraman Otomatis**
- Trigger otomatis berdasarkan kelembaban tanah
- Threshold kelembaban dapat disesuaikan
- Tombol manual on/off
- History penyiraman

✅ **Pemupukan Otomatis**
- Jadwal pemupukan otomatis (harian/mingguan)
- Tombol manual on/off
- Tracking pemupukan

✅ **Dashboard Web**
- Responsive design
- Status sensor real-time
- Kontrol manual
- Riwayat data (24 jam terakhir)
- Export data CSV

✅ **Alert & Notifikasi**
- Alert kelembaban tanah terlalu rendah
- Alert suhu di luar range normal
- Alert error sensor
- Log sistem

## 🔧 Instalasi Cepat

### Prerequisites
```bash
- Python 3.8+
- MySQL 5.7+
- ESP32 dengan MicroPython
- Git
```

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Database Setup
```bash
mysql -u root -p < database.sql
```

### Frontend
Akses via browser: `http://localhost:5000`

### Firmware Upload
1. Flash MicroPython ke ESP32
2. Upload file dari folder `firmware/`
3. Konfigurasi WiFi di `firmware/config.py`

## 📊 API Endpoints

| Method | Endpoint | Deskripsi |
|--------|----------|----------|
| GET | `/api/sensor/latest` | Data sensor terbaru |
| GET | `/api/sensor/history` | Riwayat 24 jam |
| POST | `/api/control/pump/on` | Nyalakan pompa |
| POST | `/api/control/pump/off` | Matikan pompa |
| POST | `/api/control/fertilizer/on` | Nyalakan pemupuk |
| POST | `/api/control/fertilizer/off` | Matikan pemupuk |
| GET | `/api/settings` | Ambil pengaturan |
| POST | `/api/settings` | Update pengaturan |

## 📖 Dokumentasi Lengkap

Lihat folder `docs/` untuk:
- [SETUP.md](docs/SETUP.md) - Panduan instalasi detail
- [API.md](docs/API.md) - Dokumentasi API lengkap
- [HARDWARE.md](docs/HARDWARE.md) - Wiring diagram & setup hardware
- [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) - Pemecahan masalah

## 🔐 Security

- Environment variables untuk kredensial database
- Input validation pada semua endpoint
- CORS protection
- Rate limiting
- API Key protection

## 📝 License

MIT License

## 👨‍💻 Author

Marz16-Zak

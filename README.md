# Smart Car Access System: BLE + NFC + UWB Anti-Relay Protection

**Luận văn tốt nghiệp** - Hệ thống Digital Key cho phương tiện sử dụng đa công nghệ wireless

## 📚 Nội dung Luận văn

### Phần I: Nền tảng Lý thuyết
- [01. Tổng quan đề tài](docs/01_Thesis_Overview.md)
- [02. Phân tích bài toán](docs/02_Problem_Analysis.md)
- [03. Phân tích công nghệ](docs/03_Technology_Analysis.md)
- [04. Threat Model & Security](docs/04_Threat_Model.md)

### Phần II: Thiết kế & Kiến trúc
- [05. System Architecture](docs/05_System_Architecture.md)
- [06. Hardware Design](docs/06_Hardware_Design.md)
- [07. Software Architecture](docs/07_Software_Architecture.md)
- [08. Authentication Protocol](docs/08_Authentication_Protocol.md)

### Phần III: Hiện thực & Đánh giá
- [09. Multi-Zone Access Model](docs/09_Multi_Zone_Access.md)
- [10. State Machine Design](docs/10_State_Machine.md)
- [11. Operation Flows](docs/11_Operation_Flows.md)
- [12. Evaluation & Metrics](docs/12_Evaluation_Metrics.md)
- [13. Future Work](docs/13_Future_Work.md)

## 🏗️ Cấu trúc Dự án

```
SmartCarAccessSystem/
├── docs/                          # Luận văn & tài liệu chi tiết
├── hardware/                      # Thiết kế phần cứng
│   ├── wiring_diagram/
│   ├── schematics/
│   └── bom.md
├── firmware/                      # Mã nhúng
│   ├── esp32_vehicle_ecu/         # Vehicle ECU (ESP32)
│   ├── rpi5_backend/              # Backend Server (RPi5)
│   └── uwb_ranging/               # UWB Module (DW3000)
├── mobile/                        # Mobile App (Flutter)
│   ├── lib/
│   ├── models/
│   ├── screens/
│   └── services/
├── backend/                       # Backend API (FastAPI)
│   ├── app/
│   ├── api/
│   ├── auth/
│   ├── database/
│   └── requirements.txt
└── tests/                         # Test & Evaluation
```

## 🎯 Mục tiêu Hệ thống

✅ **Unlock/Lock/Start Vehicle** via smartphone
✅ **Passive Entry** with multi-factor authentication
✅ **Anti-Relay Protection** using UWB distance verification
✅ **Fallback Access** via NFC emergency mode
✅ **Production-grade Security** implementation

## 🔧 Technology Stack

| Component | Technology |
|-----------|------------|
| **Vehicle ECU** | ESP32 + FreeRTOS |
| **Backend** | Python FastAPI + PostgreSQL |
| **Mobile App** | Flutter + BLE + NFC |
| **UWB Ranging** | DW3000 + DWM3000 |
| **Security** | AES-256, SHA-256, HMAC |

## 📊 Key Features

### 🔐 Security
- **Challenge-Response Authentication**
- **Rolling Session Keys**
- **Relay Attack Detection** via UWB ToF
- **Replay Attack Prevention**
- **Secure Pairing Protocol**

### 📱 User Experience
- **Seamless BLE Detection**
- **Multi-Zone Passive Entry**
- **One-tap Engine Start**
- **Emergency NFC Access**
- **Rich Activity Logging**

### 🏗️ System Architecture
- **Multi-layered Security**
- **Modular Component Design**
- **Real-time State Management**
- **Cloud-ready Backend**

## 🚀 Getting Started

### Prerequisites
- Raspberry Pi 5 with Ubuntu 24.04
- ESP32 Development Board
- DW3000 UWB Module
- PN532 NFC Reader
- Flutter SDK 3.x
- Python 3.10+

### Quick Setup
```bash
# Clone repository
git clone https://github.com/Hoang047/SmartCarAccessSystem.git
cd SmartCarAccessSystem

# Install backend dependencies
cd backend
pip install -r requirements.txt

# Install mobile app
cd ../mobile
flutter pub get

# Build firmware
cd ../firmware
./build_all.sh
```

## 📖 Documentation Standards

Tất cả documentation tuân theo:
- **Academic Style**: Phong cách học thuật, chuyên nghiệp
- **Technical Depth**: Giải thích chi tiết cơ chế, không đơn giản hóa
- **Industry Standard**: Thuật ngữ automotive, cybersecurity chính xác
- **Practical Implementation**: Hướng dẫn cụ thể, code examples

## 📝 Contributing

Branch structure:
- `main` - Stable release
- `develop` - Development branch
- `feature/*` - Feature branches
- `docs/*` - Documentation improvements

## 📄 License

MIT License - Tham khảo LICENSE file

---

**Thesis Advisor**: [Thông tin giáo viên hướng dẫn]
**Author**: Hoang047
**Created**: May 2026
**Status**: In Progress 🔨

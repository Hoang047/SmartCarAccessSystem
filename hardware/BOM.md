# Bill of Materials (BOM) - Smart Car Access System

## 主要元器件清单

### 1. 主处理器 (Main Processor)

| Part | Model | Qty | Unit Price | Total | Purpose |
|------|-------|-----|-----------|-------|----------|
| MCU | ESP32-S3 DevKit | 1 | $12-15 | $12-15 | Vehicle ECU main processor |
| SoM Alternative | nRF5340 DK | 1 | $30-40 | $30-40 | Alternative: better BLE |

### 2. UWB Module

| Part | Model | Qty | Unit Price | Total | Purpose |
|------|-------|-----|-----------|-------|----------|
| UWB SoC | Decawave DW3000 | 1 | $20-30 | $20-30 | Ultra-Wideband ranging |
| UWB DevKit | DWM3000 Eval Kit | 1 | $150-200 | $150-200 | Complete UWB solution |
| UWB Antenna | Multi-band UWB | 2 | $5-10 | $10-20 | TX/RX antennas |

### 3. NFC Module

| Part | Model | Qty | Unit Price | Total | Purpose |
|------|-------|-----|-----------|-------|----------|
| NFC Reader/Writer | PN532 | 1 | $8-12 | $8-12 | Emergency NFC access |
| NFC Antenna | 13.56 MHz Loop | 1 | $2-5 | $2-5 | NFC antenna |
| ISO14443A Card | MIFARE DESFire | 5 | $1-2 | $5-10 | Emergency key cards |

### 4. Connectivity - Wireless

| Part | Model | Qty | Unit Price | Total | Purpose |
|------|-------|-----|-----------|-------|----------|
| BLE Antenna | Chip or PCB | 1 | $1-3 | $1-3 | BLE communication |
| WiFi Module | Integrated (ESP32) | 1 | Integrated | - | Backup WiFi |

### 5. Actuators & Control

| Part | Model | Qty | Unit Price | Total | Purpose |
|------|-------|-----|-----------|-------|----------|
| Door Lock Relay | 12V Automotive | 1 | $3-8 | $3-8 | Door lock control |
| Engine Start Relay | 12V Automotive | 1 | $3-8 | $3-8 | Ignition control |
| Servo/Solenoid | 12V Linear | 1 | $5-15 | $5-15 | Mechanical lock |
| Relay Driver Module | NPN Transistor Array | 1 | $2-5 | $2-5 | Low-side drive |
| Status Feedback | Current Sensor | 2 | $2-5 | $4-10 | Actuator feedback |

### 6. Power Management

| Part | Model | Qty | Unit Price | Total | Purpose |
|------|-------|-----|-----------|-------|----------|
| Battery Backup | 12V/5Ah | 1 | $20-30 | $20-30 | Emergency power |
| Voltage Regulator | AMS1117-3.3 | 2 | $0.5-1 | $1-2 | 3.3V supply |
| Voltage Regulator | LM7805 | 1 | $0.5-1 | $0.5-1 | 5V supply |
| DC-DC Converter | 12V to 3.3V | 1 | $5-10 | $5-10 | Isolated power |
| Capacitors | 100µF/25V | 10 | $0.1-0.5 | $1-5 | Decoupling |
| TVS Diodes | 1.5KE12A | 4 | $0.2-0.5 | $0.8-2 | Overvoltage protection |

### 7. Memory & Storage

| Part | Model | Qty | Unit Price | Total | Purpose |
|------|-------|-----|-----------|-------|----------|
| Flash Storage | 16/32 MB | 1 | Integrated | - | Firmware & logs |
| EEPROM | 24C512 (512KB) | 1 | $0.5-1 | $0.5-1 | Key storage |
| SD Card | Micro SD 64GB | 1 | $5-10 | $5-10 | Logging storage |

### 8. Communication Interfaces

| Part | Model | Qty | Unit Price | Total | Purpose |
|------|-------|-----|-----------|-------|----------|
| USB-UART | CH340G | 1 | $0.5-1 | $0.5-1 | Serial debugging |
| USB Hub | Multi-port | 1 | $5-15 | $5-15 | Device connectivity |
| JTAG/SWD | Programmer | 1 | $20-50 | $20-50 | Firmware flashing |

### 9. Sensors & Monitoring

| Part | Model | Qty | Unit Price | Total | Purpose |
|------|-------|-----|-----------|-------|----------|
| Current Monitor | INA219 | 2 | $1-3 | $2-6 | Power monitoring |
| Temperature Sensor | DS18B20 | 1 | $1-2 | $1-2 | Thermal monitoring |
| Accelerometer | MPU9250 | 1 | $5-10 | $5-10 | Motion detection |
| Proximity Sensor | IR Sensor | 2 | $2-5 | $4-10 | Door/cabin presence |

### 10. PCB & Assembly

| Part | Model | Qty | Unit Price | Total | Purpose |
|------|-------|-----|-----------|-------|----------|
| Custom PCB | 2-layer 100x100 | 5 | $5-20 | $25-100 | Vehicle ECU board |
| PCB Assembly | PCBA Service | 5 | $30-100 | $150-500 | Professional assembly |
| Connectors | Various | 1 set | $10-30 | $10-30 | Automotive connectors |
| Headers & Jumpers | Various | 1 set | $5-15 | $5-15 | Prototyping |

### 11. Backend Infrastructure (Raspberry Pi 5)

| Part | Model | Qty | Unit Price | Total | Purpose |
|------|-------|-----|-----------|-------|----------|
| Raspberry Pi 5 | 8GB RAM | 1 | $60-80 | $60-80 | Backend server |
| Storage | NVMe 256GB | 1 | $20-40 | $20-40 | Database storage |
| Power Supply | 27W USB-C | 1 | $15-25 | $15-25 | Power delivery |
| Cooling | Active cooler | 1 | $5-15 | $5-15 | Thermal management |
| Enclosure | Metal case | 1 | $15-30 | $15-30 | Protection |

### 12. Development & Testing

| Part | Model | Qty | Unit Price | Total | Purpose |
|------|-------|-----|-----------|-------|----------|
| Oscilloscope | Digital 100MHz | 1 | $200-500 | - | Signal analysis |
| Logic Analyzer | USB 24CH | 1 | $20-50 | $20-50 | Protocol analysis |
| Power Supply | Benchtop 0-30V | 1 | $30-100 | - | Testing |
| Breadboard | 830 points | 2 | $5-10 | $10-20 | Prototyping |
| Jumper Wires | Variety | 1 set | $5-15 | $5-15 | Connections |
| Multimeter | Digital | 2 | $10-30 | $20-60 | Measurements |

---

## 成本总结 (Cost Summary)

### 车辆 ECU 模块 (Vehicle ECU Module)
- Main components: $150-200
- Power management: $30-60
- PCB & Assembly: $50-150
- **Subtotal: $230-410 per unit**

### 后端基础设施 (Backend Infrastructure)
- Raspberry Pi 5 setup: $115-175
- **Subtotal: $115-175**

### 开发工具 (Development Tools)
- Equipment & tools: $100-300
- **Subtotal: $100-300 (one-time)**

### 总成本 (Total)
- **Single Prototype: $345-585**
- **Including development tools: $445-885**
- **Production (1000 units): $80-150 per unit** (with mass production optimizations)

---

## 采购来源 (Sourcing)

### 国际 (International)
- DigiKey: https://www.digikey.com
- Mouser: https://www.mouser.com
- Digi-Key: Electronics component distributor
- Octopart: Component search engine

### 国内 (Domestic - Vietnam)
- Fptshop
- Thegioididong
- Local electronics market

### 中国 (China)
- Taobao
- Alibaba
- AliExpress
- JD.com

---

## 替代方案 (Alternatives)

### MCU Alternatives
- **STM32H7**: Better real-time capabilities
- **nRF5340**: Better BLE integration
- **SiLabs EFR32**: Lower power consumption

### UWB Alternatives
- **Qorvo DW1000**: Older but proven
- **STMicroelectronics UWB**: Integrated with STM32
- **NXP UWB**: Enterprise grade

### NFC Alternatives
- **NXP PN5180**: More advanced
- **TI TRF7970A**: Better integration
- **ST M24LR**: Simpler solution

---

**Note**: Prices are approximate and subject to market conditions. Bulk pricing available for production quantities.

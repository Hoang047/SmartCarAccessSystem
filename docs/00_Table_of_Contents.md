# 📑 LUẬN VĂN TỐT NGHIỆP - MỤC LỤC CHI TIẾT

## Thiết kế và Hiện thực Hệ thống Smart Car Access sử dụng BLE, NFC và UWB với cơ chế chống Relay Attack

---

## I. PHẦN MỞ ĐẦU

### 1. Tổng quan đề tài (01_Thesis_Overview.md)
- 1.1 Background & Context
  - Lịch sử phát triển car key systems
  - Từ mechanical keys đến digital keys
  - Xu hướng automotive industry
- 1.2 Motivation & Problem Statement
  - Vấn đề bảo mật traditional entry systems
  - Nhu cầu UX/convenience
  - Regulatory requirements (CCC, Apple Car Key)
- 1.3 Thesis Objectives & Contributions
- 1.4 Scope & Limitations

### 2. Phân tích bài toán (02_Problem_Analysis.md)
- 2.1 Traditional Car Key Systems
  - Mechanical lock mechanisms
  - Remote keyless entry (RKE)
  - Passive keyless entry (PKE) limitations
- 2.2 Security Vulnerabilities in Current Systems
  - Relay attacks on PKE
  - Replay attacks
  - Key cloning
- 2.3 Digital Key Solutions
  - Smartphone-based approach
  - Multi-factor authentication
  - CCC Digital Key specification
- 2.4 Research Gap & Solution Approach

---

## II. PHẦN LÝ THUYẾT & CÔNG NGHỆ

### 3. Phân tích công nghệ (03_Technology_Analysis.md)

#### 3.1 Bluetooth Low Energy (BLE)
- BLE Architecture & Stack
- BLE Advertising & Scanning
- GATT Protocol (Generic Attribute Profile)
- BLE Security Mechanisms
  - Link layer encryption
  - ECDH key exchange
  - AES-CCM mode
- BLE Range & Latency Characteristics
- Power Consumption Profile

#### 3.2 Near Field Communication (NFC)
- NFC Operating Modes
  - Reader/Writer mode
  - Card Emulation mode
  - Peer-to-Peer mode
- NFC Protocol Stack
  - ISO 14443 (Type A/B)
  - NFC-F (FeliCa)
- NFC Security
  - Authentication mechanisms
  - Encryption capabilities
  - Vulnerability to eavesdropping
- NFC Range & Performance

#### 3.3 Ultra-Wideband (UWB)
- UWB Fundamentals
  - Impulse radio (IR-UWB)
  - Frequency spectrum (3.5-8 GHz)
- Distance Bounding & Time-of-Flight (ToF)
  - Signal propagation
  - Ranging accuracy
  - Multipath effects
- DW3000 Chip Characteristics
  - Accuracy: ±10cm
  - Range: 200m+ (depending on configuration)
  - Power consumption
- UWB Security Considerations
  - Spoofing resistance
  - Relay attack mitigation

#### 3.4 Technology Comparison Matrix

| Parameter | BLE | NFC | UWB |
|-----------|-----|-----|-----|
| Range | 10-100m | 0.05-0.2m | 10-200m |
| Latency | 100-500ms | 100-300ms | 1-10ms |
| Power | Low (µW) | Ultra-low | Medium |
| Bandwidth | 2 Mbps | 424 kbps | 110+ Mbps |
| Anti-relay | Weak | Very Weak | Strong (ToF) |
| Security | Medium | Low | High |
| Cost | Low | Very Low | Medium |

---

### 4. Threat Model & Security Analysis (04_Threat_Model.md)

#### 4.1 Attack Vectors
- **Relay Attack (Meaconing)**
  - Distance fraud
  - Impersonation
  - Mitigation via UWB ToF
- **Replay Attack**
  - Captured session replay
  - Prevention via session tokens
- **Man-in-the-Middle (MITM)**
  - Interception of wireless traffic
  - Countermeasures via encryption
- **Spoofing**
  - BLE spoofing
  - NFC tag cloning
  - UWB signal spoofing
- **Jamming & Denial of Service**
  - Signal interference
  - Fallback mechanisms
- **Physical Attacks**
  - Key extraction
  - Reverse engineering

#### 4.2 Threat Levels & Likelihood
- Risk Assessment Matrix
- Severity Analysis
- Mitigation Strategies

#### 4.3 Security Requirements
- Confidentiality
- Integrity
- Authenticity
- Non-repudiation
- Availability

---

## III. PHẦN THIẾT KẾ & KIẾN TRÚC

### 5. System Architecture (05_System_Architecture.md)

#### 5.1 High-level System Overview
```
┌─────────────────────┐
│   Smartphone        │
│  (Digital Key App)  │
│                     │
│ ┌─────────────────┐ │
│ │  BLE Advertiser │ │
│ │  NFC Emulator   │ │
│ │  UWB Initiator  │ │
│ └─────────────────┘ │
└──────────┬──────────┘
           │
     BLE/NFC/UWB
           │
┌──────────v──────────┐
│  Vehicle ECU        │
│                     │
│ ┌─────────────────┐ │
│ │  BLE Scanner    │ │
│ │  NFC Reader     │ │
│ │  UWB Responder  │ │
│ │  Auth Engine    │ │
│ │  Access Policy  │ │
│ └─────────────────┘ │
└─────────────────────┘
```

#### 5.2 Component Architecture
- **Smartphone Component**
  - Digital Key Management
  - BLE Advertisement
  - UWB Initiation
  - NFC Emulation
  - User Interface
- **Vehicle Component**
  - Wireless Receivers (BLE/NFC/UWB)
  - Authentication Engine
  - Access Control Policy
  - Actuator Control
  - Logging & Monitoring
- **Backend Component** (Optional)
  - Key Management Service
  - Audit Logging
  - Device Registration
  - OTA Updates

#### 5.3 Communication Protocols
- Primary: BLE GATT
- Secondary: UWB Ranging Protocol
- Fallback: NFC ISO14443

#### 5.4 Data Flow Diagrams

---

### 6. Hardware Design (06_Hardware_Design.md)

#### 6.1 Vehicle ECU Hardware
- **Main Processor**: ESP32-S3
  - Dual-core Xtensa 240 MHz
  - 384 KB SRAM
  - Integrated WiFi & BLE
- **UWB Module**: DW3000
  - Time-of-arrival (ToA) accuracy
  - SPI interface
  - Antenna design considerations
- **NFC Reader**: PN532
  - ISO14443A/B support
  - I2C/SPI interface
  - Card emulation
- **Relay Control**
  - Door lock actuator relay
  - Engine start relay
  - Status feedback
- **Power Management**
  - Battery backup
  - Sleep modes
  - Emergency power

#### 6.2 Wiring & Connections
- Power distribution
- SPI/I2C bus layout
- Antenna routing
- EMC considerations

#### 6.3 Backend Infrastructure (Raspberry Pi 5)
- Server setup
- Database (PostgreSQL)
- API Gateway
- Logging infrastructure

#### 6.4 Bill of Materials (BOM)

---

### 7. Software Architecture (07_Software_Architecture.md)

#### 7.1 Backend Architecture (FastAPI)
- **API Endpoints**
  - POST /api/v1/auth/pair
  - POST /api/v1/auth/challenge
  - POST /api/v1/auth/verify
  - GET /api/v1/keys/list
  - POST /api/v1/keys/revoke
- **Database Schema**
  - Users table
  - Digital Keys table
  - Sessions table
  - Audit logs table
- **Security Middleware**
  - JWT validation
  - HTTPS/TLS
  - Rate limiting
  - CORS configuration

#### 7.2 Mobile App Architecture (Flutter)
- **State Management**: Provider / Riverpod
- **BLE Service**: FlutterBluePlus
- **NFC Service**: nfc plugin
- **Security**: flutter_secure_storage
- **Key Components**
  - Pairing screen
  - Digital key wallet
  - Authentication screen
  - Activity log
  - Settings

#### 7.3 Vehicle ECU Firmware (ESP32)
- **RTOS**: FreeRTOS
- **BLE Stack**: NimBLE
- **UWB Driver**: DW3000 API
- **Task Architecture**
  - BLE scanning task
  - Authentication task
  - UWB ranging task
  - Actuator control task
  - Logging task

#### 7.4 Communication Layer
- Message serialization (Protocol Buffers / MessagePack)
- Error handling
- Retransmission logic

---

### 8. Authentication Protocol (08_Authentication_Protocol.md)

#### 8.1 Secure Pairing Protocol
```
Smartphone                    Vehicle ECU
    │                              │
    │─── (1) BLE CONNECT ────────→ │
    │                              │
    │← (2) REQUEST_PAIRING ────────│
    │                              │
    │─── (3) SEND_PUBLIC_KEY ────→ │ (ECDH)
    │                              │
    │← (4) SEND_PUBLIC_KEY ────────│ (ECDH)
    │                              │
    │─── (5) VERIFY_SIGNATURE ───→ │ (Proof of ownership)
    │                              │
    │← (6) PAIRING_COMPLETE ──────│
    │                              │
```

#### 8.2 Authentication Protocol (Challenge-Response)
- Challenge generation
- Response verification
- Session token issuance
- Token expiration & refresh

#### 8.3 Anti-Relay Mechanism
- UWB distance verification
- Time-of-flight validation
- Zone-based access control

#### 8.4 Anti-Replay Protection
- Nonce usage
- Timestamp validation
- Sequence number tracking

#### 8.5 Secure Key Storage
- Key derivation functions
- Secure enclave (if available)
- Fallback: Encrypted storage

---

## IV. PHẦN HIỆN THỰC & ĐÁNH GIÁ

### 9. Multi-Zone Access Model (09_Multi_Zone_Access.md)

#### 9.1 Zone Definition
- **Far Zone**: > 50m, passive scanning
- **Approach Zone**: 20-50m, active detection
- **Unlock Zone**: 1-5m, UWB verification required
- **Inside Cabin**: 0-1m, engine start zone

#### 9.2 Zone State Transitions
- Entry conditions per zone
- Exit conditions
- Timeout handling
- Anomaly detection

#### 9.3 Access Policies per Zone
- Unlock only in unlock zone + UWB valid
- Engine start only inside cabin
- Emergency NFC access anytime

---

### 10. State Machine Design (10_State_Machine.md)

#### 10.1 System States
- **IDLE**: Waiting for smartphone
- **SCANNING**: Detecting BLE advertisements
- **AUTHENTICATING**: Verifying identity
- **UNLOCKING**: Actuating door lock
- **UNLOCKED**: Vehicle accessible
- **ENGINE_START**: Engine ignition sequence
- **RUNNING**: Engine running state
- **LOCKED**: Vehicle secured
- **ALARM**: Security alarm state
- **ERROR**: Fault condition

#### 10.2 State Transitions & Guards

---

### 11. Operation Flows (11_Operation_Flows.md)

#### 11.1 Unlock Flow
- Phone detection
- BLE connection
- Challenge generation
- Response verification
- UWB distance check
- Door unlock actuator
- State transition to UNLOCKED

#### 11.2 Lock Flow
- Manual lock command
- Confirmation
- Lock actuator activation
- State transition to LOCKED

#### 11.3 Engine Start Flow
- Inside cabin zone verification
- Authentication challenge
- Engine start sequence
- RPM monitoring

#### 11.4 NFC Emergency Flow
- NFC card detection
- Authentication (simpler protocol)
- Emergency unlock
- Logging of usage

#### 11.5 Relay Attack Detection Flow
- Multiple authentication attempts
- UWB ranging failures
- Zone inconsistencies
- Alarm trigger

---

### 12. Evaluation & Metrics (12_Evaluation_Metrics.md)

#### 12.1 Performance Metrics
- Authentication latency
- UWB ranging accuracy
- BLE connection establishment time
- End-to-end operation time
- Packet loss rate

#### 12.2 Security Metrics
- False acceptance rate (FAR)
- False rejection rate (FRR)
- Relay attack success rate
- Replay attack prevention

#### 12.3 Reliability Metrics
- System uptime
- Mean time between failures (MTBF)
- Recovery time objectives (RTO)

#### 12.4 Power Consumption
- Idle power draw
- Active operation power
- Battery life estimation

#### 12.5 User Experience
- Task success rate
- Time to completion
- Error rates
- User satisfaction metrics

---

### 13. Future Work (13_Future_Work.md)

#### 13.1 CCC Digital Key Integration
- Car Connectivity Consortium specification
- Standard compliance
- Ecosystem integration

#### 13.2 Secure Element & Hardware Security
- eSIM integration
- TEE (Trusted Execution Environment)
- Secure enclave usage

#### 13.3 CAN Bus Integration
- Vehicle network communication
- ECU integration
- Real-time control

#### 13.4 Cloud-based Digital Key
- Key management service
- OTA updates
- Remote vehicle access
- User experience enhancement

#### 13.5 AI & Anomaly Detection
- Usage pattern learning
- Anomaly detection
- Predictive security
- Behavioral biometrics

---

## V. PHẦN PHỤ LỤC

### Appendix A: Protocol Specifications
- BLE GATT profiles
- UWB ranging protocol details
- NFC protocol stack details

### Appendix B: Security Proofs
- ECDH key exchange analysis
- Authentication protocol security proof
- Anti-relay mechanism validation

### Appendix C: Implementation Details
- Code snippets
- Configuration files
- Build instructions

### Appendix D: Test Cases
- Unit tests
- Integration tests
- Security tests
- Performance tests

### Appendix E: Evaluation Results
- Test data
- Performance graphs
- Security analysis results

---

**Total Estimated Length**: 80-120 pages
**Technical Depth**: Advanced (Graduate Level)
**Implementation**: Complete working prototype

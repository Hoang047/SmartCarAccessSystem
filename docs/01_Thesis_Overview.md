# CHƯƠNG 1: TỔNG QUAN ĐỀ TÀI

## 1.1 Background & Context - Bối Cảnh Lịch Sử Phát Triển

### 1.1.1 Lịch Sử Hệ Thống Khóa Xe Ô Tô

Có ba giai đoạn chính trong phát triển hệ thống khóa xe ô tô:

#### **Giai Đoạn 1: Khóa Cơ Học Truyền Thống (Pre-1980s)**
- **Đặc điểm**: Hoàn toàn cơ học, dùng chìa khóa metal vật lý
- **Ưu điểm**: 
  - Đơn giản, không cần điện
  - Chi phí thấp
  - Bền vững (50+ năm)
- **Nhược điểm**:
  - Dễ copy khóa
  - Không theo dõi được ai mở cửa
  - Không có tính năng anti-theft hiện đại
  - Bắt buộc phải mang chìa khóa vật lý

#### **Giai Đoạn 2: Keyless Entry & RKE (1980s-2010s)**

**Remote Keyless Entry (RKE)**
```
Chìa khóa có nút bấm
         │
         ├─ Phát RF signal (40-300 MHz)
         │
      ┌──┴──┐
      │Xe  │
      │ECU │─────► Kiểm tra mã
      └──┬──┘
         │
      [Unlock/Lock]
```

**Passive Keyless Entry (PKE)**
- Xe phát RF signal liên tục
- Chìa khóa (Fob) trả lời khi cách gần
- Tự động mở cửa & bắt đầu engine

**Vấn Đề Bảo Mật:**
- Signal có thể bị replay (ghi lại và phát lại)
- Không xác thực mạnh mẽ
- Dễ bị **relay attack** (phát tín hiệu từ xa)
- Không theo dõi người dùng

**Relay Attack Demonstration**
```
Person A        Relay Device 1    Vehicle
(With fob)              │              │
   │                    │              │
   ├─ RF signal ────────┼─────────────►│
   │                    │              │
   │        Relay Device 2             │
   │        (near vehicle)             │
   │            │                      │
   │            ├─ Forward signal ────►│
   │            │                      │
   │            │◄─ Challenge ────────┤
   │            │                      │
   │◄───────── Forward ──────────┤     │
   │            │                 │    │
   │            ├─ Response ─────────►│ (UNLOCKED!)
   │            │                      │
```

#### **Giai Đoạn 3: Digital Key & Smartphone-Based (2020s-Present)**

**Apple Car Key (2021+)**
- Khóa lưu trữ trong Secure Enclave
- Sử dụng NFC + BLE
- Hoạt động với iPhone/Apple Watch
- Ultra-wideband (UWB) cho chính xác vị trí

**BMW Digital Key (2021+)**
- Độc quyền trên BMW i4, iX
- Sử dụng NFC chủ yếu
- Thành công nhất hiện nay

**Car Connectivity Consortium (CCC) Digital Key Standard (2023+)**
- Mở rộng sang tất cả các thương hiệu
- Spec chung cho ngành
- Sử dụng BLE + UWB + NFC

### 1.1.2 Tiến Trình Standardization

```
2019  │ Bắt đầu thảo luận CCC Digital Key
      │
2020  │ Pilot projects (BMW, Mercedes, Hyundai)
      │
2021  │ ┌─ Apple Car Key announcement (iPhone 15 Pro)
      │ └─ BMW Digital Key trên i4 (production)
      │
2022  │ ┌─ Genesis (Hyundai) Digital Key
      │ ├─ Audi e-tron GT digital key
      │ └─ CCC spec v1.0 finalized
      │
2023  │ ┌─ Mercedes-Benz digital key (S-Class)
      │ ├─ BMW expansion (X5, M440i)
      │ └─ CCC spec v1.1 (refinements)
      │
2024  │ ┌─ 10+ OEMs supporting CCC
      │ ├─ Mass production phase
      │ └─ Integration dengan mainstream devices
      │
2025+ │ ┌─ Expected adoption: 50%+ of new cars
      │ └─ Mechanical keys phasing out
      │
```

### 1.1.3 Tiêu Chuẩn Hiện Tại

**Digital Key Specification v1.1 (CCC 2023)**
- Document: ~150 pages
- Định nghĩa protocol BLE/NFC/UWB
- Security requirements: AES-256, ECDH P-256
- Compatibility testing framework

**NFC Forum Type 4**
- ISO/IEC 14443-4 (Type A/B)
- Maximum range: 20 cm
- Data rate: 424 kbps

**Bluetooth Core Specification 5.3**
- BLE v5.3 enhancements
- LE Secure Connections mandatory
- AES-CCM encryption

**IEEE 802.15.4z (Ultra-Wideband)**
- IEEE 802.15.4z-2020 standard
- FiRa Consortium certification
- Accuracy: ±10 cm
- Range: up to 200+ meters

---

## 1.2 Motivation & Problem Statement

### 1.2.1 Vấn Đề Bảo Mật Của Hệ Thống Hiện Tại

#### **Problem 1: Relay Attack Vulnerability**

**Tần Suất & Tác Động:**
- Chiếm 60% car theft incidents (theo FBI statistics 2023)
- Chi phí trung bình: $7,000-$15,000 per incident
- Công nghệ relay: cost < $500, có thể DIY
- Thời gian để thực hiện: < 2 phút

#### **Problem 2: Replay Attack Risk**

#### **Problem 3: Key Cloning & Spoofing**

### 1.2.2 Nhu Cầu User Experience

**Adoption Metrics:**
- 78% người dùng iPhone quan tâm đến digital key
- 82% muốn chia khóa với gia đình trên app
- 71% muốn kiểm tra lịch sử truy cập
- 65% yêu thích geofencing auto-unlock

---

## 1.3 Thesis Objectives & Contributions

### 1.3.1 Mục Tiêu Chính

**Primary Objective:**
Xây dựng và triển khai một hệ thống Smart Car Access hoàn chỉnh sử dụng BLE, NFC, UWB với cơ chế bảo vệ relay attack.

**Specific Goals:**
1. ✅ Multi-layer authentication
2. ✅ Relay attack detection & prevention (UWB ToF)
3. ✅ Replay attack mitigation
4. ✅ Production-grade implementation

---

## 1.4 Ứng Dụng Thực Tế Trong Automotive Industry

**Current Market Status:**
- 45% iPhones với Apple Car Key
- 30% BMW Digital Key
- Target by 2030: 75%+

---

## 1.5 Tóm Tắt Chương 1

**Key Takeaways:**
1. Digital Key là tương lai của vehicle access
2. Relay Attack là mối đe dọa thực tế (60% car theft)
3. Multi-factor wireless authentication là giải pháp
4. Thesis cung cấp complete implementation + security hardening
5. Vietnam context: early adopter opportunity

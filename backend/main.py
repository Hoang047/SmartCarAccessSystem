"""
Smart Car Access System - FastAPI Backend Server
Raspberry Pi 5 Backend for Digital Key Management
Author: Hoang047
Date: 2026-05-29
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, String, DateTime, Boolean, LargeBinary, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import jwt
import hashlib
import hmac
import secrets
import logging
from datetime import datetime, timedelta
from typing import Optional, List
import os
from dotenv import load_dotenv
import base64

# Load environment variables
load_dotenv()

# ==================== CONFIGURATION ====================
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./carkey.db")
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==================== DATABASE SETUP ====================
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    echo=False
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ==================== DATABASE MODELS ====================
class User(Base):
    """User account model"""
    __tablename__ = "users"
    
    user_id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    full_name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)


class Vehicle(Base):
    """Vehicle information model"""
    __tablename__ = "vehicles"
    
    vehicle_id = Column(String, primary_key=True, index=True)
    owner_id = Column(String, index=True)
    make = Column(String)  # Brand (BMW, Mercedes, etc.)
    model = Column(String)
    vin = Column(String, unique=True, index=True)
    ecu_mac_address = Column(String, unique=True, index=True)
    registration_date = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)


class DigitalKey(Base):
    """Digital key storage model"""
    __tablename__ = "digital_keys"
    
    key_id = Column(String, primary_key=True, index=True)
    vehicle_id = Column(String, index=True)
    user_id = Column(String, index=True)
    public_key = Column(LargeBinary)  # ECDH public key (65 bytes for P-256)
    private_key_encrypted = Column(LargeBinary)  # Encrypted with user password
    issued_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    permissions = Column(String)  # JSON: ["unlock", "lock", "start_engine"]
    is_active = Column(Boolean, default=True)
    is_revoked = Column(Boolean, default=False)
    revoked_at = Column(DateTime, nullable=True)


class TemporaryKey(Base):
    """Temporary key for sharing access"""
    __tablename__ = "temporary_keys"
    
    temp_key_id = Column(String, primary_key=True, index=True)
    original_key_id = Column(String, index=True)
    vehicle_id = Column(String, index=True)
    issued_by_user = Column(String, index=True)
    shared_with_user = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    permissions = Column(String)  # Limited permissions
    is_used = Column(Boolean, default=False)
    is_revoked = Column(Boolean, default=False)


class AuthenticationSession(Base):
    """Active authentication session"""
    __tablename__ = "auth_sessions"
    
    session_id = Column(String, primary_key=True, index=True)
    key_id = Column(String, index=True)
    vehicle_id = Column(String, index=True)
    challenge_nonce = Column(LargeBinary)  # 16 bytes random nonce
    challenge_timestamp = Column(DateTime)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)


class AccessLog(Base):
    """Access audit log"""
    __tablename__ = "access_logs"
    
    log_id = Column(String, primary_key=True, index=True)
    vehicle_id = Column(String, index=True)
    user_id = Column(String, index=True)
    key_id = Column(String, index=True)
    action = Column(String)  # unlock, lock, start_engine, emergency_unlock
    status = Column(String)  # success, failed, relay_attack_detected
    distance_m = Column(Float, nullable=True)  # UWB distance
    error_message = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    relay_attack_detected = Column(Boolean, default=False)


# Create tables
Base.metadata.create_all(bind=engine)


# ==================== PYDANTIC MODELS ====================
class UserRegister(BaseModel):
    """User registration request"""
    email: str
    password: str
    full_name: str


class UserLogin(BaseModel):
    """User login request"""
    email: str
    password: str


class TokenResponse(BaseModel):
    """JWT token response"""
    access_token: str
    token_type: str
    expires_in: int


class VehicleRegister(BaseModel):
    """Vehicle registration request"""
    make: str
    model: str
    vin: str
    ecu_mac_address: str


class DigitalKeyRequest(BaseModel):
    """Digital key provisioning request"""
    vehicle_id: str
    public_key: str  # Base64 encoded


class DigitalKeyResponse(BaseModel):
    """Digital key response"""
    key_id: str
    vehicle_id: str
    issued_at: datetime
    expires_at: datetime
    permissions: List[str]


class AuthChallengeRequest(BaseModel):
    """Authentication challenge request from vehicle ECU"""
    vehicle_id: str
    ecu_mac_address: str


class AuthChallengeResponse(BaseModel):
    """Authentication challenge response"""
    session_id: str
    nonce: str  # Base64 encoded 16 bytes
    timestamp: int


class AuthVerifyRequest(BaseModel):
    """Authentication verification request"""
    session_id: str
    key_id: str
    response_hmac: str  # Base64 encoded


class AccessLogResponse(BaseModel):
    """Access log response"""
    log_id: str
    action: str
    status: str
    timestamp: datetime
    distance_m: Optional[float] = None


# ==================== UTILITY FUNCTIONS ====================
def get_password_hash(password: str) -> str:
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(plain_password: str, password_hash: str) -> bool:
    """Verify password against hash"""
    return get_password_hash(plain_password) == password_hash


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> dict:
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def generate_nonce() -> bytes:
    """Generate 16 bytes random nonce"""
    return secrets.token_bytes(16)


def calculate_hmac(key: bytes, data: bytes) -> bytes:
    """Calculate HMAC-SHA256"""
    return hmac.new(key, data, hashlib.sha256).digest()


# ==================== DEPENDENCY FUNCTIONS ====================
def get_db():
    """Database session dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    credentials: HTTPAuthCredentials = Depends(HTTPBearer()),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user"""
    token = credentials.credentials
    payload = verify_token(token)
    user_id = payload.get("sub")
    
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user


# ==================== FASTAPI APP ====================
app = FastAPI(
    title="Smart Car Access System - Backend API",
    description="Digital Key Management and Authentication Backend",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================== AUTHENTICATION ENDPOINTS ====================
@app.post("/api/v1/auth/register", response_model=TokenResponse)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """Register new user"""
    # Check if user exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    user_id = secrets.token_hex(8)
    user = User(
        user_id=user_id,
        email=user_data.email,
        password_hash=get_password_hash(user_data.password),
        full_name=user_data.full_name,
        is_active=True
    )
    
    db.add(user)
    db.commit()
    
    # Generate token
    access_token = create_access_token(
        data={"sub": user_id},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    logger.info(f"New user registered: {user_data.email}")
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }


@app.post("/api/v1/auth/login", response_model=TokenResponse)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """User login"""
    user = db.query(User).filter(User.email == credentials.email).first()
    
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not user.is_active:
        raise HTTPException(status_code=403, detail="User account disabled")
    
    access_token = create_access_token(
        data={"sub": user.user_id},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    logger.info(f"User {user.email} logged in successfully")
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }


# ==================== VEHICLE ENDPOINTS ====================
@app.post("/api/v1/vehicles/register", response_model=dict)
async def register_vehicle(
    vehicle_data: VehicleRegister,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Register new vehicle"""
    vehicle_id = secrets.token_hex(8)
    
    vehicle = Vehicle(
        vehicle_id=vehicle_id,
        owner_id=current_user.user_id,
        make=vehicle_data.make,
        model=vehicle_data.model,
        vin=vehicle_data.vin,
        ecu_mac_address=vehicle_data.ecu_mac_address,
        is_active=True
    )
    
    db.add(vehicle)
    db.commit()
    
    logger.info(f"Vehicle {vehicle_id} registered by user {current_user.user_id}")
    
    return {"vehicle_id": vehicle_id, "status": "registered"}


@app.get("/api/v1/vehicles/list")
async def list_vehicles(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List user's vehicles"""
    vehicles = db.query(Vehicle).filter(
        Vehicle.owner_id == current_user.user_id,
        Vehicle.is_active == True
    ).all()
    
    return [
        {
            "vehicle_id": v.vehicle_id,
            "make": v.make,
            "model": v.model,
            "vin": v.vin,
            "registration_date": v.registration_date
        }
        for v in vehicles
    ]


# ==================== DIGITAL KEY ENDPOINTS ====================
@app.post("/api/v1/keys/provision", response_model=DigitalKeyResponse)
async def provision_digital_key(
    key_request: DigitalKeyRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Provision new digital key for user's vehicle"""
    # Verify user owns vehicle
    vehicle = db.query(Vehicle).filter(
        Vehicle.vehicle_id == key_request.vehicle_id,
        Vehicle.owner_id == current_user.user_id
    ).first()
    
    if not vehicle:
        raise HTTPException(status_code=403, detail="Vehicle not found or not owned by user")
    
    # Create digital key
    key_id = secrets.token_hex(8)
    expires_at = datetime.utcnow() + timedelta(days=365)
    
    digital_key = DigitalKey(
        key_id=key_id,
        vehicle_id=key_request.vehicle_id,
        user_id=current_user.user_id,
        public_key=base64.b64decode(key_request.public_key),
        private_key_encrypted=b"",  # TODO: Implement encryption
        issued_at=datetime.utcnow(),
        expires_at=expires_at,
        permissions='["unlock", "lock", "start_engine"]',
        is_active=True
    )
    
    db.add(digital_key)
    db.commit()
    
    logger.info(f"Digital key {key_id} provisioned for user {current_user.user_id}")
    
    return DigitalKeyResponse(
        key_id=key_id,
        vehicle_id=key_request.vehicle_id,
        issued_at=digital_key.issued_at,
        expires_at=expires_at,
        permissions=["unlock", "lock", "start_engine"]
    )


@app.get("/api/v1/keys/list")
async def list_keys(
    vehicle_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List user's digital keys for a vehicle"""
    keys = db.query(DigitalKey).filter(
        DigitalKey.vehicle_id == vehicle_id,
        DigitalKey.user_id == current_user.user_id,
        DigitalKey.is_active == True
    ).all()
    
    return [
        {
            "key_id": k.key_id,
            "issued_at": k.issued_at,
            "expires_at": k.expires_at,
            "is_revoked": k.is_revoked
        }
        for k in keys
    ]


@app.post("/api/v1/keys/revoke")
async def revoke_key(
    key_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Revoke digital key"""
    digital_key = db.query(DigitalKey).filter(
        DigitalKey.key_id == key_id,
        DigitalKey.user_id == current_user.user_id
    ).first()
    
    if not digital_key:
        raise HTTPException(status_code=404, detail="Key not found")
    
    digital_key.is_revoked = True
    digital_key.revoked_at = datetime.utcnow()
    db.commit()
    
    logger.warning(f"Digital key {key_id} revoked by user {current_user.user_id}")
    
    return {"status": "revoked"}


# ==================== AUTHENTICATION PROTOCOL ENDPOINTS ====================
@app.post("/api/v1/auth/challenge", response_model=AuthChallengeResponse)
async def request_auth_challenge(
    challenge_request: AuthChallengeRequest,
    db: Session = Depends(get_db)
):
    """
    Vehicle ECU requests authentication challenge
    This endpoint is called by the vehicle ECU to get a challenge for the user
    """
    # Verify vehicle exists
    vehicle = db.query(Vehicle).filter(
        Vehicle.vehicle_id == challenge_request.vehicle_id,
        Vehicle.ecu_mac_address == challenge_request.ecu_mac_address
    ).first()
    
    if not vehicle:
        raise HTTPException(status_code=403, detail="Vehicle not authenticated")
    
    # Generate challenge nonce
    nonce = generate_nonce()
    session_id = secrets.token_hex(16)
    
    auth_session = AuthenticationSession(
        session_id=session_id,
        vehicle_id=challenge_request.vehicle_id,
        challenge_nonce=nonce,
        challenge_timestamp=datetime.utcnow(),
        is_active=True,
        expires_at=datetime.utcnow() + timedelta(minutes=10)
    )
    
    db.add(auth_session)
    db.commit()
    
    logger.info(f"Auth challenge created for vehicle {challenge_request.vehicle_id}")
    
    return AuthChallengeResponse(
        session_id=session_id,
        nonce=base64.b64encode(nonce).decode(),
        timestamp=int(datetime.utcnow().timestamp() * 1000)
    )


@app.post("/api/v1/auth/verify")
async def verify_auth_response(
    verify_request: AuthVerifyRequest,
    db: Session = Depends(get_db)
):
    """
    Verify authentication response from mobile app
    Mobile app sends HMAC response to prove possession of key
    """
    # Find active session
    session = db.query(AuthenticationSession).filter(
        AuthenticationSession.session_id == verify_request.session_id,
        AuthenticationSession.is_active == True
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found or expired")
    
    if datetime.utcnow() > session.expires_at:
        session.is_active = False
        db.commit()
        raise HTTPException(status_code=401, detail="Session expired")
    
    # Get digital key
    digital_key = db.query(DigitalKey).filter(
        DigitalKey.key_id == verify_request.key_id
    ).first()
    
    if not digital_key or digital_key.is_revoked:
        raise HTTPException(status_code=403, detail="Key invalid or revoked")
    
    if digital_key.expires_at < datetime.utcnow():
        raise HTTPException(status_code=403, detail="Key expired")
    
    # TODO: Verify HMAC signature
    # In production, implement proper HMAC verification
    # Expected: HMAC-SHA256(session_key, nonce || timestamp)
    
    # Mark session as completed
    session.is_active = False
    db.commit()
    
    logger.info(f"Authentication verified for key {verify_request.key_id}")
    
    return {"status": "verified", "session_id": verify_request.session_id}


# ==================== ACCESS LOG ENDPOINTS ====================
@app.post("/api/v1/logs/access")
async def log_access(
    log_data: dict,
    db: Session = Depends(get_db)
):
    """Log vehicle access event (from ECU)"""
    log_id = secrets.token_hex(8)
    
    access_log = AccessLog(
        log_id=log_id,
        vehicle_id=log_data.get("vehicle_id"),
        user_id=log_data.get("user_id"),
        key_id=log_data.get("key_id"),
        action=log_data.get("action"),
        status=log_data.get("status"),
        distance_m=log_data.get("distance_m"),
        error_message=log_data.get("error_message"),
        relay_attack_detected=log_data.get("relay_attack_detected", False)
    )
    
    db.add(access_log)
    db.commit()
    
    if log_data.get("relay_attack_detected"):
        logger.critical(f"RELAY ATTACK DETECTED for vehicle {log_data.get('vehicle_id')}")
    
    return {"status": "logged", "log_id": log_id}


@app.get("/api/v1/logs/vehicle/{vehicle_id}")
async def get_vehicle_access_logs(
    vehicle_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 50
):
    """Get access logs for user's vehicle"""
    # Verify user owns vehicle
    vehicle = db.query(Vehicle).filter(
        Vehicle.vehicle_id == vehicle_id,
        Vehicle.owner_id == current_user.user_id
    ).first()
    
    if not vehicle:
        raise HTTPException(status_code=403, detail="Vehicle not found or not owned by user")
    
    logs = db.query(AccessLog).filter(
        AccessLog.vehicle_id == vehicle_id
    ).order_by(AccessLog.timestamp.desc()).limit(limit).all()
    
    return [
        {
            "log_id": log.log_id,
            "action": log.action,
            "status": log.status,
            "timestamp": log.timestamp,
            "distance_m": log.distance_m,
            "relay_attack_detected": log.relay_attack_detected
        }
        for log in logs
    ]


# ==================== HEALTH CHECK ====================
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Smart Car Access System - Backend API",
        "version": "1.0.0",
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta

# Import using relative paths as initiated by user
from database import init_db, get_session
from models import User, SessionTable
from schemas import (
    RegisterRequest, RegisterResponse, 
    LoginRequest, LoginResponse, 
    LogoutRequest, LogoutResponse,
    RefreshRequest, RefreshResponse
)
from hash_manager import HashManager
from jwt_manager import JWTManager

SECRET_KEY = "SUPER-DUPER-SECRET-KEY" # Move this to environment variables in production
jwt_manager = JWTManager(secret_key=SECRET_KEY)
security = HTTPBearer()

app = FastAPI(title="Session Management API", version="1.0.0")

@app.on_event("startup")
def on_startup():
    init_db()

# Dependency to check JWT in Header
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), session: Session = Depends(get_session)):
    token = credentials.credentials
    try:
        payload = jwt_manager.decode_token(token)
        
        # Check if token is revoked in DB and has correct type
        db_session = session.query(SessionTable).filter(
            SessionTable.token_jti == payload.get("jti"),
            SessionTable.token_type == "access",
            SessionTable.revoked_at == None
        ).first()
        
        if not db_session:
            raise HTTPException(status_code=401, detail="Token has been revoked or session ended")
            
        user = session.query(User).filter(User.id == payload.get("sub")).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
            
        return user
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

@app.post("/register", response_model=RegisterResponse)
def register(request: RegisterRequest, session: Session = Depends(get_session)):
    existing_user = session.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    hashed_pwd = HashManager.hash_password(request.password)
    user = User(email=request.email, password=hashed_pwd)
    session.add(user)
    session.commit()
    session.refresh(user)
    return RegisterResponse(
        id=user.id, 
        email=user.email, 
        message="User registered successfully"
    )

@app.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, session: Session = Depends(get_session)):
    user = session.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not HashManager.verify_password(request.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token, access_token_jti = jwt_manager.create_access_token(user.id)
    refresh_token, refresh_token_jti = jwt_manager.create_refresh_token(user.id)
    
    # Store access token session
    session.add(SessionTable(
        user_id=user.id,
        token_jti=access_token_jti,
        token_type="access",
        created_at=datetime.now(timezone.utc),
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=jwt_manager.access_token_expire_minutes),
        last_used=datetime.now(timezone.utc)
    ))
    
    # Store refresh token session
    session.add(SessionTable(
        user_id=user.id,
        token_jti=refresh_token_jti,
        token_type="refresh",
        created_at=datetime.now(timezone.utc),
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=jwt_manager.refresh_token_expire_minutes),
        last_used=datetime.now(timezone.utc)
    ))
    session.commit()
    
    return LoginResponse(
        id=user.id,
        email=user.email,
        access_token=access_token,
        refresh_token=refresh_token,
        message="Login successful"
    )

@app.post("/logout", response_model=LogoutResponse)
def logout(credentials: HTTPAuthorizationCredentials = Depends(security), session: Session = Depends(get_session)):
    token = credentials.credentials
    try:
        token_data = jwt_manager.decode_token(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    session.query(SessionTable).filter(SessionTable.token_jti == token_data["jti"]).update({
        "revoked_at": datetime.now(timezone.utc)
    })
    session.commit()
    
    return LogoutResponse(message="Logout successful")

@app.post("/refresh", response_model=RefreshResponse)
def refresh(request: RefreshRequest, session: Session = Depends(get_session)):
    try:
        token_data = jwt_manager.decode_token(request.refresh_token)
        
        if token_data.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
            
        db_session = session.query(SessionTable).filter(
            SessionTable.token_jti == token_data["jti"],
            SessionTable.revoked_at == None
        ).first()
        
        if not db_session:
            raise HTTPException(status_code=401, detail="Token has been revoked or is invalid")
            
        new_access_token, new_jti = jwt_manager.create_access_token(token_data["sub"])
        
        session.add(SessionTable(
            user_id=token_data["sub"],
            token_jti=new_jti,
            token_type="access",
            created_at=datetime.now(timezone.utc),
            expires_at=datetime.now(timezone.utc) + timedelta(minutes=jwt_manager.access_token_expire_minutes),
            last_used=datetime.now(timezone.utc)
        ))
        session.commit()
        
        return RefreshResponse(
            access_token=new_access_token,
            message="Token refreshed successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Refresh failed: {str(e)}")

# Örnek korumalı endpoint
@app.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {"id": current_user.id, "email": current_user.email}

if __name__ == "__main__":
    init_db()
    print("Database initialized and app ready.")
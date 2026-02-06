from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta

# Veritabanı, Modeller, Şemalar ve Yardımcı Sınıfların İçe Aktarılması
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

# GÜVENLİK NOTU: SECRET_KEY üretim ortamında (production) ortam değişkenlerinden (environment variables) alınmalıdır.
SECRET_KEY = "SUPER-DUPER-SECRET-KEY"
jwt_manager = JWTManager(secret_key=SECRET_KEY)
security = HTTPBearer()

# FastAPI uygulama nesnesinin oluşturulması
# ==============================================================================
# SİSTEM ÖZETİ (Yeni Başlayanlar İçin)
# ------------------------------------------------------------------------------
# 1. Kayıt: Şifreniz "mikserden" geçer, "ketçap" olur ve depoya (DB) o haliyle girer.
# 2. Giriş: Şifreniz kontrol edilir, size bir "bileklik" (Access) ve "anahtar" (Refresh) verilir.
# 3. Güvenlik: Bileklikler 5 dakikada eskir, anahtar kartla yenisini alırsınız.
# 4. Kara Liste: Çıkış yaparsanız bileklik numaranız defterde "geçersiz" işaretlenir.
# ==============================================================================

app = FastAPI(title="Oturum Yönetimi API", version="1.0.0")

@app.on_event("startup")
def on_startup():
    """Uygulama başladığında veritabanını ilklendirir."""
    init_db()

# Bağımlılık (Dependency): "KARA LİSTE KONTROLÜ" (Session Tracking)
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), session: Session = Depends(get_session)):
    """
    Özet: Kapıdaki görevli gibi çalışır. Bilekliğe bakar, mührü kontrol eder 
          ve "kara liste" defterinde bu bilekliğin iptal edilip edilmediğine bakar.
    """
    token = credentials.credentials
    try:
        # Token'ın geçerliliğini ve süresini kontrol et
        payload = jwt_manager.decode_token(token)
        
        # Token'ın veritabanında kayıtlı olduğunu, türünün 'access' olduğunu ve iptal edilmediğini (revoked) kontrol et
        db_session = session.query(SessionTable).filter(
            SessionTable.token_jti == payload.get("jti"),
            SessionTable.token_type == "access",
            SessionTable.revoked_at == None
        ).first()
        
        if not db_session:
            raise HTTPException(status_code=401, detail="Token iptal edilmiş veya oturum sonlandırılmış")
            
        # Kullanıcının varlığını kontrol et
        user = session.query(User).filter(User.id == payload.get("sub")).first()
        if not user:
            raise HTTPException(status_code=401, detail="Kullanıcı bulunamadı")
            
        return user
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=401, detail="Kimlik bilgileri doğrulanamadı")

@app.post("/register", response_model=RegisterResponse)
def register(request: RegisterRequest, session: Session = Depends(get_session)):
    """
    Yeni bir kullanıcı kaydı oluşturur.
    E-posta adresi sistemde kayıtlıysa hata döndürür.
    """
    existing_user = session.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="E-posta adresi zaten kullanımda")
    
    # Şifreyi güvenli bir şekilde hash'le
    hashed_pwd = HashManager.hash_password(request.password)
    user = User(email=request.email, password=hashed_pwd)
    
    session.add(user)
    session.commit()
    session.refresh(user)
    
    return RegisterResponse(
        id=user.id, 
        email=user.email, 
        message="Kullanıcı başarıyla kaydedildi"
    )

@app.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, session: Session = Depends(get_session)):
    """
    Kullanıcı girişi yapar.
    Başarılı girişte Access ve Refresh token çifti döndürür ve bunları veritabanına kaydeder.
    """
    user = session.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Geçersiz e-posta veya şifre")
    
    # Şifreyi doğrula
    if not HashManager.verify_password(request.password, user.password):
        raise HTTPException(status_code=401, detail="Geçersiz e-posta veya şifre")
    
    # Yeni token'lar oluştur
    access_token, access_token_jti = jwt_manager.create_access_token(user.id)
    refresh_token, refresh_token_jti = jwt_manager.create_refresh_token(user.id)
    
    # Access token bilgisini veritabanına kaydet
    session.add(SessionTable(
        user_id=user.id,
        token_jti=access_token_jti,
        token_type="access",
        created_at=datetime.now(timezone.utc),
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=jwt_manager.access_token_expire_minutes),
        last_used=datetime.now(timezone.utc)
    ))
    
    # Refresh token bilgisini veritabanına kaydet
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
        message="Giriş başarılı"
    )

@app.post("/logout", response_model=LogoutResponse)
def logout(credentials: HTTPAuthorizationCredentials = Depends(security), session: Session = Depends(get_session)):
    """
    Kullanıcıyı sistemden çıkarır.
    Mevcut token'ı veritabanında 'revoked' (iptal edildi) olarak işaretler.
    """
    token = credentials.credentials
    try:
        token_data = jwt_manager.decode_token(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Geçersiz token")
    
    # Token'ı iptal et (revoked_at alanını doldur)
    session.query(SessionTable).filter(SessionTable.token_jti == token_data["jti"]).update({
        "revoked_at": datetime.now(timezone.utc)
    })
    session.commit()
    
    return LogoutResponse(message="Çıkış başarılı")

@app.post("/refresh", response_model=RefreshResponse)
def refresh(request: RefreshRequest, session: Session = Depends(get_session)):
    """
    Süresi dolmuş bir erişim (access) token'ını yenilemek için kullanılır.
    Geçerli bir yenileme (refresh) token'ı gerektirir.
    """
    try:
        # Yenileme token'ını doğrula
        token_data = jwt_manager.decode_token(request.refresh_token)
        
        if token_data.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Geçersiz token türü")
            
        # Token'ın iptal edilip edilmediğini DB'den kontrol et
        db_session = session.query(SessionTable).filter(
            SessionTable.token_jti == token_data["jti"],
            SessionTable.revoked_at == None
        ).first()
        
        if not db_session:
            raise HTTPException(status_code=401, detail="Yenileme token'ı iptal edilmiş veya geçersiz")
            
        # Yeni bir erişim token'ı oluştur
        new_access_token, new_jti = jwt_manager.create_access_token(token_data["sub"])
        
        # Yeni access token'ı veritabanına kaydet
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
            message="Token başarıyla yenilendi"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Yenileme başarısız: {str(e)}")

# Korumalı bir endpoint örneği
@app.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    """Giriş yapmış olan kullanıcının bilgilerini döndürür."""
    return {"id": current_user.id, "email": current_user.email}

if __name__ == "__main__":
    # Uygulama doğrudan çalıştırılırsa veritabanını ilklendir
    init_db()
    print("Veritabanı hazırlandı ve uygulama çalışmaya hazır.")
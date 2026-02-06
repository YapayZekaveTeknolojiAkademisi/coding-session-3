import uuid
from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone, timedelta
from database import Base

# Varsayılan oturum süresi (dakika bazında)
MINUTES = 5

def generate_id():
    """Benzersiz bir UUID string oluşturur."""
    return str(uuid.uuid4())

class User(Base):
    """
    Kullanıcı bilgilerini saklayan tablo.
    """
    __tablename__ = "users"

    # Birincil anahtar, otomatik olarak UUID atanır.
    id = Column(String, primary_key=True, index=True, default=generate_id)
    # Tekil (unique) e-posta adresi.
    email = Column(String, unique=True, index=True)
    # Karma (hash) hale getirilmiş şifre.
    password = Column(String)

    # Kullanıcıya ait oturumların (SessionTable) listesi.
    sessions = relationship("SessionTable", back_populates="user")

class SessionTable(Base):
    """
    Kullanıcı oturumlarını (access ve refresh token bilgilerini) saklayan tablo.
    Bu tablo sayesinde token'ları iptal edebilir (revoke) veya oturumları yönetebiliriz.
    """
    __tablename__ = "sessions"
    
    id = Column(String, primary_key=True, index=True, default=generate_id)
    # Hangi kullanıcıya ait olduğu bilgisi.
    user_id = Column(String, ForeignKey("users.id"), index=True)

    # JWT içerisindeki benzersiz ID (JTI). Token iptali için kullanılır.
    token_jti = Column(String, unique=True, index=True, nullable=False)
    # Token türü: 'access' (erişim) veya 'refresh' (yenileme).
    token_type = Column(String, nullable=False) 
    
    # Oturumun oluşturulma tarihi.
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    # Oturumun sona erme tarihi.
    expires_at = Column(DateTime, default=lambda: datetime.now(timezone.utc) + timedelta(minutes=MINUTES))
    # Eğer oturum sonlandırıldıysa (logout), bu alan iptal tarihini tutar.
    revoked_at = Column(DateTime, nullable=True)
    # En son ne zaman işlem yapıldığı bilgisi.
    last_used = Column(DateTime, nullable=True)

    # Oturumun hangi kullanıcıya ait olduğunu belirten ilişki.
    user = relationship("User", back_populates="sessions")

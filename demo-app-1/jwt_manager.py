import jwt
import uuid
from datetime import datetime, timezone, timedelta
from fastapi import HTTPException

def generate_id():
    """Benzersiz bir JTI (JWT ID) oluşturur."""
    return str(uuid.uuid4())

def current_time():
    """Şu anki zamanı UTC bazında döndürür."""
    return datetime.now(timezone.utc)

class JWTManager:
    """
    ALGORİTMA: "Konser Bilekliği" (JWT)
    ----------------------------------
    Özet: Giriş yaptıktan sonra size verilen dijital bir bilekliktir. 
          Üzerinde kim olduğunuz ve süreniz yazar, ayrıca sunucunun gizli mührü vardır.
    
    YÖNTEM: "Kısa Süreli Pass ve Yenileme Kartı" (Access & Refresh)
    --------------------------------------------------------------
    - Access Token (Bileklik): 5-10 dk geçerlidir. Kapılardan geçmek için kullanılır.
    - Refresh Token (Anahtar): 1-2 gün geçerlidir. Bileklik eskiyince yenisini almak için kullanılır.
    """
    def __init__(self, secret_key: str, algorithm: str = "HS256", 
                 access_token_expire_minutes: int = 1, 
                 refresh_token_expire_minutes: int = 2):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes
        self.refresh_token_expire_minutes = refresh_token_expire_minutes

    def create_access_token(self, user_id: str):
        """
        Kısa süreli bir erişim (access) token'ı oluşturur.
        
        Args:
            user_id (str): Kullanıcının benzersiz ID'si (sub claim).
            
        Returns:
            tuple: (encoded_jwt, jti)
        """
        jti = generate_id()
        to_encode = {
            "sub": str(user_id),
            "jti": str(jti),
            "type": "access",
            "iat": current_time(),
            "exp": current_time() + timedelta(minutes=self.access_token_expire_minutes)
        }
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt, jti

    def create_refresh_token(self, user_id: str):
        """
        Daha uzun süreli bir yenileme (refresh) token'ı oluşturur.
        Yenileme token'ı, süresi dolan erişim token'ını yenilemek için kullanılır.
        
        Args:
            user_id (str): Kullanıcının benzersiz ID'si (sub claim).
            
        Returns:
            tuple: (encoded_jwt, jti)
        """
        jti = generate_id()
        to_encode = {
            "sub": str(user_id),
            "jti": str(jti),
            "type": "refresh",
            "iat": current_time(),
            "exp": current_time() + timedelta(minutes=self.refresh_token_expire_minutes)
        }
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt, jti

    def decode_token(self, token: str):
        """
        Token'ın içeriğini çözer ve doğruluğunu kontrol eder.
        
        Args:
            token (str): Çözülecek olan JWT string'i.
            
        Returns:
            dict: Token içerisindeki veri (payload).
            
        Raises:
            HTTPException: Token süresi dolmuşsa (401) veya geçersizse (401).
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token süresi dolmuş")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Geçersiz token")
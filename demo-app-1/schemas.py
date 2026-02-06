from pydantic import BaseModel

class RegisterRequest(BaseModel):
    """Kayıt olma isteği için gereken veriler."""
    email: str
    password: str

class RegisterResponse(BaseModel):
    """Kayıt işlemi başarılı olduğunda dönülen veriler."""
    id: str
    email: str
    message: str

class LoginRequest(BaseModel):
    """Giriş yapma isteği için gereken veriler."""
    email: str
    password: str

class LoginResponse(BaseModel):
    """Giriş işlemi başarılı olduğunda dönülen veriler ve token'lar."""
    id: str
    email: str
    access_token: str
    refresh_token: str
    message: str

class LogoutRequest(BaseModel):
    """Çıkış yapmak için gönderilen token bilgisi."""
    token: str

class LogoutResponse(BaseModel):
    """Çıkış işlemi sonucu dönülen mesaj."""
    message: str

class RefreshRequest(BaseModel):
    """Yeni bir erişim token'ı almak için kullanılan yenileme token'ı."""
    refresh_token: str

class RefreshResponse(BaseModel):
    """Yenilenmiş erişim token'ı."""
    access_token: str
    message: str

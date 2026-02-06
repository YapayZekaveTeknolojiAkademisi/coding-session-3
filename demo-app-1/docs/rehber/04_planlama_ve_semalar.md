# 📋 04 - Planlama ve Şemalar

FastAPI'da veriler "Şemalar" üzerinden akar. Bu, hem güvenlik hem de otomatik dokümantasyon sağlar.

## 1. Neden Şema Kullanıyoruz?
Eğer bir kullanıcı kayıt olurken `email` yerine `yaş` gönderirse, Pydantic şeması bunu (`schemas.py`) anında engeller ve bize temiz veri sunar.

## 2. Gerekli Şemalar:
- **`RegisterRequest` / `LoginRequest`**: `email` ve `password`.
- **`RegisterResponse`**: ID, Email ve mesaj.
- **`LoginResponse`**: Kullanıcı bilgileri + `access_token` + `refresh_token`.
- **`RefreshRequest`**: Sadece `refresh_token`.
- **`LogoutResponse` / `RefreshResponse`**: İşlem sonucu dönen mesajlar.

## 💡 İpucu:
Tüm şemalar Pydantic'in `BaseModel` sınıfından miras almalıdır.

## 🛠 Görev:
1. `schemas.py` dosyasında yukarıdaki tüm sınıfları oluştur.
2. `LoginResponse` içine `token_type: str = "bearer"` ekleyerek standartlara uyum sağla.

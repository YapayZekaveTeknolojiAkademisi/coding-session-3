# 🚀 06 - Çalıştırma ve Postman Testi

Sistemin tam döngüsünü test etme vakti.

## 1. Uygulamayı Başlatma
Uygulamayı iki şekilde çalıştırabilirsiniz:
- `uvicorn app:app --reload`
- `python app.py` (Dosya sonunda `main` bloğu olduğu için)

## 2. Postman Test Senaryosu (Tam Döngü)

### 1. Kayıt (`/register`)
- **JSON**: `{"email": "ali@veli.com", "password": "123"}` -> Başarılı mesajı alınmalı.

### 2. Giriş (`/login`)
- Bilgileri gönderin. Yanıt olarak gelen `access_token` ve `refresh_token`'ı bir yere not edin.

### 3. Profil Görüntüleme (`/me`)
- **Auth** -> **Bearer Token** kısmına `access_token`'ı yapıştırın. Bilgileriniz gelmeli.

### 4. Token Yenileme (`/refresh`)
- 1 dakika bekleyin (Access token süresi dolana kadar). `/me` isteği atınca "Token expired" hatası almalısınız.
- `/refresh` endpoint'ine not ettiğiniz `refresh_token`'ı gönderin. Yeni bir `access_token` alacaksınız!

### 5. Çıkış Yapma (`/logout`)
- Elinizdeki son `access_token` ile logout olun.
- Artık o token ile `/me` sayfasına girmeye çalışırsanız "Token revoked" hatası almalısınız.

## 🏁 Sonuç
Tebrikler! Hem token süresi dolunca yenileyen, hem de logout olunca token'ı anında geçersiz kılan **profesyonel seviyede** bir auth sistemini tamamladınız.

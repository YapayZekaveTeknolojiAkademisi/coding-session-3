# 📡 API Dokümantasyonu

Uygulamanın sunduğu tüm servislerin detayları, örnek istek/yanıtlar ve test araçları aşağıdadır.

**Base URL (yerel):** `http://127.0.0.1:8000`  
**Otomatik dokümantasyon:** [Swagger UI](http://127.0.0.1:8000/docs) · [ReDoc](http://127.0.0.1:8000/redoc)

---

## 1. Kullanıcı Kaydı — `POST /register`

- **Amaç:** Yeni hesap oluşturur. Şifre Bcrypt ile hash’lenerek veritabanına yazılır.
- **Kimlik doğrulama:** Gerekmez.

**İstek gövdesi (JSON):**

```json
{
  "email": "kullanici@ornek.com",
  "password": "gizli_sifre_123"
}
```

**Başarılı yanıt (200):**

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "kullanici@ornek.com",
  "message": "Kullanıcı başarıyla kaydedildi"
}
```

**Hata (400):** E-posta zaten kullanımda — `"E-posta adresi zaten kullanımda"`

---

## 2. Giriş — `POST /login`

- **Amaç:** Kimlik doğrulaması yapar; Access ve Refresh token çifti döndürür ve oturumları veritabanına kaydeder.
- **Kimlik doğrulama:** Gerekmez.

**İstek gövdesi (JSON):**

```json
{
  "email": "kullanici@ornek.com",
  "password": "gizli_sifre_123"
}
```

**Başarılı yanıt (200):**

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "kullanici@ornek.com",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "message": "Giriş başarılı"
}
```

**Hata (401):** Geçersiz e-posta veya şifre — `"Geçersiz e-posta veya şifre"`

---

## 3. Token Yenileme — `POST /refresh`

- **Amaç:** Süresi dolan Access token yerine yeni Access token almak.
- **Kimlik doğrulama:** Gerekmez; gövdede `refresh_token` gönderilir.

**İstek gövdesi (JSON):**

```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Başarılı yanıt (200):**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "message": "Token başarıyla yenilendi"
}
```

**Hata (401):** Geçersiz veya iptal edilmiş refresh token.

---

## 4. Çıkış — `POST /logout`

- **Amaç:** Mevcut oturumu sonlandırır; kullanılan token veritabanında `revoked` olarak işaretlenir.
- **Kimlik doğrulama:** Gerekli — **Bearer Token** (Access token).

**Header:**

```
Authorization: Bearer <access_token>
```

**İstek gövdesi:** Boş veya yok.

**Başarılı yanıt (200):**

```json
{
  "message": "Çıkış başarılı"
}
```

**Hata (401):** Geçersiz veya eksik token.

---

## 5. Profil Bilgileri — `GET /me` *(Korumalı)*

- **Amaç:** Giriş yapmış kullanıcının bilgilerini döndürür.
- **Kimlik doğrulama:** Gerekli — **Bearer Token** (Access token).

**Header:**

```
Authorization: Bearer <access_token>
```

**Başarılı yanıt (200):**

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "kullanici@ornek.com"
}
```

**Hata (401):** Token yok, geçersiz, süresi dolmuş veya iptal edilmiş — `"Kimlik bilgileri doğrulanamadı"` / `"Token iptal edilmiş veya oturum sonlandırılmış"`

---

## 🧪 Bruno ile Test

Proje kökündeki `bruno/` klasöründe hazır istekler bulunur:

- **Register** — Kayıt
- **Login** — Giriş (email/şifre ile)
- **Me** — Profil (Bearer token gerekir)
- **Refresh** — Token yenileme
- **Logout** — Çıkış (Bearer token gerekir)

1. [Bruno](https://www.usebruno.com/) uygulamasını açın.
2. `bruno` klasörünü koleksiyon olarak ekleyin.
3. Uygulamayı `http://localhost:8000` adresinde çalıştırın.
4. Önce **Login** ile giriş yapıp dönen `access_token` ve `refresh_token` değerlerini kopyalayın.
5. **Me** ve **Logout** için Authorization’da `Bearer <access_token>` kullanın; **Refresh** için body’de `refresh_token` gönderin.

---

## Özet Tablo

| Endpoint        | Yöntem | Auth     | Açıklama                    |
|----------------|--------|----------|-----------------------------|
| `/register`    | POST   | Hayır    | Yeni kullanıcı kaydı        |
| `/login`       | POST   | Hayır    | Giriş, token çifti          |
| `/refresh`     | POST   | Hayır*   | Yeni access token           |
| `/logout`      | POST   | Bearer   | Oturum sonlandırma          |
| `/me`          | GET    | Bearer   | Giriş yapmış kullanıcı bilgisi |

\* Refresh için body’de `refresh_token` gönderilir.

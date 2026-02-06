# 🔐 Kimlik Doğrulama ve Oturum Yönetimi Projesi

FastAPI ile geliştirilmiş, **JWT** (Access + Refresh token) ve veritabanı tabanlı **oturum iptali (revocation)** destekleyen örnek bir auth uygulaması.

---

## 📁 Proje Yapısı

| Klasör / Dosya | Açıklama |
|----------------|----------|
| **demo-app-1/** | Ana uygulama: kayıt, giriş, çıkış, token yenileme, korumalı `/me` |
| **demo-app-1/docs/** | Auth sistemini kodla adım adım inşa etme rehberi (6 bölüm) |
| **docs/** | Genel dokümantasyon: kurulum, API, mimari, güvenlik, adım adım rehber |
| **bruno/** | Bruno ile API testi için hazır istek koleksiyonu |
| **notebooks/** | JWT ve token konulu eğitim not defteri |

---

## 🚀 Hızlı Başlangıç

```bash
# Bağımlılıklar
pip install fastapi uvicorn sqlalchemy bcrypt pyjwt

# Uygulamayı çalıştır
cd demo-app-1 && uvicorn app:app --reload
```

Tarayıcıda: **http://127.0.0.1:8000/docs** (Swagger) · **http://127.0.0.1:8000/redoc** (ReDoc).

---

## 📖 Hangi Rehberi Okumalıyım?

| Durumunuz | Önerilen rehber |
|-----------|------------------|
| Hiç bilmiyorum, sıfırdan çalıştırıp test etmek istiyorum | [**Adım Adım Başlangıç Rehberi**](docs/adim_adim_baslangic_rehberi.md) — 10 adım + her adımda **arkadaki mantık ve algoritma** |
| Hızlı kurulum ve kısa özet yeterli | [**Başlangıç Rehberi**](docs/baslangic_rehberi.md) |
| Auth sistemini kod tarafında adım adım kurmak istiyorum | [**Öğrenim Rehberi**](demo-app-1/docs/README.md) (6 bölüm: veritabanı → hash → JWT → şemalar → route’lar → test) |
| Tüm dokümanların listesini görmek istiyorum | [**Dokümantasyon İndeksi**](docs/README.md) |

---

## 📚 Dokümantasyon Özeti

| Doküman | Açıklama |
|---------|----------|
| [Dokümantasyon İndeksi](docs/README.md) | Tüm dökümanların haritası |
| [Adım Adım Başlangıç Rehberi](docs/adim_adim_baslangic_rehberi.md) | Hiç bilmeyenler için 10 adım + mantık/algoritma |
| [Başlangıç Rehberi](docs/baslangic_rehberi.md) | Kurulum ve ilk test (kısa) |
| [API Dokümantasyonu](docs/api_dokumantasyonu.md) | Endpoint’ler, örnek istek/yanıt, Bruno |
| [Mimari Yapı](docs/mimari_yapi.md) | Klasör yapısı ve veri akışı |
| [Güvenlik Rehberi](docs/guvenlik_rehberi.md) | Şifre, JWT, token süreleri, iptal |
| [Öğrenim Rehberi](demo-app-1/docs/README.md) | Auth’u kodla inşa etme (6 bölüm) |

---

## 🛠 Kullanılan Teknolojiler

- **FastAPI** — Web API  
- **SQLAlchemy** — ORM (SQLite)  
- **Bcrypt** — Şifre hash  
- **PyJWT** — JWT üretimi ve doğrulama  
- **Pydantic** — Veri doğrulama ve şemalar  

---

*İyi çalışmalar.*

# 🚀 Başlangıç Rehberi

Bu proje, **FastAPI** kullanarak geliştirilmiş, güvenli bir kullanıcı **kayıt** ve **oturum yönetimi (Auth)** sistemidir. JWT (Access + Refresh token) ve veritabanında oturum takibi (revocation) ile çalışır.

---

## 🛠 Gereksinimler

- **Python 3.9+**
- **pip** (Python paket yöneticisi)

---

## 📦 Kurulum

1. **Proje köküne gidin** (veya `demo-app-1` klasörüne, bağımlılıklar orada ise):

   ```bash
   cd /path/to/codding-session-4
   ```

2. **Bağımlılıkları yükleyin:**

   ```bash
   pip install fastapi uvicorn sqlalchemy bcrypt pyjwt
   ```

   Veya projede `requiremetns.txt` varsa:

   ```bash
   pip install -r requiremetns.txt
   ```

3. **Uygulamayı çalıştırın** — API, `demo-app-1` içindeki `app.py` ile sunulur:

   ```bash
   cd demo-app-1
   uvicorn app:app --reload
   ```

   En pratik yol: önce `cd demo-app-1` ile klasöre girip ardından `uvicorn app:app --reload` çalıştırmaktır.

---

## 🌐 API’ye Erişim

| Adres | Açıklama |
|-------|----------|
| **Uygulama** | http://127.0.0.1:8000 |
| **Swagger UI** | http://127.0.0.1:8000/docs |
| **ReDoc** | http://127.0.0.1:8000/redoc |

---

## 🧪 İlk Test (Swagger)

1. Tarayıcıda **http://127.0.0.1:8000/docs** adresini açın.
2. **POST /register** ile bir kullanıcı oluşturun (örn. `email`, `password`).
3. **POST /login** ile giriş yapın; yanıttaki `access_token` değerini kopyalayın.
4. Sayfanın üst kısmındaki **Authorize** butonuna tıklayın; **Bearer** alanına sadece token’ı yapıştırın (Bearer kelimesi zaten eklenir).
5. **GET /me** ile giriş yapmış kullanıcı bilgilerinizi görün.

---

## 🧪 Bruno ile Test

Projede `bruno/` klasöründe hazır istekler vardır:

1. [Bruno](https://www.usebruno.com/) uygulamasını kurun ve açın.
2. **bruno** klasörünü koleksiyon olarak ekleyin.
3. API’yi yukarıdaki gibi çalıştırın (`http://localhost:8000`).
4. **Login** isteğini çalıştırıp dönen `access_token` ve `refresh_token` değerlerini not alın.
5. **Me** ve **Logout** için ilgili isteklerde Authorization’a `Bearer <access_token>` ekleyin.
6. **Refresh** isteğinde body’de `refresh_token` kullanın.

Detaylı endpoint açıklamaları ve örnek yanıtlar için [API Dokümantasyonu](./api_dokumantasyonu.md) sayfasına bakın.

---

## 📚 Sonraki Adımlar

- [Mimari Yapı](./mimari_yapi.md) — Dosya düzeni ve veri akışı  
- [API Dokümantasyonu](./api_dokumantasyonu.md) — Tüm endpoint’ler ve örnekler  
- [Güvenlik Rehberi](./guvenlik_rehberi.md) — Şifre, JWT ve token iptali  
- [demo-app-1 Öğrenim Rehberi](../demo-app-1/docs/README.md) — Adım adım auth sistemi inşası

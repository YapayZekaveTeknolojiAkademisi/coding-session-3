# 📗 Adım Adım Başlangıç Rehberi — Hiç Bilmeyenler İçin

Bu rehber, **daha önce API veya bu projeyi hiç çalıştırmamış** biri için yazılmıştır. Her adımda hem **ne yapacağınız** hem de **arkada neyin, nasıl çalıştığı** (mantık ve algoritma) anlatılır.

---

## 🧩 Bu projede ne var? (Kısaca)

- **API:** Uygulamanın dışarıya sunduğu “hizmetler” (kayıt ol, giriş yap, çıkış yap gibi). Tarayıcı veya Postman/Bruno ile bu hizmetlere istek atarız.
- **Token:** Giriş yaptıktan sonra size verilen bir “giriş kartı” gibidir. Bunu isteklerde göndererek “ben giriş yapmış kullanıcıyım” dersiniz.
- **Bu proje:** Kayıt, giriş, token ile korunan sayfa ve çıkış gibi işlemleri yapan küçük bir **kimlik doğrulama** örneğidir.

---

## 🏗 Sistemin genel mantığı (Büyük resim)

Uygulama çalıştığında arka planda şunlar vardır:

1. **Veritabanı (SQLite)**  
   - **`users`** tablosu: Her kullanıcı için bir satır (id, email, **hash’lenmiş şifre**). Şifre düz metin **asla** yazılmaz.  
   - **`sessions`** tablosu: Her açılan oturum için bir satır (hangi kullanıcı, token’ın benzersiz numarası **jti**, türü: access/refresh, süre, **iptal tarihi**). Çıkış yapınca ilgili token’ın satırına iptal zamanı yazılır (“kara liste”).

2. **Şifre güvenliği (Bcrypt)**  
   Kayıtta şifre “mikserden geçirilir” — geri dönüşü olmayan bir **hash** üretilir. Veritabanı çalınsa bile kimse düz şifreyi göremez. Girişte girilen şifre aynı algoritmayla karşılaştırılır; eşleşirse kabul.

3. **Token’lar (JWT)**  
   Girişte iki token üretilir:  
   - **Access token:** Kısa ömürlü (ör. 1 dakika). Her korumalı istekte “Authorization: Bearer &lt;token&gt;” ile gönderilir.  
   - **Refresh token:** Daha uzun ömürlü. Access süresi dolunca yeni access almak için kullanılır.  
   Token’ın içinde kullanıcı id’si (**sub**), token’ın benzersiz numarası (**jti**) ve süre (**exp**) vardır. Sunucu gizli bir anahtar (**SECRET_KEY**) ile imzalar; biri token’ı değiştirirse imza bozulur ve kabul edilmez.

4. **Korumalı sayfalar**  
   `/me` ve `/logout` gibi uç noktalar, istekte **Bearer token** ister. Sunucu:  
   - Token’ı çözer (süre ve imza kontrolü),  
   - **jti**’yi veritabanındaki `sessions` tablosunda arar,  
   - Bu token’ın **revoked** (iptal) olup olmadığına bakar.  
   İptal edilmişse veya süresi dolmuşsa 401 döner.

5. **Çıkış (logout)**  
   Gönderilen token’ın **jti**’si bulunur, ilgili oturum satırına **revoked_at** alanına “şu an” yazılır. O andan sonra o token ile artık hiçbir korumalı işlem yapılamaz.

Bu bütünlük, rehberdeki her adımda “Arkadaki mantık” bölümünde tek tek açılacak.

---

# BÖLÜM A — Ortam ve çalıştırma

---

## Adım 1 — Bilgisayarınızda Python var mı?

### Ne yapacaksınız

1. **Terminal** (veya **Komut İstemi**) açın:
   - **Mac/Linux:** “Terminal” yazıp Enter.
   - **Windows:** “cmd” veya “PowerShell” yazıp Enter.
2. Şu komutu yazıp **Enter**’a basın:

   ```bash
   python --version
   ```

   veya:

   ```bash
   python3 --version
   ```

3. **Beklenen:** Ekranda `Python 3.9` veya daha yüksek bir sürüm numarası görünmeli (örn. `Python 3.11.5`).
4. **Hata alırsanız:** [python.org](https://www.python.org/downloads/) adresinden Python’u indirip kurun. Kurulumda **“Add Python to PATH”** seçeneğini işaretleyin.

### Arkadaki mantık

- Uygulama **Python** ile yazıldığı için çalıştırabilmek için sisteminizde Python yüklü olmalı.
- `python` veya `python3` komutu, kurulu sürümü gösterir. FastAPI ve kullandığımız kütüphaneler Python 3.9+ ile uyumludur.

---

## Adım 2 — Proje klasörüne girin

### Ne yapacaksınız

1. Terminal/Komut İstemi açık kalsın.
2. Projenin bulunduğu klasöre gidin. Örnek (kendi bilgisayarınızdaki yolu yazın):

   ```bash
   cd /Users/enesa/Documents/ForAkademi/codding-session-4
   ```

   **Windows’ta** örnek:

   ```bash
   cd C:\Users\KullaniciAdi\Documents\ForAkademi\codding-session-4
   ```

3. Doğru yerde olduğunuzu kontrol etmek için:

   ```bash
   dir
   ```

   (Mac/Linux’ta `ls` yazabilirsiniz.)  
   `demo-app-1`, `docs`, `bruno` gibi klasörleri görüyorsanız doğru yerdesiniz.

### Arkadaki mantık

- Komutlar “şu an hangi klasördeyim?” bilgisine göre çalışır. `cd` ile proje köküne geçiyoruz; böylece bir sonraki adımda `demo-app-1` içine girip uygulamayı oradan başlatacağız.
- Proje yapısı: `demo-app-1` = ana uygulama (app.py, veritabanı, modeller), `docs` = dokümantasyon, `bruno` = hazır API istekleri.

---

## Adım 3 — Gerekli paketleri yükleyin

### Ne yapacaksınız

Aynı terminalde şu komutu çalıştırın:

```bash
pip install fastapi uvicorn sqlalchemy bcrypt pyjwt
```

(Bazı bilgisayarlarda `pip3` yazmanız gerekebilir.)

- İşlem 1–2 dakika sürebilir.
- Sonunda hata mesajı yoksa kurulum tamamdır.

### Arkadaki mantık ve algoritma

- **FastAPI:** Web API’yi tanımladığımız framework (route’lar, şemalar, dependency’ler).
- **Uvicorn:** Sunucu programı; bilgisayarınızda bir “port” (ör. 8000) açıp gelen HTTP isteklerini FastAPI uygulamasına iletir.
- **SQLAlchemy:** Veritabanı ile konuşmak için ORM. Tabloları Python sınıfları gibi kullanırız; gerçekte SQLite dosyasına (`test.db`) yazar/okur.
- **Bcrypt:** Şifre **hash** algoritması. Şifreyi tek yönlü bir fonksiyondan geçirir; aynı şifre + aynı “tuz” (salt) ile hep aynı sonuç çıkar, ama sonuçtan şifreyi geri hesaplamak pratikte imkânsızdır. Böylece veritabanında sadece hash tutulur.
- **PyJWT:** JWT (JSON Web Token) üretmek ve doğrulamak için. Token’ın içine `sub`, `jti`, `exp`, `type` gibi alanlar konur; sunucu gizli anahtar ile imzalar. Doğrulama sırasında imza ve süre kontrol edilir.

Bu paketler olmadan uygulama import aşamasında hata verir.

---

## Adım 4 — Uygulamayı çalıştırın

### Ne yapacaksınız

1. Uygulama klasörüne girin:

   ```bash
   cd demo-app-1
   ```

2. Sunucuyu başlatın:

   ```bash
   uvicorn app:app --reload
   ```

3. **Beklenen:** Ekranda buna benzer satırlar görünür:

   ```
   INFO:     Uvicorn running on http://127.0.0.1:8000
   INFO:     Application startup complete.
   ```

4. Bu pencereyi **kapatmayın**. Durdurmak için **Ctrl + C** yapabilirsiniz.

### Arkadaki mantık ve algoritma

- **`uvicorn app:app`:** `app` = `demo-app-1` içindeki `app.py` dosyası, ikinci `app` = o dosyadaki `app = FastAPI(...)` nesnesi. Uvicorn bu nesneyi yükleyip HTTP isteklerini ona yönlendirir.
- **`--reload`:** Kod dosyalarında değişiklik yapıldığında sunucuyu otomatik yeniden başlatır (geliştirme için).
- **Startup:** FastAPI’de `@app.on_event("startup")` ile tanımlı fonksiyon çalışır; bu projede `init_db()` çağrılır. `init_db()` SQLAlchemy ile `users` ve `sessions` tablolarını oluşturur (yoksa). Veritabanı dosyası `demo-app-1/test.db` olarak oluşur.
- **Port 8000:** Tarayıcıda `http://127.0.0.1:8000` yazdığınızda istekler bu sunucuya gider.

---

## Adım 5 — Tarayıcıda dokümantasyonu açın

### Ne yapacaksınız

1. Tarayıcıyı açın.
2. Adres çubuğuna yazın:

   ```
   http://127.0.0.1:8000/docs
   ```

3. **Beklenen:** “Oturum Yönetimi API” başlıklı bir sayfa; altında **POST /register**, **POST /login**, **GET /me** vb. satırlar (Swagger UI).

### Arkadaki mantık

- FastAPI, tanımladığınız route’lardan ve Pydantic şemalarından otomatik bir **OpenAPI** dokümantasyonu üretir. `/docs` adresi bu dokümantasyonun etkileşimli arayüzünü (Swagger UI) sunar. Buradan istek atınca gerçekte sunucuya HTTP isteği gider; yani API’yi doğrudan test etmiş olursunuz.

---

# BÖLÜM B — Kayıt, giriş ve token akışı

---

## Adım 6 — Kayıt olun (Register)

### Ne yapacaksınız

1. Swagger’da **POST /register** satırını bulun.
2. **“Try it out”** butonuna tıklayın.
3. **Request body** kutusunda örnek:

   ```json
   {
     "email": "test@ornek.com",
     "password": "123456"
   }
   ```

4. **“Execute”** tıklayın.
5. **Response body**’de **Code 200** ve `"message": "Kullanıcı başarıyla kaydedildi"` görmelisiniz.

### Arkadaki mantık ve algoritma

- **İstek:** İstemci `POST /register` ile JSON gövde gönderir. FastAPI bunu **Pydantic** ile `RegisterRequest` şemasına göre doğrular (email ve password alanları zorunludur).
- **E-posta kontrolü:** Sunucu veritabanında `User.email == request.email` sorgusu yapar. Kayıt varsa **400** döner: “E-posta adresi zaten kullanımda”.
- **Şifre hash’leme (algoritma):**  
  Şifre **asla** düz metin saklanmaz. `HashManager.hash_password(request.password)` çağrılır:
  - Bcrypt **rastgele bir tuz (salt)** üretir (`gensalt()`).
  - Şifre UTF-8 byte’a çevrilir, tuz ile birlikte bcrypt hash fonksiyonundan geçirilir.
  - Çıkan hash string olarak alınır (`.decode('utf-8')`) ve veritabanına yazılacak tek değer budur.  
  Aynı şifreyi iki kez kaydetsek bile tuz farklı olduğu için hash’ler farklı olur; bu da güvenlik için istenen davranıştır.
- **Veritabanına yazma:** `User` nesnesi oluşturulur: `id` otomatik UUID, `email` = istekten gelen, `password` = hash. `session.add(user)` ve `session.commit()` ile `users` tablosuna bir satır eklenir.
- **Yanıt:** `RegisterResponse` ile `id`, `email` ve mesaj döndürülür. Şifre veya hash yanıtta **yer almaz**.

---

## Adım 7 — Giriş yapın (Login)

### Ne yapacaksınız

1. **POST /login** satırını bulun.
2. **“Try it out”** deyin.
3. **Request body**’de kayıtta kullandığınız e-posta ve şifreyi yazın:

   ```json
   {
     "email": "test@ornek.com",
     "password": "123456"
   }
   ```

4. **“Execute”** tıklayın.
5. **Response body**’de **`access_token`** ve **`refresh_token`** değerlerini görün. **`access_token`** değerini (tamamını) kopyalayıp bir yere not edin.

### Arkadaki mantık ve algoritma

- **Kullanıcı bulma:** `User` tablosunda `email` ile sorgu yapılır. Bulunamazsa **401** “Geçersiz e-posta veya şifre”.
- **Şifre doğrulama (algoritma):**  
  `HashManager.verify_password(request.password, user.password)` çağrılır:
  - Girilen şifre ve veritabanındaki hash byte’a çevrilir.
  - Bcrypt’in `checkpw` fonksiyonu, aynı tuz ve maliyet parametreleriyle girilen şifrenin hash’inin veritabanındaki hash ile eşleşip eşleşmediğini kontrol eder. Eşleşmezse **401** döner.
- **Token üretimi (JWT algoritması):**  
  Şifre doğruysa iki token üretilir:
  - **Access token:** `JWTManager.create_access_token(user.id)`:
    - Benzersiz bir **jti** (UUID) üretilir.
    - Payload: `sub` = kullanıcı id’si, `jti`, `type` = `"access"`, `iat` (verilme zamanı), `exp` (bitiş zamanı, örn. 1 dakika sonra).
    - Bu sözlük `SECRET_KEY` ve algoritma (HS256) ile imzalanıp base64’e çevrilir; ortaya `eyJ...` ile başlayan JWT string’i çıkar.
  - **Refresh token:** Aynı mantık, `type` = `"refresh"`, süre daha uzun (örn. 2 dakika).
- **Veritabanına oturum kaydı:**  
  Her iki token için de `sessions` tablosuna bir satır eklenir:
  - `user_id`, `token_jti`, `token_type` (access/refresh), `created_at`, `expires_at`, `revoked_at` = NULL, `last_used`.  
  Böylece ileride “bu token iptal mi?” sorusu veritabanından cevaplanabilir (kara liste).
- **Yanıt:** `LoginResponse` ile `id`, `email`, `access_token`, `refresh_token` ve mesaj döner. İstemci access token’ı saklayıp korumalı isteklerde kullanacak; gerekirse refresh token ile yeni access alacak.

---

## Adım 8 — “Giriş yapmışım” diye nasıl söylerim? (Authorize)

### Ne yapacaksınız

1. Swagger sayfasının **en üstünde** **“Authorize”** (veya kilit ikonu) butonuna tıklayın.
2. Açılan pencerede **Value** kutusuna **sadece** kopyaladığınız token’ı yapıştırın (`Bearer` yazmayın).
3. **“Authorize”** deyip pencereyi kapatın.

Bundan sonra Swagger’dan yapılan isteklerde bu token otomatik gönderilir.

### Arkadaki mantık ve algoritma

- HTTP’de “kimlik kanıtı” genelde **Authorization** başlığında taşınır: `Authorization: Bearer <token>`. “Bearer” = “taşıyıcı”; yani “bu token’ı taşıyorum, ben bu kullanıcıyım” anlamındadır.
- Swagger UI, Authorize’a yazdığınız değeri alıp her istekte `Authorization: Bearer <sizin_token>` olarak ekler. Böylece `/me` ve `/logout` gibi korumalı endpoint’lere istek atıldığında sunucu token’ı görür.
- Sunucu tarafında `HTTPBearer()` dependency’si bu başlığı okur ve token string’ini endpoint’e iletir; `get_current_user` veya doğrudan token kullanan route’lar buna göre davranır.

---

## Adım 9 — Profil bilginizi görün (/me)

### Ne yapacaksınız

1. **GET /me** satırını bulun.
2. **“Try it out”** → **“Execute”** tıklayın.
3. **Beklenen:** Response body’de kendi **id** ve **email** bilginiz görünür.

### Arkadaki mantık ve algoritma

- **Korumalı route:** `/me` endpoint’i `get_current_user` bağımlılığını kullanır. Yani istek geldiğinde önce `get_current_user` çalışır; o başarılı olursa döndürdüğü `User` nesnesi endpoint’e “current_user” olarak verilir.
- **get_current_user algoritması (kara liste dahil):**
  1. **Token alınır:** `HTTPBearer()` ile `Authorization` başlığındaki Bearer token okunur.
  2. **Token çözülür:** `jwt_manager.decode_token(token)`:
     - PyJWT ile token imzası `SECRET_KEY` ve HS256 kullanılarak doğrulanır. Biri token’ı değiştirdiyse imza tutmaz → **401**.
     - `exp` (expiration) kontrol edilir; süre geçmişse **401** “Token süresi dolmuş”.
     - Geçerliyse payload (içindeki `sub`, `jti`, `type` vb.) döner.
  3. **Kara liste kontrolü:** Veritabanında `SessionTable` sorgulanır: `token_jti == payload["jti"]`, `token_type == "access"`, `revoked_at == None`. Böyle bir satır yoksa token ya iptal edilmiş ya da hiç kaydedilmemiş demektir → **401** “Token iptal edilmiş veya oturum sonlandırılmış”.
  4. **Kullanıcı kontrolü:** `User` tablosunda `id == payload["sub"]` ile kullanıcı aranır. Yoksa **401**.
  5. **Başarı:** `User` nesnesi döndürülür; endpoint bunu kullanarak `{"id": ..., "email": ...}` yanıtını üretir.

Bu sayede sadece geçerli, süresi dolmamış ve iptal edilmemiş bir access token ile `/me` çalışır.

---

## Adım 10 — Çıkış yapın (Logout)

### Ne yapacaksınız

1. **POST /logout** satırını bulun.
2. **“Try it out”** → **“Execute”** tıklayın.
3. **Beklenen:** `"message": "Çıkış başarılı"`.
4. Sonrasında **GET /me** ile tekrar istek atın → **401 Unauthorized** almalısınız.

### Arkadaki mantık ve algoritma

- **İstek:** `Authorization: Bearer <token>` ile gelir. Sunucu bu token’ı alır.
- **Token çözülür:** `jwt_manager.decode_token(token)` ile payload (içinde `jti`) alınır. Geçersiz veya süresi dolmuşsa **401**.
- **İptal (revocation) algoritması:** Veritabanında `SessionTable` içinde `token_jti == payload["jti"]` olan oturum satırı bulunur ve `revoked_at = datetime.now(timezone.utc)` ile güncellenir. Logout isteğinde gönderilen token (genelde access token) olduğu için sadece o token’ın kaydı iptal edilir; o token’a ait tek bir satır vardır çünkü her token’ın jti’si benzersizdir.
- **Sonuç:** Bir daha aynı token ile `/me` veya başka korumalı endpoint’e istek atıldığında `get_current_user` veritabanında bu jti için `revoked_at == None` koşulunu sağlayan bir satır bulamayacak ve **401** döndürecek. Yani “çıkış” = token’ı kara listeye almak; token hâlâ geçerli imzaya ve süreye sahip olsa bile sunucu onu artık kabul etmez.

Bu yapıya **token revocation** (token iptali) veya projedeki benzetmeyle **“kara liste”** denir. Saf JWT’de token süresi dolana kadar geçerli kalır; bu projede veritabanında oturum takibi sayesinde çıkış anında token devre dışı bırakılır.

---

## ✅ Özet — Ne yaptık, arka planda ne oldu?

| Adım | Pratikte ne yaptık? | Arkada ne oldu? |
|------|----------------------|------------------|
| 1–4 | Python, paketler, sunucu | Ortam hazırlandı; `init_db()` ile tablolar oluşturuldu. |
| 5 | /docs açtık | Swagger UI, OpenAPI’den üretildi. |
| 6 | Register | Şifre Bcrypt ile hash’lendi; `users` tablosuna tek satır eklendi. |
| 7 | Login | Şifre doğrulandı; 2 JWT üretildi; her biri `sessions` tablosuna yazıldı. |
| 8 | Authorize | Token Swagger’a tanıtıldı; her istekte Bearer header’a eklenecek. |
| 9 | /me | Token decode + kara liste (revoked) kontrolü + kullanıcı bulundu; yanıt döndü. |
| 10 | Logout | Token’ın jti’si için `revoked_at` dolduruldu; aynı token artık geçersiz. |

Bu akışı tamamladıysanız, hem kullanıcı tarafında adımları hem de arkadaki mantık ve algoritmaları (hash, JWT, kara liste) uygulayarak görmüş oldunuz.

---

## 🆘 Sık karşılaşılan sorunlar

- **“python / pip bulunamadı”:** Python’u PATH’e ekleyerek kurun veya `python3` / `pip3` deneyin.
- **“Port 8000 kullanımda”:** Başka bir program 8000 kullanıyordur. Kapatın veya `uvicorn app:app --reload --port 8001` deneyin; tarayıcıda `http://127.0.0.1:8001/docs` açın.
- **401 Unauthorized /me’de:** Token’ı Authorize’a yapıştırmayı unutmuş veya yanlış yapıştırmış olabilirsiniz. Login’i tekrar yapıp yeni token ile Authorize’ı güncelleyin.
- **“E-posta zaten kullanımda”:** Aynı e-postayla ikinci kez register denediniz. Farklı e-posta kullanın veya doğrudan login yapın.

---

## 📚 Bundan sonra

- Tüm endpoint’ler ve örnekler: [API Dokümantasyonu](./api_dokumantasyonu.md)
- Kurulum özeti: [Başlangıç Rehberi](./baslangic_rehberi.md)
- Mimari ve güvenlik: [Mimari Yapı](./mimari_yapi.md), [Güvenlik Rehberi](./guvenlik_rehberi.md)
- Sistemi kod tarafında adım adım inşa etmek: [Öğrenim Rehberi](../demo-app-1/docs/README.md)

*Takıldığınız bir adım olursa, hangi adımda ve ne gördüğünüzü not ederseniz birine sorarken işiniz kolaylaşır.*

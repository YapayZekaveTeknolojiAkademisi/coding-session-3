# 🛣 05 - Route Tanımları ve Mantık

Tüm bileşenleri `app.py` içerisinde birleştiriyoruz. Burası uygulamanın "beyni"dir.

## 1. Kimlik Doğrulama Bağımlılığı (`get_current_user`)
Korumalı yolları kilitleyen anahtardır. Şu adımları izler:
1. Header'dan token'ı al.
2. Token'ı çöz (`decode`).
3. Veritabanına git: "Bu ID'li token iptal edilmiş mi? (Revoked check)".
4. Eğer iptal edilmişse girişe izin verme (401).

## 2. Kritik Endpoint Mantıkları:

### `/login`:
Aynı anda hem **Access** hem de **Refresh** token üretir ve ikisini de veritabanındaki `sessions` tablosuna kaydeder. Böylece ikisini de istediğimiz zaman iptal edebiliriz.

### `/logout`:
Kullanıcının o an kullandığı token'ın `jti` (numarasını) veritabanında bulur ve `revoked_at` alanını şu anki zamanla doldurur.

### `/refresh`:
Sadece `refresh_token` kabul eder. Eski `access_token`'a bakmaz. Yeni bir `access_token` üretir ve onu da veritabanına kaydeder.

## 🛠 Görev:
1. `app.on_event("startup")` içinde `init_db()` çağrısı yaparak tabloların oluşmasını sağla.
2. `get_session` bağımlılığını her database işlemi yapan endpoint'e ekle.

# 🔐 Güvenlik ve Algoritma Rehberi

Bu proje, modern güvenlik standartlarını (industry standards) takip ederek kullanıcı verilerini korur.

## 1. Şifre Güvenliği (Bcrypt Hashing)

Şifreler asla veritabanına doğrudan yazılmaz. `hash_manager.py` içerisinde bulunan Bcrypt algoritması sayesinde:
- **Salt (Tuzlama):** Her şifreye rastgele bir veri eklenir, böylece aynı şifreyi kullanan iki kişinin hash'i farklı olur.
- **Maliyet (Work Factor):** Şifre kırma saldırılarını yavaşlatmak için işlemci maliyetli bir yöntem kullanılır.

## 2. JWT (JSON Web Token) Yapısı

Oturum yönetimi için `jwt_manager.py` kullanılır.
- **Stateless:** Sunucu her kullanıcı için hafızada yer tutmaz, bilgi token'ın içindedir.
- **İmza:** Token'lar `SECRET_KEY` ile imzalanır, böylece içeriği değiştirilemez.

## 3. Access & Refresh Token Mantığı

- **Access Token:** Kısa sürelidir (varsayılan 1 dk). Çalınsa bile kısa süre sonra geçersiz olur.
- **Refresh Token:** Daha uzun sürelidir. Kullanıcı her dakika şifre girmesin diye yeni Access Token almak için kullanılır.

## 4. Session Revocation (Oturum İptali)

Çoğu JWT sisteminin aksine, bu projede **"Kara Liste"** kontrolü vardır.
- Çıkış (Logout) yapıldığında, token veritabanındaki `sessions` tablosunda `revoked_at` olarak işaretlenir.
- Token'ın süresi dolsa bile, iptal edilmişse sisteme giriş yapılamaz.

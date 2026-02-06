# 📚 Kimlik Doğrulama Sistemi — Öğrenim Rehberi

Sıfırdan kendi **auth (kimlik doğrulama)** sistemini kurmak isteyenler için hazırlanmış bu rehber, adım adım ilerleyerek JWT tabanlı, güvenli bir oturum yönetimi yapısını anlamanı ve inşa etmeni sağlar.

---

## 🎬 Önce denemek istiyorum

Uygulamayı hiç bilmeden çalıştırıp Swagger ile test etmek ve **arkadaki mantık/algoritmayı** okumak istersen:

👉 **[Adım Adım Başlangıç Rehberi](../../docs/adim_adim_baslangic_rehberi.md)** — 10 adım + her adımda hash, JWT ve kara liste açıklaması.

---

## 🗺 Rehber Adımları (Kod ile inşa)

| # | Konu | Açıklama |
|---|------|----------|
| 1 | [Veritabanı Mimarisi](./rehber/01_veritabani_mimarisi.md) | SQLAlchemy, tablolar (User, Session) ve bağlantı yapısı |
| 2 | [Hash Manager](./rehber/02_hash_manager.md) | Şifre güvenliği ve Bcrypt ile hash/doğrulama |
| 3 | [JWT Manager](./rehber/03_jwt_manager.md) | Access/Refresh token üretimi ve doğrulama |
| 4 | [Planlama ve Şemalar](./rehber/04_planlama_ve_semalar.md) | Pydantic şemaları ve API giriş/çıkış modelleri |
| 5 | [Route Tanımları](./rehber/05_rote_tanimlari.md) | Endpoint mantığı, `get_current_user` ve korumalı yollar |
| 6 | [Çalıştırma ve Test](./rehber/06_calistirma_ve_postman.md) | Uygulamayı çalıştırma ve Postman/Bruno ile tam döngü testi |

---

## 🎯 Bu Rehberi Bitirdiğinde

- Veritabanında kullanıcı ve oturum bilgilerini nasıl tutacağını,
- Şifreleri nasıl güvenli hash’leyip doğrulayacağını,
- JWT ile access/refresh token akışını ve “kara liste” (revocation) mantığını,
- FastAPI ile kayıt, giriş, çıkış ve token yenileme uç noktalarını

öğrenmiş olacaksın.

---

## 📚 Bundan sonra

- [API Dokümantasyonu](../../docs/api_dokumantasyonu.md) — Tüm endpoint’ler ve örnekler  
- [Mimari Yapı](../../docs/mimari_yapi.md) — Dosya düzeni ve veri akışı  
- [Güvenlik Rehberi](../../docs/guvenlik_rehberi.md) — Şifre, JWT, token iptali  
- [Dokümantasyon İndeksi](../../docs/README.md) — Tüm dökümanların listesi  

---

*İyi kodlamalar!*

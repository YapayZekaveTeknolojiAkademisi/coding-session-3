# 🎫 03 - JWT Manager (Token Yönetimi)

Kullanıcı giriş yaptıktan sonra, ona her defasında şifre sormamak için bir "bileklik" (Token) veririz.

## 1. JWT Anatomisi
`jwt_manager.py` içerisinde oluşturduğumuz token'lar şunları içerir:
- **`sub` (Subject):** Kullanıcının ID'si.
- **`jti` (JWT ID):** Token'ın benzersiz seri numarası.
- **`type`:** 'access' veya 'refresh'.
- **`exp`:** Sona erme zamanı.

## 2. Token Stratejimiz
Projemizde şu süreleri kullanıyoruz:
- **Access Token:** 1 Dakika (Çok güvenli, çalınsa bile ömrü çok kısa).
- **Refresh Token:** 2 Dakika (Test kolaylığı için kısa tutuldu, gerçek projelerde daha uzun olur).

## 3. Güvenlik Notu: `SECRET_KEY`
JWT'lerin içeriği herkes tarafından okunabilir ama **değiştirilemez**. Çünkü değiştirilirse sistemdeki "imza" geçersiz olur. Bu imzayı atmak için gizli bir anahtar (`SECRET_KEY`) kullanılır. Bu anahtarı asla birine vermeyin!

## 🛠 Görev:
1. `PyJWT` kütüphanesini kullan.
2. `decode_token` fonksiyonu içinde `ExpiredSignatureError` (süresi bitmiş) ve `InvalidTokenError` (hatalı token) hatalarını yakala ve 401 hatası fırlat.

# 🏗 Mimari Yapı ve Dosya Düzeni

Proje, sürdürülebilir ve modüler bir yapı üzerine inşa edilmiştir.

## 📁 Klasör Yapısı

- `app.py`: Ana uygulama ve API uç noktaları (Endpoints).
- `database.py`: Veritabanı bağlantısı ve oturum yönetimi.
- `models.py`: Veritabanı tablolarının (User, SessionTable) tanımları.
- `schemas.py`: Veri giriş/çıkış kalıpları (Pydantic modelleri).
- `hash_manager.py`: Şifreleme işlemleri.
- `jwt_manager.py`: Token işlemleri.
- `test.db`: SQLite veritabanı dosyası (Uygulama çalıştığında oluşur).

## 🛠 Kullanılan Teknolojiler

1. **FastAPI:** Hızlı ve modern web framework.
2. **SQLAlchemy:** Veritabanı yönetim aracı (ORM).
3. **SQLite:** Yerel veritabanı.
4. **Bcrypt:** Güvenli şifreleme.
5. **PyJWT:** JSON Web Token kütüphanesi.
6. **Pydantic:** Veri doğrulama.

## 🔄 Veri Akışı

1. Kullanıcı istek atar.
2. `schemas.py` veriyi doğrular.
3. `app.py` mantığı işletir (hash kontrolü, token üretimi vb.).
4. `models.py` ve `database.py` aracılığıyla veritabanı ile konuşulur.
5. Yanıt kullanıcıya iletilir.

# 📁 01 - Veritabanı Mimarisi

Bir kimlik doğrulama sistemi için veritabanı, her şeyin temelidir. Biz bu projede **SQLAlchemy ORM** ve **SQLite** kullanıyoruz.

## 1. Veritabanı Bağlantısı (`database.py`)
İlk adım, veritabanına nasıl bağlanacağımızı belirlemektir.

- **`create_engine`:** Veritabanı dosyasına (`test.db`) olan asıl bağlantıdır.
- **`sessionmaker`:** Her istek için yeni bir veritabanı oturumu oluşturmamızı sağlar.
- **`declarative_base`:** Tablo sınıflarımızın temelidir.

## 2. Modellerin Tasarımı (`models.py`)
İki ana tabloya ihtiyacımız var:

### A. Kullanıcılar Tablosu (`User`)
- `id`: Benzersiz UUID (String).
- `email`: Kullanıcının giriş anahtarı (Unique).
- `password`: Şifrenin **bcrypt** ile hashlenmiş hali.

### B. Oturumlar Tablosu (`SessionTable`)
JWT sistemimizin "Kara Liste" (Revocation) mekanizması buradan yönetilir.
- `token_jti`: Token içerisindeki benzersiz ID. İptal işlemi için kullanılır.
- `token_type`: 'access' veya 'refresh'.
- `expires_at`: Token'ın ne zaman geçersiz olacağı.
- `revoked_at`: Eğer bu alan doluysa, kullanıcı çıkış yapmış demektir.
- `last_used`: Oturumun en son ne zaman kullanıldığı.

## 💡 Kritik Bilgi:
`generate_id` fonksiyonu ile tüm kayıtlarımıza (User ve Session) otomatik olarak benzersiz UUID'ler atıyoruz. Bu, veritabanı güvenliği için sıralı ID'lerden daha iyidir.

## 🛠 Görev:
1. `database.py` içinde `get_session` adında bir generator oluştur (FastAPI Dependency için).
2. `models.py` içinde tabloları ve aralarındaki `relationship` (User <-> Session) bağını kur.

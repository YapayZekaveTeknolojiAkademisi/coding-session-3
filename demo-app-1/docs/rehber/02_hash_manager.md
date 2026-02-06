# 🔐 02 - Hash Manager (Şifre Güvenliği)

Şifreleri asla veritabanına doğrudan yazmayız. Eğer veritabanı çalınırsa, tüm kullanıcıların şifreleri ifşa olur.

## 1. Hashing Nedir?
Şifreyi matematiksel bir formülle (Bcrypt) geri döndürülemez bir karmaşaya dönüştürmektir.

## 2. Bcrypt Kullanımı (`hash_manager.py`)
Bcrypt kullanırken dikkat edilmesi gereken en önemli nokta, şifrelerin **byte** formatına çevrilmesidir.

### Teknik Detaylar:
- **`encode('utf-8')`:** Kullanıcının girdiği string şifreyi bilgisayarın anlayacağı byte formatına çevirir.
- **`gensalt()`:** Her şifreleme işlemi için rastgele bir "tuz" üretir. Bu sayede iki aynı şifrenin hash'i farklı olur.
- **`checkpw`:** Girilen şifreyi veritabanındaki hash ile karşılaştırırken yine byte dönüşümü yapmak gerekir.

## 💡 Dikkat:
Veritabanına kaydederken `.decode('utf-8')` yaparak karmaşayı tekrar string olarak saklarız.

## 🛠 Görev:
1. `bcrypt` kütüphanesini kur (`pip install bcrypt`).
2. `hash_password` ve `verify_password` metodlarını `HashManager` sınıfı içinde `@staticmethod` olarak tanımla.

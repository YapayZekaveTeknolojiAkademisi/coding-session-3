# 📖 Proje Dokümantasyonu

FastAPI ile geliştirilmiş **Kimlik Doğrulama ve Oturum Yönetimi** projesinin merkezi dokümantasyon indeksidir.

👉 **Proje kökü:** [Ana README](../README.md)

---

## 🚀 Başlangıç

| Doküman | İçerik |
|--------|--------|
| [**Adım Adım Başlangıç Rehberi**](./adim_adim_baslangic_rehberi.md) | Hiç bilmeyenler için: kurulum, çalıştırma, Swagger ile test (10 adım). Her adımda **arkadaki mantık ve algoritma** (hash, JWT, kara liste) anlatılır. |
| [**Başlangıç Rehberi**](./baslangic_rehberi.md) | Kurulum ve ilk test (kısa özet). Bruno ile test. |

---

## 📁 Dokümantasyon Haritası

### Genel

| Doküman | Açıklama |
|--------|----------|
| [**Mimari Yapı**](./mimari_yapi.md) | Klasör yapısı, kullanılan teknolojiler ve veri akışı |
| [**API Dokümantasyonu**](./api_dokumantasyonu.md) | Tüm endpoint’ler, istek/yanıt örnekleri ve Bruno kullanımı |
| [**Güvenlik Rehberi**](./guvenlik_rehberi.md) | Şifre hash’leme, JWT, token süreleri ve oturum iptali |

### Öğrenim (kod ile inşa)

Uygulamayı sıfırdan anlamak ve geliştirmek için:

👉 **[demo-app-1/docs README](../demo-app-1/docs/README.md)** — 6 adımlık öğrenim rehberi (veritabanı → hash → JWT → şemalar → route’lar → test).

---

## 🔗 Özet Akış

```
Kayıt (/register) → Giriş (/login) → Access + Refresh token
       ↓                    ↓
   Hash (Bcrypt)      Session DB’ye yazılır
                            ↓
              Korumalı istekler: Authorization: Bearer <access_token>
                            ↓
              Token yenileme: /refresh (refresh_token ile)
              Çıkış: /logout (token iptal / kara liste)
```

---

*Sorularınız için proje içi rehberleri ve kod yorumlarını kullanabilirsiniz.*

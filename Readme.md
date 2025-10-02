# 📊 ETL Pipeline - JSONPlaceholder API to PostgreSQL

Bu proje, **JSONPlaceholder API**'den veri çekerek PostgreSQL veritabanına yükleyen tam otomatik bir **ETL (Extract, Transform, Load)** pipeline'ıdır.

---

## 🎯 Proje Amacı

- JSONPlaceholder API'den **users**, **posts** ve **comments** verilerini çekmek
- Verileri temizlemek ve dönüştürmek
- PostgreSQL veritabanına **upsert** (insert or update) mantığıyla yüklemek
- Production-ready, güvenli ve performanslı bir ETL süreci oluşturmak

---

## 🏗️ Mimari

```
┌─────────────────┐
│ JSONPlaceholder │
│      API        │
└────────┬────────┘
         │ Extract
         ▼
┌─────────────────┐
│   Transform     │
│  (Pandas)       │
└────────┬────────┘
         │ Load
         ▼
┌─────────────────┐
│   PostgreSQL    │
│   Database      │
└─────────────────┘
```

---

## 📂 Proje Yapısı

```
ETL/
├── database/
│   └── tables.sql          # Veritabanı tablo şemaları
├── .env                    # Veritabanı bağlantı bilgileri
├── etl.py                  # Ana ETL pipeline kodu
├── main.py                 # ETL sürecini başlatan script
├── requirements.txt        # Python bağımlılıkları
└── README.md              # Bu dosya
```

---

## 🗄️ Veritabanı Şeması

### Users Tablosu
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    username VARCHAR(50),
    city VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20),
    website VARCHAR(100),
    company_name VARCHAR(100),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

### Posts Tablosu
```sql
CREATE TABLE posts (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    title VARCHAR(200),
    body TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

### Comments Tablosu
```sql
CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    post_id INTEGER REFERENCES posts(id),
    name VARCHAR(100),
    email VARCHAR(100),
    body TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

---


## 📊 ETL Süreci

### 1. **Extract (Veri Çekme)**

```python
# JSONPlaceholder API'den veri çekme
users = fetch_data("https://jsonplaceholder.typicode.com/users")
posts = fetch_data("https://jsonplaceholder.typicode.com/posts")
comments = fetch_data("https://jsonplaceholder.typicode.com/comments")
```

**Özellikler:**
- ✅ Timeout kontrolü (15 saniye)
- ✅ HTTP hata yönetimi
- ✅ Retry mekanizması

---

### 2. **Transform (Veri Dönüştürme)**

```python
# Nested JSON alanlarını düzleştir
users_df.rename(columns={"address.city": "city", "company.name": "company_name"})

# Veri temizleme
- Email formatı kontrolü
- Telefon numarası standardizasyonu
- Duplicate kayıtları kaldır
- Timestamp ekleme
```

**Temizleme Kuralları:**
- Email: Küçük harfe çevir, @ kontrolü yap
- Phone: Sadece rakam ve + karakteri bırak
- Username: Küçük harfe çevir
- Website: Küçük harfe çevir

---

### 3. **Load (Veri Yükleme)**

```python
# Temp tablo kullanarak bulk upsert
1. DataFrame → Temp tablo
2. Temp tablo → Ana tablo (ON CONFLICT DO UPDATE)
3. Temp tabloyu sil
```

**Upsert Stratejisi:**
- Çakışma varsa: Güncelle (`updated_at` değişir)
- Çakışma yoksa: Yeni kayıt ekle
- Primary key çakışması `ON CONFLICT` ile yönetilir

---

## 🔧 Teknik Detaylar

### Kullanılan Teknolojiler

| Teknoloji | Amaç |
|-----------|------|
| **Python 3.x** | Ana programlama dili |
| **Pandas** | Veri manipülasyonu |
| **SQLAlchemy** | Veritabanı ORM |
| **psycopg2** | PostgreSQL driver |
| **requests** | HTTP istekleri |
| **python-dotenv** | Environment variables |

---

### Performans Optimizasyonları

1. **Bulk Insert**: Temp tablo kullanarak tek sorguda tüm kayıtları yükler
2. **Upsert**: `ON CONFLICT DO UPDATE` ile gereksiz işlemler önlenir
3. **Batch Processing**: Her tablo için ayrı transaction



### Güvenlik

✅ **SQL Injection Koruması**
- Pandas `to_sql()` parametreli sorgu kullanır
- Kullanıcı input'u yok
- Dinamik SQL oluşturulmaz

✅ **Veri Doğrulama**
- Email format kontrolü
- Duplicate kontrol
- Null değer yönetimi

---

## 📝 Log Örnekleri

```
2025-10-02 10:30:15 - INFO - 🚀 ETL süreci başladı
2025-10-02 10:30:16 - INFO - Extract: API'den veri çekiliyor...
2025-10-02 10:30:17 - INFO - ✓ 10 users, 100 posts, 500 comments çekildi
2025-10-02 10:30:18 - INFO - Transform: Veri dönüştürülüyor...
2025-10-02 10:30:19 - INFO - ✓ Transform tamamlandı
2025-10-02 10:30:20 - INFO - Load: Raw SQL ile upsert başladı
2025-10-02 10:30:21 - INFO - ✓ 10 kullanıcı upsert edildi
2025-10-02 10:30:22 - INFO - ✓ 100 gönderi upsert edildi
2025-10-02 10:30:23 - INFO - ✓ 500 yorum upsert edildi
2025-10-02 10:30:24 - INFO - ✅ ETL süreci tamamlandı
```



### Gelecekteki Özellikler

- [ ] Airflow ile zamanlı çalıştırma (daily/hourly)
- [ ] Data validation (Great Expectations)
- [ ] Monitoring dashboard (Grafana)
- [ ] Error notification (email/Slack)
- [ ] Docker containerization
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Unit tests
- [ ] Incremental load (sadece yeni kayıtlar)

---

## 📌 Notlar

### Veri Kaynağı
- JSONPlaceholder fake API kullanır (test için)
- Production'da gerçek API endpoint'leri kullanılmalı



## 👤 Geliştirici

**Uygar**  
Data Engineer



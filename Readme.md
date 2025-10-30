# 🚀 ETL Pipeline - Apache Airflow + JSONPlaceholder API

Bu proje, **Apache Airflow** ile orkestre edilen, **JSONPlaceholder API**'den veri çekerek PostgreSQL veritabanına yükleyen tam otomatik bir **ETL (Extract, Transform, Load)** pipeline'ıdır.


---

## 🎯 Proje Özellikleri

- ✅ **Apache Airflow** ile pipeline orchestration
- ✅ **Docker Compose** ile tek komutla kurulum
- ✅ **PostgreSQL** ile veri depolama
- ✅ **CeleryExecutor** ile paralel task çalıştırma
- ✅ **Upsert** stratejisi ile veri güncelleme
- ✅ **Environment Variables** ile güvenli konfigürasyon
- ✅ Profesyonel **logging** ve hata yönetimi

---

## 🏗️ Sistem Mimarisi

```
┌─────────────────────────────────────────────────────┐
│                 Apache Airflow                       │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────┐ │
│  │  Scheduler  │  │  Web Server  │  │   Worker   │ │
│  └─────────────┘  └──────────────┘  └────────────┘ │
└───────────┬─────────────────────────────────────────┘
            │
            ▼
    ┌───────────────┐
    │   ETL DAG     │
    └───────┬───────┘
            │
    ┌───────▼────────┬──────────────┬────────────┐
    │                │              │            │
    ▼                ▼              ▼            ▼
┌─────────┐   ┌──────────┐   ┌─────────┐   ┌──────────┐
│ Extract │→  │Transform │→  │  Load   │→  │PostgreSQL│
└─────────┘   └──────────┘   └─────────┘   └──────────┘
    │
    ▼
┌──────────────────┐
│ JSONPlaceholder  │
│      API         │
└──────────────────┘
```

---

## 📂 Proje Yapısı

```
ETL/
├── dags/
│   └── etl_pipeline.py        # Airflow DAG tanımı
├── database/
│   ├── tables.sql             # Veritabanı tablo şemaları
│   └── tables_updates.sql     # Güncelleme SQL'leri
├── logs/                      # Airflow logları
├── plugins/                   # Airflow eklentileri
├── config/                    # Airflow konfigürasyonları
├── docker-compose.yaml        # Docker Compose konfigürasyonu
├── etl.py                     # ETL işlemleri (Extract, Transform, Load)
├── .env                       # Environment variables
├── .gitignore                 # Git ignore kuralları
└── README.md                  # Bu dosya
```

---



## 📊 ETL Süreci Detayları

### 1. **Extract (Veri Çekme)**

```python
def extract_data():
    users = fetch_data("https://jsonplaceholder.typicode.com/users")
    posts = fetch_data("https://jsonplaceholder.typicode.com/posts")
    comments = fetch_data("https://jsonplaceholder.typicode.com/comments")
    return users_df, posts_df, comments_df
```

**Özellikler:**
- ✅ Timeout kontrolü (15 saniye)
- ✅ HTTP hata yönetimi
- ✅ Exception handling

### 2. **Transform (Veri Dönüştürme)**

**Veri Temizleme İşlemleri:**
- Email formatı kontrolü (`@` işareti zorunlu)
- Telefon numarası standardizasyonu (sadece rakam ve `+`)
- Duplicate kayıtları kaldırma
- Timestamp ekleme (`created_at`, `updated_at`)
- Nested JSON alanlarını düzleştirme

**Örnek Dönüşümler:**
```python
# Email temizleme
df['email'] = df['email'].str.lower().str.strip()
df['email'] = np.where(df['email'].str.contains("@"), df['email'], "invalid_email")

# Telefon temizleme
df['phone'] = df['phone'].str.replace(r'[^0-9+]', '', regex=True)

# Nested field düzleştirme
df.rename(columns={"address.city": "city", "company.name": "company_name"})
```

### 3. **Load (Veri Yükleme)**

**Upsert Stratejisi:**
```sql
INSERT INTO users(...)
VALUES (...)
ON CONFLICT (id) DO UPDATE SET
    name = EXCLUDED.name,
    email = EXCLUDED.email,
    updated_at = EXCLUDED.updated_at
```

**Avantajları:**
- Duplicate kayıt oluşturmaz
- Mevcut kayıtları günceller
- Yeni kayıtları ekler
- Atomik işlem (transaction)

---

## 🗄️ Veritabanı Şeması

### Users Tablosu
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
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
    id SERIAL PRIMARY KEY,
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
    id SERIAL PRIMARY KEY,
    post_id INTEGER REFERENCES posts(id),
    name VARCHAR(100),
    email VARCHAR(100),
    body TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```


## 🎛️ Airflow DAG Yapısı

```python
@dag(
    dag_id='etl_pipeline',
    start_date=datetime(2025, 1, 1),
    catchup=False
)
def etl_pipeline_taskflow():
    @task
    def extract():
        # Extract işlemleri
        return data
    
    @task
    def transform(data):
        # Transform işlemleri
        return transformed_data
    
    @task
    def load(data):
        # Load işlemleri
        pass
    
    # Task dependencies
    extracted = extract()
    transformed = transform(extracted)
    load(transformed)
```

---

## 🔧 Kullanılan Teknolojiler

| Teknoloji | Versiyon | Amaç |
|-----------|----------|------|
| **Apache Airflow** | 3.1.0 | Workflow orchestration |
| **PostgreSQL** | 16 | Veri depolama |
| **Redis** | 7.2 | Celery message broker |
| **Python** | 3.x | ETL scripting |
| **Pandas** | Latest | Veri manipülasyonu |
| **SQLAlchemy** | Latest | Database ORM |
| **Docker Compose** | Latest | Container orchestration |

---




---

## 📈 Performans Optimizasyonları

1. **Bulk Insert**: Temp tablo kullanarak tek sorguda tüm kayıtları yükler
2. **Upsert**: `ON CONFLICT` ile gereksiz işlemler önlenir
3. **Paralel Execution**: CeleryExecutor ile task'lar paralel çalışır
4. **Connection Pooling**: SQLAlchemy ile verimli DB bağlantıları

---

## 🔒 Güvenlik

- ✅ **Environment Variables**: Hassas bilgiler `.env` dosyasında
- ✅ **SQL Injection Koruması**: Parametreli sorgular kullanılır
- ✅ **Git Ignore**: `.env` dosyası commit edilmez
- ✅ **Docker Network**: Servisler izole network'te çalışır

---

## 📝 Log Örnekleri

```
2025-10-03 11:05:15 - INFO - ETL süreci başladı
2025-10-03 11:05:16 - INFO - Extract: API'den veri çekiliyor...
2025-10-03 11:05:17 - INFO - ✓ 10 users, 100 posts, 500 comments çekildi
2025-10-03 11:05:18 - INFO - Transform: Veri dönüştürülüyor...
2025-10-03 11:05:19 - INFO - ✓ Transform tamamlandı
2025-10-03 11:05:20 - INFO - Load: Veritabanına yükleniyor...
2025-10-03 11:05:21 - INFO - Users tablosu güncellendi. (upsert)
2025-10-03 11:05:22 - INFO - Posts tablosu güncellendi. (upsert)
2025-10-03 11:05:23 - INFO - Comments tablosu güncellendi. (upsert)
2025-10-03 11:05:24 - INFO - ✅ ETL süreci tamamlandı
```

---


# 📌 Project Roadmap - ETL Pipeline (JSONPlaceholder)

Bu dosya, JSONPlaceholder API kullanarak ETL projesini gerçekleştirirken izlenecek adımları yol haritası şeklinde özetlemektedir.

---

## 1. Veri Kaynağını Belirleme (Extract)
- [X] JSONPlaceholder API'den 3 endpoint çek:
  - Users: `https://jsonplaceholder.typicode.com/users`
  - Posts: `https://jsonplaceholder.typicode.com/posts`
  - Comments: `https://jsonplaceholder.typicode.com/comm    ents`
- [X] requests kütüphanesi ile veri çekme denemesi yap
- [X] Gelen JSON yapısını incele ve nested alanları (address, geo, company) tespit et
- [X] Her endpoint için hangi alanlara ihtiyaç olduğunu belirle

---

## 2. Veri Tabanı Tasarımı (Load Hedefi)
- [ ] PostgreSQL üzerinde `jsonplaceholder_db` isimli veri tabanı oluştur
- [ ] 3 ana tablo tasarla:
  - `users` (id, name, username, email, phone, website, city, company_name)
  - `posts` (id, user_id, title, body, created_at)
  - `comments` (id, post_id, name, email, body, created_at)
- [ ] SQL script ile tabloları oluştur
- [ ] Foreign key ilişkilerini kur (users ↔ posts ↔ comments)

---

## 3. Dönüştürme Adımı (Transform)
- [ ] JSON → DataFrame dönüştür (`pd.json_normalize()` kullan)
- [ ] Nested alanları düzleştir (address.city, company.name gibi)
- [ ] Sütun adlarını standartlaştır (snake_case formatına çevir)
- [ ] Null değerleri temizle veya varsayılan değer ata
- [ ] Email formatlarını validate et
- [ ] Timestamp alanları ekle (created_at, updated_at)
- [ ] Gereksiz kolonları kaldır

---

## 4. Veri Kalitesi Kontrolleri
- [ ] Duplicate kayıtları tespit et ve temizle
- [ ] Email ve telefon formatlarını doğrula
- [ ] Her post'un geçerli bir user_id'si olduğunu kontrol et
- [ ] Her comment'in geçerli bir post_id'si olduğunu kontrol et
- [ ] Eksik verileri raporla

---

## 5. PostgreSQL'e Yükleme (Load)
- [ ] Python → PostgreSQL bağlantısı kur (SQLAlchemy kullan)
- [ ] DataFrame'den tablolara bulk insert yap
- [ ] Duplicate kayıt kontrolü ekle (ON CONFLICT stratejisi)
- [ ] Transaction yönetimi ekle (hata durumunda rollback)
- [ ] Yükleme sonrası kayıt sayılarını doğrula

---

## 6. Pipeline Otomasyonu
- [ ] extract.py, transform.py, load.py dosyalarını ayır
- [ ] main.py ile tüm pipeline'ı orkestre et
- [ ] Hata yönetimi ve logging ekle
- [ ] Config dosyası oluştur (API URL, DB credentials)
- [ ] Başarısız işlemleri yeniden deneme (retry) mekanizması ekle

---

## 7. Analiz ve Raporlama
- [ ] PostgreSQL'den SQL sorguları yaz:
  - En çok post yazan kullanıcılar
  - En çok yorum alan postlar
  - Kullanıcı başına ortalama post/comment sayısı
  - Şehir bazında kullanıcı dağılımı
- [ ] Pandas ile veri analizi yap
- [ ] Matplotlib/Seaborn ile görselleştirme oluştur

---

## 8. İleri Seviye Geliştirmeler (Opsiyonel)
- [ ] Incremental loading ekle (sadece yeni/değişen kayıtları çek)
- [ ] Apache Airflow ile DAG oluştur
- [ ] Docker container'ı hazırla
- [ ] Unit test yaz (pytest ile)
- [ ] Data quality metrics dashboard'u oluştur

---

## 9. Proje Dokümantasyonu
- [ ] README.md dosyası hazırla:
  - Proje amacı ve mimari
  - Kurulum adımları
  - Kullanım kılavuzu
  - ER diyagramı
- [ ] requirements.txt oluştur
- [ ] ETL pipeline akış şeması çiz
- [ ] Kod içine docstring ve comment ekle
- [ ] GitHub'a yükle ve profesyonel açıklama yaz

---

## 🎯 Nihai Çıktı
- ✅ Otomatik çalışan ETL pipeline
- ✅ PostgreSQL'de normalize edilmiş veri tabanı
- ✅ İlişkisel veri yapısı (users → posts → comments)
- ✅ Veri kalitesi kontrolleri
- ✅ Analiz sorguları ve raporlar
- ✅ GitHub'da profesyonel proje portföyü

---

## 📚 Öğrenilecek Beceriler
- REST API entegrasyonu
- JSON veri işleme ve normalizasyon
- Pandas ile veri dönüştürme
- PostgreSQL veri modelleme
- ETL pipeline tasarımı
- Hata yönetimi ve logging
- SQL sorgu optimizasyonu
- Versiyon kontrolü (Git)

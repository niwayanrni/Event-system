# 📦 Event System with Idempotency & Deduplication

## 📌 Deskripsi Proyek

Proyek ini merupakan implementasi **event-driven system** menggunakan **Docker Compose** yang mendukung:

- ✅ At-least-once delivery  
- ✅ Idempotency & deduplication persisten  
- ✅ Transaksi aman terhadap race condition  
- ✅ Multi-worker concurrent processing  
- ✅ Persistensi data meskipun container direstart  

Sistem dirancang agar **event dengan kombinasi `(topic, event_id)` yang sama hanya diproses satu kali**, meskipun dikirim berulang atau terjadi restart layanan.


## 🧱 Arsitektur Sistem

Sistem terdiri dari empat layanan utama yang berjalan dalam satu jaringan Docker Compose.

### 1️⃣ Aggregator
- API utama sistem (FastAPI)
- Endpoint untuk publish event dan monitoring
- Menyimpan event unik ke database
- Menjalankan worker internal untuk memproses event dari broker
- Menjamin idempotency melalui constraint unik `(topic, event_id)`

### 2️⃣ Publisher
- Simulator pengirim event
- Mengirim batch event dengan ±30% duplikasi
- Membuktikan skema **at-least-once delivery**

### 3️⃣ Broker (Redis)
- Queue internal berbasis Redis
- Mendukung pemrosesan paralel oleh multiple worker
- Digunakan untuk decoupling publisher dan aggregator

### 4️⃣ Storage (PostgreSQL)
- Database persisten (`postgres:16-alpine`)
- Menyimpan:
  - Event yang telah diproses
  - Statistik pemrosesan
- Data tetap aman meskipun container direstart


## 📑 Model Event

Setiap event memiliki format JSON berikut:

```json
{
  "topic": "string",
  "event_id": "string-unik",
  "timestamp": "ISO8601",
  "source": "string",
  "payload": { }
}


## Link Youtube: https://youtu.be/kB1WWWliOOA


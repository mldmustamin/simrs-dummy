# Panduan Arsitektur Database (Prisma Schema)
*Visi Utama: Database berspesifikasi Enterprise/Ideal yang dilengkapi kapabilitas Multi-Model untuk mode Pragmatis (Fallback).*

## 1. Aturan Dasar Desain Tabel (Enterprise Standard)
- **Soft Deletes Obligatory**: Tidak boleh ada operasi `DELETE` permanen pada data transaksional (pasien, billing, resep). Semua tabel utama wajib menggunakan mekanisme `deleted_at` (DateTime nullable) atau `status` (Aktif/Inaktif).
- **Audit Trails**: Setiap tabel transaksional EMR wajib memiliki `created_at`, `updated_at`, dan `created_by` (NIP Petugas) untuk melacak jejak audit. Waktu klinis (`jam_rawat`) harus dipisahkan dari waktu input sistem (`created_at`).
- **Idempotency Keys**: Semua tabel yang menerima data dari frontend wajib memiliki kolom `idempotency_key` (UUID). Dalam mode Ideal, ini mencegah *double-click*. Dalam mode Pragmatis, ini mencegah duplikasi data saat sinkronisasi *bulk* dari *offline storage*.

## 2. Struktur Tabel Pekerjaan Latar Belakang (Event-Driven & Background Jobs)
Pada operasional ideal, sinkronisasi berjalan *real-time*. Namun, database harus menyediakan infrastruktur *queue* sebagai *fallback* ketika API eksternal (BPJS/SATUSEHAT) *timeout*:
```prisma
model simrs_web_background_job {
  id           String   @id @default(uuid())
  job_type     String   // 'CREATE_SEP_BPJS', 'SEND_SATUSEHAT'
  payload      Json     // Data JSON yang akan dikirim
  status       String   @default("PENDING") // 'PENDING', 'PROCESSING', 'SUCCESS', 'FAILED'
  retry_count  Int      @default(0)
  max_retries  Int      @default(50) 
  last_error   String?  @db.Text
  created_at   DateTime @default(now())
  processed_at DateTime?
}
```

## 3. Resolusi Tabel `bridging_sep` (Graceful Degradation)
Mode Ideal menuntut SEP langsung terbit. Mode Pragmatis menuntut pendaftaran tetap jalan walau BPJS mati.
- **Strategi**: Gunakan `no_rawat` sebagai Primary Key di sisi lokal. Tabel `bridging_sep` dapat diisi langsung (Real-time) saat koneksi lancar, ATAU dibiarkan `nullable`/opsional di awal dan diisi oleh *background job* ketika mode pragmatis aktif akibat gangguan jaringan.

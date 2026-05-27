# Panduan Arsitektur Database (Prisma Schema)
*Dokumen teknis bagi AI Agent untuk merancang tabel database yang tahan banting (Survivable).*

## 1. Aturan Dasar Desain Tabel
- **Soft Deletes Obligatory**: Tidak boleh ada operasi `DELETE` permanen pada data transaksional (pasien, billing, resep). Semua tabel utama wajib menggunakan mekanisme `deleted_at` (DateTime nullable) atau `status` (Aktif/Inaktif).
- **Audit Trails**: Setiap tabel transaksional EMR wajib memiliki `created_at`, `updated_at`, dan `created_by` (NIP Petugas) untuk melacak jejak audit. Waktu klinis (`jam_rawat`) harus dipisahkan dari waktu input sistem (`created_at`).
- **Idempotency Keys**: Semua tabel yang menerima data dari frontend mode *Offline* wajib memiliki kolom `idempotency_key` (UUID) untuk mencegah duplikasi data saat sinkronisasi ganda.

## 2. Struktur Tabel Pekerjaan Latar Belakang (Background Jobs)
Untuk menghindari *timeout* API eksternal (BPJS/SATUSEHAT) melumpuhkan aplikasi, kita menggunakan tabel antrean di database:
```prisma
model simrs_web_background_job {
  id           String   @id @default(uuid())
  job_type     String   // 'CREATE_SEP_BPJS', 'SEND_SATUSEHAT'
  payload      Json     // Data JSON yang akan dikirim
  status       String   @default("PENDING") // 'PENDING', 'PROCESSING', 'SUCCESS', 'FAILED'
  retry_count  Int      @default(0)
  max_retries  Int      @default(50) // Toleransi tinggi untuk BPJS
  last_error   String?  @db.Text
  created_at   DateTime @default(now())
  processed_at DateTime?
}
```

## 3. Resolusi Tabel `bridging_sep` (Decoupling)
Tabel asli `bridging_sep` menggunakan `no_sep` sebagai Primary Key. Ini **HARUS DIUBAH** karena pendaftaran tidak boleh terblokir jika SEP gagal.
- **Strategi**: Gunakan `no_rawat` sebagai Primary Key sesungguhnya di sisi lokal, dan buat `no_sep` menjadi bersifat opsional/nullable sampai *background job* berhasil mendapatkannya.

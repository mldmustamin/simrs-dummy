import os

folder_path = "/home/gudang-data-kantor/simrs-web/docs/Implementasi"

docs = {
    "01_DATABASE_SCHEMA_GUIDELINES.md": """# Panduan Arsitektur Database (Prisma Schema)
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
""",
    "02_BACKEND_NESTJS_GUIDELINES.md": """# Panduan Arsitektur Backend (NestJS)
*Visi Utama: Backend berspesifikasi Smart Hospital (Event-Driven) yang dapat menyesuaikan diri (Feature Flags) dengan infrastruktur daerah.*

## 1. Event-Driven Architecture (Pub/Sub)
Dalam mode Enterprise Ideal, sistem tidak beroperasi secara linear. Gunakan `@nestjs/event-emitter`.
- **Standar Ideal**: `KasirService.bayar()` menembakkan event `kasir.pembayaran_sukses`. Kemudian `ApotekListener`, `AkuntansiListener`, dan `SmartDashboardListener` merespons event tersebut secara *real-time* dan asinkronus.

## 2. Proteksi Concurrency & Pessimistic Locking
Setiap transaksi finansial dan inventori di tingkat RS Besar sangat tinggi. Perlindungan mutlak diperlukan.
- Gunakan Prisma Raw Query untuk mengeksekusi `SELECT ... FOR UPDATE` jika berhadapan dengan data tunggal yang rentan *race-condition*.
- Selalu gunakan blok `$transaction` Prisma yang membungkus semua operasi terkait menjadi satu kesatuan atomik (ACID).

## 3. Mekanisme Multi-Model (Feature Flags & Graceful Degradation)
API Backend dibangun dengan standar parameter yang lengkap dan ketat. Namun, sediakan fleksibilitas (*Feature Toggles*) untuk faskes tipe rendah.
- Gunakan DTO dengan validasi ketat untuk RS Enterprise, namun sediakan mode `LITE_MODE` di konfigurasi global yang dapat mereduksi tingkat kewajiban (Required Fields) menjadi `IsOptional()` untuk data non-kritis, guna menyelamatkan operasional di situasi darurat atau faskes dengan SDM minim.
""",
    "03_FRONTEND_REACT_GUIDELINES.md": """# Panduan Arsitektur Frontend (React/Vite)
*Visi Utama: UI/UX canggih, responsif, dan *paperless* mutlak, dengan fitur Offline-Ready sebagai katup pengaman.*

## 1. Implementasi PWA & Offline Storage (Kapasitas Fallback)
Meskipun didesain untuk Cloud & Local Server bertenaga tinggi, Frontend tidak boleh menampilkan *White Screen of Death* saat LAN terputus sementara.
- **Standar Utama**: Operasi sinkron dan asinkron melalui Websocket/REST yang cepat.
- **Lapisan Pragmatis**: Gunakan Workbox dan `localForage` (IndexedDB) untuk menampung *request* sesaat jika aplikasi mendeteksi `navigator.onLine === false`. Begitu terkoneksi, lakukan sinkronisasi otomatis di latar belakang.

## 2. State Management & Optimistic UI
- Terapkan pola **Optimistic UI Updates** menggunakan React Query atau Zustand. Antarmuka harus menyajikan pengalaman *Enterprise* di mana aksi (simpan, klik, geser) bereaksi instan tanpa hambatan visual (*spinner*).
- Indikator status jaringan harus terlihat elegan di sudut layar (Online / Pending Sync).

## 3. Aksesibilitas: Keyboard-First & Touch-First
- UI/UX harus merespons interaksi *Tablet/Touchscreen* untuk dokter yang *visite* menggunakan iPad di bangsal VIP (Mode Ideal).
- Sekaligus mendukung navigasi ekstrem berbasis *Keyboard* (Tab, Enter, Alt+S) untuk petugas loket BPJS yang dituntut kecepatan tinggi tanpa memegang *mouse* (Mode Pragmatis).
""",
    "04_BPJS_INTEGRATION_STRATEGY.md": """# Strategi Integrasi BPJS (Enterprise to Pragmatic)
*Visi Utama: Sinkronisasi real-time paripurna, didukung oleh sistem *Eventually Consistent* sebagai peredam kejut.*

## 1. Flow Real-time (Mode Ideal)
Pada kondisi jaringan BPJS sehat, integrasi beroperasi 100% *real-time*.
1. Petugas klik "Daftar BPJS".
2. API langsung menembak V-Claim, SEP terbit instan (< 1 detik).
3. Pasien memegang validasi digital dan langsung menuju Poli.
4. *Trigger* ke SEP dan INA-CBG terhubung mulus.

## 2. Flow Asinkron (Mode Fallback / Pragmatis)
Ketika server V-Claim tumbang, ERP kita **TIDAK BOLEH** ikut tumbang. Sistem harus beralih mulus ke mode Asinkron.
1. Frontend mengirim *request* ke backend, backend mendeteksi *timeout* dari V-Claim.
2. Backend seketika mengaktifkan mode *Graceful Degradation*: Pasien tetap disimpan di `reg_periksa` (Lokal) dengan nomor antrean RS.
3. Pembuatan SEP dialihkan ke tabel `simrs_web_background_job`.
4. *Cron Job Worker* akan mencoba kembali (*retry exponential backoff*) tanpa disadari petugas.
5. Saat berhasil, SEP diinjeksi ke tabel pasien. Petugas administrasi menyelesaikan sisa urusan kertas secara kolektif di kemudian waktu tanpa menghalangi jalan pasien ke ruang periksa.
""",
    "05_ASYNC_CLINICAL_WORKFLOW.md": """# Panduan Alur Klinis (Enterprise EMR & Async Fallback)
*Visi Utama: *Closed-Loop Electronic Medical Record* yang *perfectly normalized*, dengan fleksibilitas input darurat.*

## 1. Closed-Loop EMR (Mode Ideal)
Operasional utama menuntut dokter melakukan pengisian EMR langsung saat berhadapan dengan pasien.
- **CPOE (Computerized Provider Order Entry)**: Dokter mengklik resep, data langsung mengurangi virtual stok depo, merilis harga ke kasir, dan membunyikan bel di apotek. Semua terekam instan dengan *Digital Signature* (TTE).

## 2. Retrospective Data Entry (Mode Pragmatis)
Sistem memahami bahwa dalam kekacauan ruang IGD atau lonjakan pasien, dokter tidak selalu berada di depan komputer.
- Form EMR menyediakan kolom **Jam Tindakan Real** yang dapat diisi mundur untuk menyesuaikan dengan waktu kejadian asli.
- Kolom sistemik `created_at` tetap tak bisa dimanipulasi untuk memisahkan waktu tindakan dan waktu ketik (Audit Trail).

## 3. Verbal Order & Draft System
- Apoteker dan Perawat memiliki wewenang (*Feature Toggle* khusus darurat) untuk mengeksekusi instruksi lisan dokter demi menyelamatkan nyawa pasien.
- Transaksi ini menghasilkan `Draft Darurat` yang statusnya "Belum Disahkan". Dokter diwajibkan (melalui notifikasi *Smart Dashboard*) untuk melakukan validasi/otorisasi digital dalam waktu maksimal 1x24 jam.
- Jika ada kesalahan pada dokumen yang terlanjur di-TTE, sistem tidak mengizinkan edit langsung (WORM - *Write Once Read Many*), melainkan membangkitkan form **Addendum** berstandar akreditasi internasional.
"""
}

for filename, content in docs.items():
    file_path = os.path.join(folder_path, filename)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

print(f"Berhasil mengondisikan ulang 5 dokumen implementasi dengan visi Multi-Model (Enterprise Ideal + Pragmatic Fallback).")

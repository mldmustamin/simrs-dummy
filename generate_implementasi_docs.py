import os

folder_path = "/home/gudang-data-kantor/simrs-web/docs/Implementasi"
os.makedirs(folder_path, exist_ok=True)

docs = {
    "01_DATABASE_SCHEMA_GUIDELINES.md": """# Panduan Arsitektur Database (Prisma Schema)
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
""",
    "02_BACKEND_NESTJS_GUIDELINES.md": """# Panduan Arsitektur Backend (NestJS)
*Standard Operating Procedure bagi AI Agent saat menulis kode backend API.*

## 1. Event-Driven Architecture (Pub/Sub)
Jangan memanggil *Service* lintas domain secara berantai panjang (Tight Coupling). Gunakan `@nestjs/event-emitter`.
- **Contoh Buruk**: `KasirService.bayar()` memanggil `ApotekService.kurangiStok()` dan `AkuntansiService.jurnal()`.
- **Contoh Baik**: `KasirService.bayar()` menembakkan event `kasir.pembayaran_sukses`. Kemudian `ApotekListener` dan `AkuntansiListener` merespons event tersebut secara independen.

## 2. Proteksi Concurrency & Pessimistic Locking
Setiap transaksi yang berkaitan dengan pengurangan stok fisik (Gudang/Apotek) dan *auto-numbering* kasir (Nomor Nota/Jurnal) **WAJIB** dikunci.
- Gunakan Prisma Raw Query untuk mengeksekusi `SELECT ... FOR UPDATE` jika berhadapan dengan data tunggal yang rentan *race-condition*.
- Selalu gunakan blok `$transaction` Prisma yang membungkus semua operasi terkait menjadi satu kesatuan atomik (ACID).

## 3. Mekanisme Graceful Degradation
API Backend harus mau menerima *payload* yang tidak lengkap dari frontend jika situasi mensyaratkan demikian.
- Gunakan DTO (Data Transfer Object) dengan validasi `IsOptional()` untuk data-data non-kritis (seperti Suhu, Tinggi Badan). Jangan me-reject keseluruhan EMR hanya karena perawat lupa menginput berat badan di tengah *mass casualty* IGD.
""",
    "03_FRONTEND_REACT_GUIDELINES.md": """# Panduan Arsitektur Frontend (React/Vite)
*Panduan teknis bagi AI Agent untuk membangun antarmuka UI/UX yang Offline-First.*

## 1. Implementasi PWA & Offline Storage
Frontend tidak boleh lumpuh (*White Screen of Death*) saat kabel LAN dicabut.
- **Service Workers**: Gunakan Workbox untuk melakukan *caching* semua aset statis (HTML, JS, CSS).
- **IndexedDB (Lokal Database)**: Gunakan library seperti `localForage` atau `Dexie.js` untuk menyimpan antrean *request* POST/PUT saat aplikasi mendeteksi `navigator.onLine === false`.

## 2. State Management & Optimistic UI
Sistem harus terasa secepat kilat (*snappy*) di mata dokter, tanpa loading *spinner* berlarut-larut.
- Terapkan pola **Optimistic UI Updates** menggunakan React Query atau Zustand. Ketika dokter menekan tombol "Simpan Resep", antarmuka langsung menampilkannya sebagai berhasil tersimpan, sementara *request* sinkronisasi terjadi diam-diam di *background*.
- Jika sinkronisasi gagal karena internet terputus, tambahkan ikon kecil ⚠️ (Pending Sync) di sebelah data tersebut, bukan memblokir layar dengan pesan *Error*.

## 3. Keyboard-First Navigation
Di faskes daerah, mouse sering lambat atau meja perawat terlalu sempit.
- Pastikan semua *form* pelayanan kritis (Kasir, Apotek, Pendaftaran) mendukung navigasi penuh menggunakan tombol `Tab`, `Enter`, dan *Shortcut* keyboard khusus (misal `Alt+S` untuk simpan) tanpa harus menggunakan *mouse*.
""",
    "04_BPJS_INTEGRATION_STRATEGY.md": """# Strategi Integrasi BPJS (Eventually Consistent)
*Aturan khusus agen untuk memprogram Bridging V-Claim agar tidak menyandera operasional Faskes.*

## 1. Flowchart Pendaftaran Asinkron
1. Pasien datang membawa rujukan/kartu. Petugas klik "Daftar BPJS".
2. **Frontend** menembak API Backend `POST /api/registrasi`.
3. **Backend** langsung menyimpan pasien ke tabel `reg_periksa` (Lokal) dan men-generate `no_rawat`. Backend menyuntikkan *task* pembuatan SEP ke tabel `simrs_web_background_job`.
4. **Backend** merespons `200 OK` ke frontend dalam waktu kurang dari 500ms. Pasien langsung disuruh duduk di depan Poli, **TANPA** memegang kertas SEP.
5. **Background Worker** (Cron Job) yang berjalan setiap menit mengambil *task* tersebut dan menembak API V-Claim BPJS Kemenkes.
6. Jika V-Claim *timeout* atau MT (Maintenance), *worker* akan menunda (*delay*) dan mencoba lagi (*retry exponential backoff*) 5 menit kemudian.
7. Ketika *worker* berhasil mendapat balasan dari BPJS, nomor SEP diekstrak dan disimpan ke dalam tabel `bridging_sep` milik pasien.

## 2. Penyelesaian Administratif Belakangan
- Kertas SEP bisa di-*print* kolektif oleh admin loket di sore hari, atau cukup ditandatangani pasien secara elektronik di akhir layanan saat mengambil obat di Apotek.
- Arsitektur ini memastikan loket pendaftaran bebas dari penumpukan panjang saat server BPJS nasional sedang tumbang.
""",
    "05_ASYNC_CLINICAL_WORKFLOW.md": """# Panduan Input Asuhan Klinis Asinkron (Retrospektif)
*Panduan teknis untuk menangani kekacauan input dokter/perawat di dunia nyata.*

## 1. Retrospective Data Entry (Pencatatan Mundur)
Sistem harus memfasilitasi dokter IGD atau perawat ICU yang baru sempat membuka komputer di penghujung *shift* kerja mereka.
- Form *EMR / SOAP* di frontend harus memiliki *field* **Jam Tindakan Real** yang bisa diedit mundur oleh perawat secara manual.
- Backend tetap menyimpan `created_at` (jam *server* menyimpan data) untuk menghindari sengketa medikolegal, namun data yang dicetak pada rekam medis fisik/PDF adalah *Jam Tindakan Real* yang diinput.

## 2. Mekanisme Addendum & Revisi EMR
Mengingat kebiasaan "Copy-Paste", kesalahan input pasti terjadi. EMR tidak boleh dikunci absolut tanpa mekanisme revisi yang legal.
- Jika dokumen telah di-TTE (Tanda Tangan Elektronik), maka dokumen terkunci.
- Jika ada perbaikan setelah di-TTE, sistem harus menggunakan mekanisme **Addendum**. Data lama tidak dihapus, melainkan ditumpuk/ditambahkan catatan koreksi dengan penanda waktu baru (menganut kaidah *Write-Once-Read-Many / WORM*).

## 3. Penerimaan Resep Lisan (Verbal Order)
- Apoteker dapat membuat `Draft Resep` tanpa otorisasi digital dokter untuk melayani pasien darurat yang nyawanya terancam (atas perintah lisan/telepon dokter).
- Draft ini dibiarkan menggantung di *dashboard* dokter. Dokter memiliki kewajiban (dan notifikasi *reminder* berkala) untuk me-klik tombol "Validasi Resep Lisan" maksimal dalam waktu 1x24 jam setelah kejadian.
"""
}

for filename, content in docs.items():
    file_path = os.path.join(folder_path, filename)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

print(f"Berhasil membuat 5 dokumen pedoman implementasi di dalam {folder_path}.")

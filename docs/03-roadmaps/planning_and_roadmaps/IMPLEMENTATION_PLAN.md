# Rencana Implementasi dan Eksekusi Refaktor Prioritas

Dokumen ini merangkum rencana teknis detail (Implementation Plan) untuk mengeksekusi prioritas refaktor sesuai dengan keputusan strategis yang telah disepakati.

## Eksekusi akan dilakukan secara bertahap dengan urutan prioritas berikut:

### 1. Audit Trail & RBAC (Prioritas 1)
Menambahkan tabel ekstensi untuk rekam jejak sistem dan mengamankan seluruh *endpoint*.

*   **Modifikasi `schema.prisma`:**
    *   Menambahkan model `simrs_web_audit_trail` (id, module, action, entity_name, entity_id, actor_id, actor_name, ip_address, user_agent, before_payload, after_payload, created_at).
    *   Sinkronisasi menggunakan `db push` (khusus dev).
*   **Pembuatan `AuditService`:** Membuat layanan untuk mencatat log ke database (wajib dalam transaksi untuk endpoint kritis).
*   **Implementasi Guard:** Membuat `JwtAuthGuard` dan `RoleGuard` (RBAC) yang terhubung ke data otorisasi tabel `user`. Memasang Guard pada semua *endpoint write*.

### 2. Modul Kasir - Optimistic Concurrency (Prioritas 2)
Mengamankan *generate* nomor nota dan jurnal dari *race condition*.

*   **Refaktor Kasir:** Membungkus seluruh logika pembuatan nota, jurnal, dan pembaruan registrasi ke dalam `$transaction`.
*   **Retry on Duplicate Key:** Mengimplementasikan tangkapan *error* `P2002` (Duplicate Key) dan *retry* maksimal 5 kali mengulang seluruh proses.
*   **Validasi Keuangan:** Memastikan Debit = Kredit.
*   **Testing:** Uji konkurensi dengan skrip paralel.

### 3. Modul Farmasi Multi-Depo (Prioritas 3)
Menjamin stok obat dipotong dari depo yang tepat.

*   **Endpoint Baru:** `GET /api/farmasi/depo` untuk mengambil master bangsal.
*   **Refaktor Serah Obat:** Mewajibkan parameter `kd_bangsal_asal`. Mengunci baris `gudangbarang` dengan `SELECT ... FOR UPDATE` dan memotong stok. Validasi kecukupan stok (rollback jika kurang).
*   **Frontend:** Menambahkan Dropdown Depo.

### 4. Pendaftaran APS Lab/Radiologi (Prioritas 4)
Menambahkan jalur pendaftaran mandiri tanpa melanggar struktur.

*   **Endpoint Baru:** `POST /api/registrations/aps`.
*   **Anchor `reg_periksa`:** Validasi payload dan tetap men-*generate* `no_rawat` ke dalam tabel `reg_periksa`.
*   **Penunjang:** Membuat billing awal atau order lab/radiologi.

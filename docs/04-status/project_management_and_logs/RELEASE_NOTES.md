# RELEASE_NOTES.md

Catatan perubahan (Changelog) untuk rilis SIMRS-Web (Aladin).

---

## [0.1.2-dev] - 2026-05-27
Status: **SYNCHRONIZED**

### ✅ Perbaikan Struktur Repositori
- Memperbaiki konflik dan anomali *nested git repository* yang sebelumnya terdapat di dalam direktori `simrs-backend`.
- Melakukan penyelarasan versi (force push) untuk memastikan kode tersinkronisasi secara akurat ke *remote repository* `https://github.com/mldmustamin/simrs-dummy.git` pada branch `main`.

## [0.1.1-dev] - 2026-05-27
Status: **STABILIZATION IN PROGRESS**

### ✅ Perbaikan Keamanan & Runtime
- Backend memakai pola **protected-by-default** melalui global `JwtAuthGuard`
  (`APP_GUARD`) dengan pengecualian route publik eksplisit (`@Public()`).
- `ValidationPipe` global diaktifkan untuk menolak field tidak dikenal dan
  mentransform payload DTO.
- CORS kini menggunakan `CORS_ORIGINS` (default development terbatas ke
  `http://localhost:5173`).
- Throttling ditambahkan untuk endpoint publik (login dan kiosk) untuk
  menurunkan risiko abuse.
- Script runtime production backend dikoreksi ke artifact build aktual
  (`dist/src/main`).

### ✅ Quality Gate Iterasi Ini
- Backend unit test distabilkan dan lulus penuh (`22/22 suite`).
- Security e2e test untuk route publik/protected, validation, dan throttling
  lulus.
- Frontend lint sudah tanpa error (masih ada warning non-blocking).

### ⚠️ Masih Dalam Pengerjaan
- Permission mapping legacy per-modul klinis (Lab/Ranap/Operasi).
- Object-level authorization berbasis scope actor terhadap record klinis.
- Proof konkurensi transaksi Kasir/Farmasi pada database aktif.
- Penyelesaian endpoint backend Dashboard/Monitoring yang saat ini dipanggil
  frontend.

## [0.1.0-alpha] - 2026-05-26
Status: **UNSTABLE / PROTOTYPE**

### 🚀 Fitur Baru (Belum Disertifikasi Production)
- **Modul Pendaftaran (FO)**: Mendukung registrasi Poli & IGD. Pembuatan nomor `no_rawat` format baru terintegrasi.
- **Modul Poliklinik (RME)**: Dokter dapat menginput *Subjective, Objective, Assessment, Plan* (SOAP) di `pemeriksaan_ralan`.
- **Modul Laboratorium**: *Dashboard* petugas Lab, penambahan biaya uji lab otomatis.
- **Modul Rawat Inap & Bed Management**: Penarikan ketersediaan tempat tidur Inap, form pengisian CPPT TTV Harian (`pemeriksaan_ranap`).
- **Modul Kasir & Billing**: 
  - Penarikan kumulatif biaya (Registrasi + Tindakan Dr + Obat + Lab + Inap + Operasi).
  - *Auto-posting* Nota Jalan & Jurnal Akuntansi (*Prototype*).
- **Modul Kamar Operasi (OK)**: Integrasi dengan Master Paket Operasi untuk membagi insentif (Operator, Anestesi, Omloop, dsb).

### ⚠️ Known Issues / Technical Debt Terindentifikasi
- **Sistem Keamanan Terbuka**: Belum ada enkripsi *Guard* RBAC di Backend (API bisa *di-hit* publik secara *bypass*).
- **Race Condition Billing Kasir**: Pembuatan Nota belum dilindungi oleh skema kunci transaksi (*Pessimistic Lock*). Menimbulkan potensi ID tabrakan.
- **Stok Farmasi Cacat**: Modul tidak terkoneksi ke gudang barang untuk pengeluaran fisik HPP stok. 

### 🔧 Rencana Rilis Berikutnya (Fokus Refaktor)
- Implementasi Sequence Locking / Pessimistic Locking untuk Kasir.
- Pembuatan NestJS JWT Guard & Roles Guard berdasarkan konfigurasi `user` tabel SIMRS Dummy.
- Refaktor modul Logika Pemotongan Fisik Stok Farmasi (`gudangbarang` & `riwayat_barang_medis`).

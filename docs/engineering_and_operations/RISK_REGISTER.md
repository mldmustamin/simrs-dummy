# RISK_REGISTER.md — Pendaftaran Risiko SIMRS-Web

Dokumen ini memantau risiko sistem berdasarkan dampak (Impact), kemungkinan terjadi (Likelihood), tingkat keparahan (Level), dan status mitigasi.

| ID | Risiko | Dampak | Kemungkinan | Level | Mitigasi | Status |
|:---|:---|:---:|:---:|:---|:---|:---|
| **RSK-01** | **Duplicate/Collision `no_nota` & `no_jurnal`**<br>Dua kasir menekan tombol bayar bersamaan menghasilkan nomor yang sama. | Tinggi | Sedang | **Kritis** | Implementasi fungsi *generator* sequence tersendiri dengan Pessimistic Locking (`SELECT ... FOR UPDATE` via raw query atau Prisma `$transaction` dengan level Isolasi yang ketat). | 🔴 Open |
| **RSK-02** | **Mutasi Stok Farmasi Belum Terverifikasi Operasional**<br>Source telah memotong `gudangbarang` dan menulis `riwayat_barang_medis` dalam transaction, tetapi belum dibuktikan pada konkurensi/depo/racikan. | Tinggi | Sedang | **Kritis** | Jalankan integration test stok cukup/kurang, request paralel, multi-depo, dan resep racikan terhadap database test terkontrol. | 🟡 Mitigasi Parsial |
| **RSK-03** | **Otorisasi Fungsi/Objek Belum Lengkap**<br>JWT global sudah menolak anonymous, tetapi user terautentikasi masih memerlukan verifikasi izin fungsi dan scope record pasien. | Tinggi | Sedang | **Kritis** | `JwtAuthGuard` global telah diterapkan; lanjutkan `PermissionGuard` per fungsi dan object-level authorization setelah mapping hak legacy disahkan. | 🟡 Mitigasi Parsial |
| **RSK-04** | **Cakupan Audit Trail Belum Lengkap**<br>Audit transaction telah tersedia pada Kasir/Farmasi, tetapi cakupan aksi klinis lain belum terverifikasi. | Sedang | Sedang | **Tinggi** | Tetapkan daftar action wajib dan tambahkan integration test audit untuk RME, Lab, Ranap, Operasi, Kasir, serta Farmasi. | 🟡 Mitigasi Parsial |
| **RSK-05** | **Validasi Stok Minus Belum Teruji**<br>Source telah memblokir stok kurang saat penyerahan, tetapi hasil pada request paralel belum dibuktikan. | Tinggi | Sedang | **Tinggi** | Uji `FOR UPDATE`, rollback, dan penyerahan simultan pada database test terkontrol. | 🟡 Mitigasi Parsial |
| **RSK-06** | **Kegagalan Pembuatan SEP (BPJS)**<br>Pasien BPJS lolos daftar tapi SEP gagal di-*generate*. Klaim RS akan hangus. | Tinggi | Tinggi | **Kritis** | Terapkan *Mock API* dan validasi sinkron. Jika SEP gagal terbit, *rollback* pendaftaran atau tandai sebagai "Tunda SEP". | 🔴 Open |

*Risk Register akan diperbarui seiring berjalannya iterasi perbaikan (Refaktor).*

## Tambahan Risiko Pivot (26 Mei 2026)

| Risiko | Dampak | Kemungkinan | Level | Mitigasi | Status |
|---|---:|---:|---|---|---|
| Timeout/Deadlock karena Optimistic Retry berlebihan saat traffic meledak | Tinggi | Rendah | Tinggi | Batasi maksimal retry (saat ini 5 kali). Jika gagal, kembalikan respon error eksplisit ke UI agar kasir bisa klik bayar ulang secara manual. | Open |
| Serah obat gagal karena Depo Resolver tidak disediakan oleh UI Frontend | Tinggi | Sedang | Kritis | Validasi wajib `kd_bangsal_asal` di level API. Tanpanya proses otomatis terblokir (tidak akan salah potong). | Open |

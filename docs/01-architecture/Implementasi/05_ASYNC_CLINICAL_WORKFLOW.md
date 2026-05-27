# Panduan Alur Klinis (Enterprise EMR & Async Fallback)
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

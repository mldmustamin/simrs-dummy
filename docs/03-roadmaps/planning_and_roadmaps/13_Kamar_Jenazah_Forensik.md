> **Status**: *On-going modul (Cetak Biru Masa Depan)*

Kamar Jenazah & Forensik
=========================================
**Dokumen Arsitektur & Alur Kerja**

## 1. Deskripsi Eksekutif
Pemulasaraan jenazah, sewa freezer, dan pelayanan forensik medis.

## 2. Aktor & Hak Akses
- Petugas Jenazah, Dokter Forensik

## 3. Alur Perjalanan Pasien (Patient Journey)
1. Jenazah diterima dari bangsal.
2. Jenazah dimandikan/dikafani.
3. Keluarga membayar sewa ambulans jenazah ke kasir dan membawa jenazah.

## 4. Alur Perjalanan Sistem (ERP Data Lifecycle)
- Kalkulasi sewa lemari pendingin (freezer) per 24 jam.
- Penguncian mutlak rekam medis menjadi status `Meninggal/Deceased` agar tidak bisa didaftarkan poli lagi.

## 5. Implementasi Multi-Model (Arsitektur Fallback)
- **Standar Ideal (Enterprise)**: Pencetakan Surat Kematian Digital terenkripsi QRCode.
- **Skenario Pragmatis (Fallback)**: Keluarga Mr.X tidak ditemukan. Setelah 3 hari di freezer, sistem mengirim notifikasi integrasi pelaporan ke Dinas Sosial untuk pemakaman gratis.

## 6. Titik Integrasi & Bridging Eksternal
- Disdukcapil (Pelaporan Kematian Otomatis).

## 7. Penanganan Bencana & Edge Cases
- ⚠️ **Skenario Ekstrem**: Polisi meminta Visum et Repertum. Sistem mengamankan (lock) rekam medis dari ahli waris karena berstatus Barang Bukti Hukum.

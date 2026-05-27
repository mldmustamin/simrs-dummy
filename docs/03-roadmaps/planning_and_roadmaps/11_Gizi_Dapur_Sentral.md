> **Status**: *On-going modul (Cetak Biru Masa Depan)*

Instalasi Gizi & Dapur Sentral
=========================================
**Dokumen Arsitektur & Alur Kerja**

## 1. Deskripsi Eksekutif
Manajemen nampan diet pasien dan logistik bahan makanan mentah.

## 2. Aktor & Hak Akses
- Ahli Gizi, Koki Dapur

## 3. Alur Perjalanan Pasien (Patient Journey)
1. Dapur menerima kompilasi pesanan diet (Bubur, Nasi, Rendah Garam) dari Ranap.
2. Memasak dan memporsikan ke nampan pasien berlabel barcode.
3. Distribusi menggunakan troli tertutup.

## 4. Alur Perjalanan Sistem (ERP Data Lifecycle)
- Pemotongan stok bahan basah (beras, sayur) dari Gudang Gizi harian.
- Pencegahan Fatal: Sistem langsung membunyikan alarm di layar Dapur jika pasien yang diproses memiliki rekaman `Alergi Telur`.

## 5. Implementasi Multi-Model (Arsitektur Fallback)
- **Standar Ideal (Enterprise)**: Sistem menghitung nilai kalori pasti per porsi dan melaporkannya ke EMR pasien.
- **Skenario Pragmatis (Fallback)**: Keluarga menyelundupkan makanan luar. Perawat bangsal mencatat asupan gizi eksternal sebagai anomali.

## 6. Titik Integrasi & Bridging Eksternal
- Internal ERP.

## 7. Penanganan Bencana & Edge Cases
- ⚠️ **Skenario Ekstrem**: Keracunan makanan massal. Sistem bisa men-trace batch bahan makanan mana (Supplier Sayur X) yang digunakan pada tanggal kejadian.

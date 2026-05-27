> **Status**: *On-going modul (Cetak Biru Masa Depan)*

Laundry & Manajemen Linen
=========================================
**Dokumen Arsitektur & Alur Kerja**

## 1. Deskripsi Eksekutif
Siklus pembersihan dan pengendalian infeksi linen RS (Sprei, Baju OK, Selimut).

## 2. Aktor & Hak Akses
- Petugas Laundry

## 3. Alur Perjalanan Pasien (Patient Journey)
1. Pengumpulan linen kotor (Infeksius Merah / Non-Infeksius Hitam) dari bangsal.
2. Penimbangan total (Kg) di pintu Laundry.
3. Pencucian, Penyetrikaan, Pelipatan.
4. Penyimpanan di Rak Bersih, dan didistribusikan ulang.

## 4. Alur Perjalanan Sistem (ERP Data Lifecycle)
- Sistem melacak frekuensi cuci per lembar linen menggunakan tag RFID (Mode Enterprise).
- Pemotongan stok bahan kimia laundry (Deterjen, Klorin) dari Gudang Utama.

## 5. Implementasi Multi-Model (Arsitektur Fallback)
- **Standar Ideal (Enterprise)**: Linen dilengkapi chip RFID tahan panas. Setiap melewati pintu bangsal, sistem otomatis mencatat posisi linen (Track & Trace).
- **Skenario Pragmatis (Fallback)**: Menghitung berat total (Kiloan) per bangsal dan mencatat serah terima secara manual di komputer logistik.

## 6. Titik Integrasi & Bridging Eksternal
- Logistik ERP.

## 7. Penanganan Bencana & Edge Cases
- ⚠️ **Skenario Ekstrem**: Wabah Penyakit Menular. Sistem mengunci linen dari bangsal isolasi agar masuk ke mesin cuci khusus (Infectious Washing Cycle) tanpa dicampur.

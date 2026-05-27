> **Status**: *On-going modul (Cetak Biru Masa Depan)*

IPSRS (Teknisi RS)
=========================================
**Dokumen Arsitektur & Alur Kerja**

## 1. Deskripsi Eksekutif
Sistem Helpdesk perbaikan gedung/AC dan jadwal kalibrasi alat medis bernilai miliaran.

## 2. Aktor & Hak Akses
- Mekanik, Teknisi Elektromedik

## 3. Alur Perjalanan Pasien (Patient Journey)
1. Ruangan mensubmit Tiket Kerusakan.
2. Teknisi mengambil sparepart dari gudang teknik dan mengeksekusi perbaikan.
3. Teknisi menutup tiket.

## 4. Alur Perjalanan Sistem (ERP Data Lifecycle)
- Peringatan Kalibrasi (Preventive Maintenance) untuk Ventilator/Mesin Anestesi setiap 12 bulan.
- Sistem melarang mesin yang belum dikalibrasi digunakan di modul Kamar Operasi.

## 5. Implementasi Multi-Model (Arsitektur Fallback)
- **Standar Ideal (Enterprise)**: Sistem IoT dari Genset otomatis mengirim log BBM ke ERP setiap hari.
- **Skenario Pragmatis (Fallback)**: Mati lampu, Genset utama gagal menyala 10 detik. Teknisi menerima Push Notification darurat ke HP pribadi.

## 6. Titik Integrasi & Bridging Eksternal
- ASPAK (Aplikasi Sarana Prasarana Kemenkes).

## 7. Penanganan Bencana & Edge Cases
- ⚠️ **Skenario Ekstrem**: Pipa oksigen sentral bocor. Eskalasi darurat level 1 ke Direktur Umum.

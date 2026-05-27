Instalasi Farmasi (Apotek)
=========================================
**Dokumen Arsitektur & Alur Kerja**

## 1. Deskripsi Eksekutif
Jantung pengeluaran stok. Manajemen resep, PIO, dan kalkulasi HNA+Margin.

## 2. Aktor & Hak Akses
- Apoteker, Asisten Apoteker

## 3. Alur Perjalanan Pasien (Patient Journey)
1. Menerima E-Resep. Apoteker melakukan telaah (Screening klinis).
2. Meracik puyer/salep atau menyiapkan obat jadi.
3. Validasi pembayaran (Pasien Umum).
4. Penyerahan obat dengan Pelayanan Informasi Obat (PIO).

## 4. Alur Perjalanan Sistem (ERP Data Lifecycle)
- Pessimistic Locking pada tabel `gudangbarang` untuk menghindari Race Condition stok.
- Otomatis injeksi harga `Tuslah` dan `Embalase`.

## 5. Implementasi Multi-Model (Arsitektur Fallback)
- **Standar Ideal (Enterprise)**: Sistem otomatis mengkalkulasi FEFO (First Expired First Out) dan memandu lokasi rak obat.
- **Skenario Pragmatis (Fallback)**: Jika stok komputer 0 tapi fisik ada, sistem mengizinkan 'Force Dispense' dengan mencatat minus stok sementara untuk diperbaiki saat Stock Opname.

## 6. Titik Integrasi & Bridging Eksternal
- E-Katalog Kemenkes, SIPNAP.

## 7. Penanganan Bencana & Edge Cases
- ⚠️ **Skenario Ekstrem**: Pasien alergi obat yang diresepkan. Apoteker me-reject E-Resep, sistem mengirim notif ke EMR Poli untuk penggantian obat.

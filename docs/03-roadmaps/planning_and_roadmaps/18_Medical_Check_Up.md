> **Status**: *On-going modul (Cetak Biru Masa Depan)*

Medical Check Up (MCU)
=========================================
**Dokumen Arsitektur & Alur Kerja**

## 1. Deskripsi Eksekutif
Pelayanan preventif berpaket (massal/korporat).

## 2. Aktor & Hak Akses
- Petugas MCU, Dokter Spesialis

## 3. Alur Perjalanan Pasien (Patient Journey)
1. Pendaftaran Paket (misal: Paket Eksekutif Jantung).
2. Sistem me-routing pasien untuk antre ke Poli Jantung, Lab, Rontgen, dan Treadmill.
3. Sistem mengkompilasi seluruh hasil dari berbagai unit menjadi 1 Buku Laporan PDF.
4. Dokter MCU menarik kesimpulan akhir (*Fit to Work*).

## 4. Alur Perjalanan Sistem (ERP Data Lifecycle)
- Sistem mencegah Modul Kasir menagihkan biaya per item, melainkan menagihkan Harga Paket.
- Kalkulasi diskon kolektif untuk Karyawan Perusahaan (Corporate Billing).

## 5. Implementasi Multi-Model (Arsitektur Fallback)
- **Standar Ideal (Enterprise)**: Buku Hasil MCU bisa diunduh via Portal Pasien / Mobile App RS oleh pasien dari rumah.
- **Skenario Pragmatis (Fallback)**: Perusahaan BUMN X meminta format PDF laporan diubah secara spesifik. ERP menyediakan Template Engine (HTML to PDF) untuk kustomisasi.

## 6. Titik Integrasi & Bridging Eksternal
- Lab & Radiologi.

## 7. Penanganan Bencana & Edge Cases
- ⚠️ **Skenario Ekstrem**: Ditemukan penyakit kritis (misal: Tumor) saat MCU. Pasien di-switch statusnya secara sistem menjadi Pasien Rawat Jalan Kuratif (BPJS) untuk ditindaklanjuti.

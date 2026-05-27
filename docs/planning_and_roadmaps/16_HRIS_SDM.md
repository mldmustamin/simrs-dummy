> **Status**: *On-going modul (Cetak Biru Masa Depan)*

HRIS & SDM (Kepegawaian)
=========================================
**Dokumen Arsitektur & Alur Kerja**

## 1. Deskripsi Eksekutif
Penjadwalan shift, absensi, KPI, payroll, dan Jasa Medis (Remunerasi Dokter).

## 2. Aktor & Hak Akses
- HRD, Dokter, Perawat

## 3. Alur Perjalanan Pasien (Patient Journey)
1. Fingerprint ditarik otomatis.
2. Penyusunan Shift Perawat Bulanan.
3. Hitung Payroll (Gaji Pokok + Tunjangan - Pajak).
4. Hitung Jasa Pelayanan (Jaspel) dari tindakan klinis ERP.

## 4. Alur Perjalanan Sistem (ERP Data Lifecycle)
- Kalkulasi `Fee for Service` yang sangat kompleks berdasarkan proporsi jasa Asisten vs Operator saat pembedahan.
- Integrasi pemotongan BPJS Ketenagakerjaan dan Kesehatan.

## 5. Implementasi Multi-Model (Arsitektur Fallback)
- **Standar Ideal (Enterprise)**: Absensi berbasis Face Recognition tersinkron GPS di HP (Mobile App).
- **Skenario Pragmatis (Fallback)**: Fingerprint rusak. Admin bangsal mengeklik tombol 'Hadir' secara manual untuk staf shift malam.

## 6. Titik Integrasi & Bridging Eksternal
- Mesin Absensi, Pajak PPh 21.

## 7. Penanganan Bencana & Edge Cases
- ⚠️ **Skenario Ekstrem**: Dokter menuntut transparansi Jaspel. ERP menyediakan Dashboard khusus Dokter untuk melihat rincian pasien mana saja yang sudah ia layani beserta nominal jasanya secara transparan.

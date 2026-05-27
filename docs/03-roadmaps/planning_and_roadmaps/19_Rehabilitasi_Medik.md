> **Status**: *On-going modul (Cetak Biru Masa Depan)*

Rehabilitasi Medik (Fisioterapi)
=========================================
**Dokumen Arsitektur & Alur Kerja**

## 1. Deskripsi Eksekutif
Manajemen sesi terapi berulang dan kuota asuransi.

## 2. Aktor & Hak Akses
- Fisioterapis, Dokter KFR

## 3. Alur Perjalanan Pasien (Patient Journey)
1. Dokter membuat program terapi (misal: 6x kunjungan).
2. Fisioterapis melayani pasien setiap datang.
3. Sistem mencatat kedatangan 1/6, 2/6, dst.

## 4. Alur Perjalanan Sistem (ERP Data Lifecycle)
- Pemblokiran sistem (*Hard Stop*) jika pasien datang ke-7 kalinya sementara asuransinya hanya meng-cover 6 kali per siklus rujukan.

## 5. Implementasi Multi-Model (Arsitektur Fallback)
- **Standar Ideal (Enterprise)**: Sensor gerak/IoT merekam kemajuan sudut tekuk lutut pasien ke dalam ERP.
- **Skenario Pragmatis (Fallback)**: Sistem peringatan sisa kuota (Warning) pada kunjungan ke-5 agar pasien siap-siap memperpanjang rujukan.

## 6. Titik Integrasi & Bridging Eksternal
- Internal ERP.

## 7. Penanganan Bencana & Edge Cases
- ⚠️ **Skenario Ekstrem**: Pasien menyerah di sesi ke-3 dan tidak pernah datang lagi. Sistem otomatis melakukan Auto-Discharge setelah 30 hari tidak ada aktivitas.

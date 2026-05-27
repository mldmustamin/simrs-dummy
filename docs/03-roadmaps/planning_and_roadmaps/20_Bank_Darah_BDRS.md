> **Status**: *On-going modul (Cetak Biru Masa Depan)*

Bank Darah Rumah Sakit (BDRS)
=========================================
**Dokumen Arsitektur & Alur Kerja**

## 1. Deskripsi Eksekutif
Manajemen stok kantong darah (PRC, TC, FFP) dan Uji Silang Serasi.

## 2. Aktor & Hak Akses
- Petugas Lab/BDRS

## 3. Alur Perjalanan Pasien (Patient Journey)
1. Dokter Ranap memesan kantong darah.
2. BDRS menerima permintaan, mengambil sampel darah pasien, melakukan Crossmatch.
3. Menyiapkan kantong darah cocok (Compatible).
4. Menyerahkan ke perawat ruangan.

## 4. Alur Perjalanan Sistem (ERP Data Lifecycle)
- Stok kantong darah dikelola per Golongan Darah dan Rhesus.
- Sistem menagihkan biaya Pengolahan Darah (Bukan biaya beli darah) ke modul Kasir.

## 5. Implementasi Multi-Model (Arsitektur Fallback)
- **Standar Ideal (Enterprise)**: Kulkas penyimpan darah dilengkapi sensor suhu IoT. Alarm menyala di ERP jika suhu kulkas naik membahayakan stok darah.
- **Skenario Pragmatis (Fallback)**: Kekosongan stok darah RS. Sistem menerbitkan form Rujukan Darah PMI untuk diserahkan keluarga pasien ke PMI Kota.

## 6. Titik Integrasi & Bridging Eksternal
- Sistem PMI (Jika tersedia).

## 7. Penanganan Bencana & Edge Cases
- ⚠️ **Skenario Ekstrem**: Reaksi Transfusi. Pasien gatal/syok saat ditransfusi. EMR memiliki modul Pelaporan Insiden Transfusi Darah (Hemovigilance) untuk investigasi BDRS.

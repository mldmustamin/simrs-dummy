Kamar Operasi (OK) & CSSD
=========================================
**Dokumen Arsitektur & Alur Kerja**

## 1. Deskripsi Eksekutif
Manajemen penjadwalan pembedahan, pencatatan BHP, dan sterilisasi alat.

## 2. Aktor & Hak Akses
- Dokter Bedah, Perawat Omloop, Petugas CSSD

## 3. Alur Perjalanan Pasien (Patient Journey)
1. Asesmen Pra-Bedah oleh Anestesi.
2. Operasi berjalan (Intra). Perawat mencatat tiap benang dan kassa yang dipakai.
3. Pasien dipindah ke Recovery Room (RR).
4. Alat kotor dikirim ke CSSD untuk dicuci dan di-Autoclave.

## 4. Alur Perjalanan Sistem (ERP Data Lifecycle)
- Pemotongan inventori BHP secara real-time.
- Sistem CSSD men-generate barcode Expired Date sterilisasi per instrumen set.

## 5. Implementasi Multi-Model (Arsitektur Fallback)
- **Standar Ideal (Enterprise)**: Layar monitor besar di ruang tunggu menampilkan status operasi (Persiapan -> Operasi -> Pemulihan) layaknya bandara.
- **Skenario Pragmatis (Fallback)**: Operasi memakan waktu lebih lama dari jadwal (Pendarahan Hebat). Sistem meng-hold dan menunda otomatis jadwal bedah berikutnya.

## 6. Titik Integrasi & Bridging Eksternal
- Sistem Antrean Operasi RS.

## 7. Penanganan Bencana & Edge Cases
- ⚠️ **Skenario Ekstrem**: Mesin Autoclave CSSD rusak. Operasi non-cito dibatalkan sistem otomatis karena set steril tidak tersedia.

Instalasi Gawat Darurat (IGD) & Triase
=========================================
**Dokumen Arsitektur & Alur Kerja**

## 1. Deskripsi Eksekutif
Penanganan nyawa. Membutuhkan sistem yang tidak memblokir tindakan di saat kritis.

## 2. Aktor & Hak Akses
- Dokter Jaga IGD, Perawat Triase

## 3. Alur Perjalanan Pasien (Patient Journey)
1. Pasien masuk. Triase (<2 menit): Merah, Kuning, Hijau, Hitam.
2. Pasien prioritas masuk ruang resusitasi tanpa perlu daftar.
3. Tindakan *Life Saving* dan pemberian obat emergency dari kotak depo.

## 4. Alur Perjalanan Sistem (ERP Data Lifecycle)
- Bypass validasi kasir. Tagihan menumpuk secara asinkronus.
- Virtual mutasi obat dari `Gudang_IGD`.

## 5. Implementasi Multi-Model (Arsitektur Fallback)
- **Standar Ideal (Enterprise)**: Integrasi alat EKG langsung ke EMR Dokter.
- **Skenario Pragmatis (Fallback)**: Verbal Order (Resep Lisan) diakomodasi. Perawat menyuntik dulu, form resep di-approve dokter 24 jam kemudian (Retrospektif).

## 6. Titik Integrasi & Bridging Eksternal
- SPGDT Kemenkes.

## 7. Penanganan Bencana & Edge Cases
- ⚠️ **Skenario Ekstrem**: Mass Casualty (Kecelakaan Masal). Sistem memiliki fitur 'Batch Admit' Mr.X 1 hingga Mr.X 20.

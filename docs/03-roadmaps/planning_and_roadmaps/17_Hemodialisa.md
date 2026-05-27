> **Status**: *On-going modul (Cetak Biru Masa Depan)*

Hemodialisa (Cuci Darah)
=========================================
**Dokumen Arsitektur & Alur Kerja**

## 1. Deskripsi Eksekutif
Layanan siklik pasien kronis yang memerlukan booking mesin jangka panjang.

## 2. Aktor & Hak Akses
- Perawat HD, Dokter KGH

## 3. Alur Perjalanan Pasien (Patient Journey)
1. Pasien datang sesuai jadwal rutin (Booking Slot Mesin).
2. Pemeriksaan TTV Pre-HD.
3. Mesin menyala (Intra-HD), pemberian Heparin.
4. Penyelesaian (Post-HD), penjadwalan bulan depan.

## 4. Alur Perjalanan Sistem (ERP Data Lifecycle)
- Sistem menjadwalkan ulang 8 sesi kunjungan secara masal (Bulk Scheduling).
- Sistem mengingatkan masa aktif rujukan BPJS yang habis tiap 3 bulan.

## 5. Implementasi Multi-Model (Arsitektur Fallback)
- **Standar Ideal (Enterprise)**: Mesin Hemodialisa mengirim data *Ultrafiltration Rate* langsung ke sistem.
- **Skenario Pragmatis (Fallback)**: Rujukan BPJS habis masa berlaku di tengah siklus. Sistem memasukkan pasien ke mode Penjaminan Sementara sampai keluarga mengurus kertas rujukan baru ke Puskesmas.

## 6. Titik Integrasi & Bridging Eksternal
- Internal ERP.

## 7. Penanganan Bencana & Edge Cases
- ⚠️ **Skenario Ekstrem**: Pasien Drop (Hipotensi) saat dicuci darah. Tindakan Emergency Stop dieksekusi, pasien dialihkan ke ICU tanpa perlu daftar dari awal.

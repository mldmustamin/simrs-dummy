Poliklinik (Rawat Jalan)
=========================================
**Dokumen Arsitektur & Alur Kerja**

## 1. Deskripsi Eksekutif
Modul tempat dokter spesialis dan perawat melakukan asesmen awal, anamnesis, dan penentuan terapi.

## 2. Aktor & Hak Akses
- Perawat Poli, Dokter Spesialis DPJP

## 3. Alur Perjalanan Pasien (Patient Journey)
1. Perawat memanggil pasien, melakukan ukur TTV (Tensi, Suhu, Berat) dan Anamnesis.
2. Dokter memanggil pasien, membuka EMR, memeriksa riwayat historis.
3. Dokter menginput Diagnosa Utama (ICD-10) dan Tindakan (ICD-9CM).
4. Dokter meresepkan obat secara elektronik (E-Resep) atau Order Lab/Rad (CPOE).

## 4. Alur Perjalanan Sistem (ERP Data Lifecycle)
- Merekam `pemeriksaan_ralan`.
- Mengirim event `Poli.Selesai` yang merilis harga layanan ke `Kasir`.
- Membuka kunci antrean di Farmasi/Lab.

## 5. Implementasi Multi-Model (Arsitektur Fallback)
- **Standar Ideal (Enterprise)**: Dokter mengisi SOAP secara komplit saat pasien duduk di depan meja. Sistem memberi peringatan interaksi obat secara real-time.
- **Skenario Pragmatis (Fallback)**: Kekacauan antrean. Dokter hanya menginput diagnosis singkat. SOAP diisi retrospektif (mundur waktu) 2 jam kemudian dengan sistem mencatat `created_at` asli.

## 6. Titik Integrasi & Bridging Eksternal
- SATUSEHAT (Kunjungan Rawat Jalan).

## 7. Penanganan Bencana & Edge Cases
- ⚠️ **Skenario Ekstrem**: Salah input diagnosis setelah di-TTE. Fitur Addendum diaktifkan.

# Workflow Modul Rehabilitasi Medik & Fisioterapi
> **Status**: *On-going modul*

## 1. Deskripsi Umum
Pelayanan fisioterapi, terapi okupasi, dan terapi wicara yang sifatnya berseri (beberapa kali kunjungan untuk satu rujukan).

## 2. Aktor Terlibat
- Fisioterapis
- Dokter Spesialis KFR

## 3. Alur Kerja (Ideal & Fallback)
1. **Evaluasi Awal:** Dokter Spesialis KFR menentukan program terapi (misal: 6 kali kunjungan TENS).
2. **Pelaksanaan Terapi:** Fisioterapis mengeksekusi terapi per sesi.
3. **Protokol Klaim:** ERP akan otomatis mengingatkan jika sesi terapi pasien BPJS sudah melebihi batas kuota bulanan.

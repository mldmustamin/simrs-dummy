Rekam Medis & Casemix
=========================================
**Dokumen Arsitektur & Alur Kerja**

## 1. Deskripsi Eksekutif
Back-office untuk audit kelengkapan berkas, koding ICD, dan pengajuan klaim piutang BPJS.

## 2. Aktor & Hak Akses
- Koder, Petugas Casemix BPJS

## 3. Alur Perjalanan Pasien (Patient Journey)
1. Pasien pulang. EMR dikunci.
2. Koder menganalisa kelengkapan (KLPCM).
3. Pemberian kode ICD-10 dan ICD-9CM.
4. Grouping INA-CBG untuk menarik nilai tarif klaim.
5. Pemberkasan (Penggabungan SEP, Resume Medis, Rincian Kasir) menjadi PDF Klaim.

## 4. Alur Perjalanan Sistem (ERP Data Lifecycle)
- Pemblokiran klaim jika EMR belum memiliki Tanda Tangan Elektronik dokter.
- Jurnal otomatis: Piutang Klaim (Debet).

## 5. Implementasi Multi-Model (Arsitektur Fallback)
- **Standar Ideal (Enterprise)**: AI Coding. Sistem menyarankan kode ICD otomatis berdasarkan teks bahasa alami dari SOAP dokter.
- **Skenario Pragmatis (Fallback)**: Klaim di-pending oleh BPJS. Petugas Casemix memiliki form Dispute untuk melampirkan alasan sanggahan.

## 6. Titik Integrasi & Bridging Eksternal
- INA-CBG E-Klaim Kemenkes.

## 7. Penanganan Bencana & Edge Cases
- ⚠️ **Skenario Ekstrem**: Dokter tidak mau mengisi EMR lengkap. Sistem mengaktifkan sanksi otomatis: Menahan pencairan Jasa Medis (Fee for Service) dokter tersebut bulan ini.

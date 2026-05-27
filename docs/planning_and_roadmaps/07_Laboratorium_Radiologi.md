Laboratorium & Radiologi
=========================================
**Dokumen Arsitektur & Alur Kerja**

## 1. Deskripsi Eksekutif
Penunjang medis. Pemrosesan sampel/scan dan pelaporan hasil (Expertise).

## 2. Aktor & Hak Akses
- Analis Lab, Radiografer, Dokter Spesialis

## 3. Alur Perjalanan Pasien (Patient Journey)
1. Pasien menyerahkan barcode CPOE.
2. Pengambilan spesimen darah / Pemosisian pasien rontgen.
3. Analisa mesin.
4. Dokter merilis hasil bacaan (Expertise).

## 4. Alur Perjalanan Sistem (ERP Data Lifecycle)
- Integrasi LIS (Laboratory Information System) - nilai darah masuk otomatis ke kolom ERP.
- Integrasi PACS - Gambar DICOM rontgen bisa dibuka langsung dari EMR dokter perujuk.

## 5. Implementasi Multi-Model (Arsitektur Fallback)
- **Standar Ideal (Enterprise)**: Fully paperless. Hasil muncul instan di layar HP/Tablet dokter DPJP.
- **Skenario Pragmatis (Fallback)**: Alat Lab rusak. Pasien dikirim ke lab luar (Rujukan Parsial), hasil luar di-scan PDF dan di-upload ke sistem sebagai Attachment.

## 6. Titik Integrasi & Bridging Eksternal
- SATUSEHAT (Kirim Hasil Lab/Radiologi).

## 7. Penanganan Bencana & Edge Cases
- ⚠️ **Skenario Ekstrem**: Hasil Kritis (Klaim Panik). Darah Hb < 5. Alarm menyala berkedip merah di EMR IGD.

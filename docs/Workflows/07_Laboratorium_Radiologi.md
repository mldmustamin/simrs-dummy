# Workflow Modul Laboratorium & Radiologi
## 1. Deskripsi Umum
Penunjang medis. Menerima order (CPOE) dari dokter, memproses sampel/gambar, dan mengirim balik hasil expertise.

## 2. Aktor Terlibat
- Analis Lab / Radiografer
- Dokter Spesialis Patologi Klinik / Radiologi

## 3. Alur Kerja (Ideal & Fallback)
1. **Penerimaan Order:** Order E-Lab/Radiologi muncul di layar.
2. **Pengambilan Spesimen / Scan:** Petugas mengambil darah atau memposisikan pasien rontgen.
3. **Proses Alat (LIS/PACS):**
   - *Lab:* Mesin LIS mengirim hasil numerik otomatis ke ERP via protokol HL7.
   - *Radiologi:* Mesin MRI/CT-Scan mengirim gambar DICOM ke server PACS.
4. **Verifikasi / Expertise:** Dokter spesialis membaca hasil dan menuliskan kesimpulan (*Expertise*).
5. **Release Hasil:** Hasil dirilis. Indikator merah/kritis langsung menyala di layar komputer dokter perujuk (Poli/Ranap).

## 4. Trigger & Integrasi
- **Menembak Event:** `Penunjang.HasilRilis` -> Memicu notifikasi *Push/Websocket* ke dokter perujuk, memicu penambahan tagihan ke Kasir.
- **Bridging:** SATUSEHAT (Hasil Lab/Radiologi spesifik).

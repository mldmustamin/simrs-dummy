# Workflow Modul Kamar Operasi (OK) & CSSD
## 1. Deskripsi Umum
Penjadwalan operasi yang ketat, penggunaan BHP dinamis, hingga sterilisasi alat medis.

## 2. Aktor Terlibat
- Dokter Bedah & Anestesi
- Perawat Instrumen
- Staf CSSD

## 3. Alur Kerja (Ideal & Fallback)
1. **Penjadwalan Operasi:** Order dari Ranap/Poli masuk. Sistem memblokir *slot* waktu Kamar Operasi.
2. **Pra-Operasi:** Dokter Anestesi mengisi EMR Asesmen Pra-Anestesi.
3. **Intra-Operasi (BHP Dinamis):** Perawat omloop mencatat secara *real-time* setiap benang, kassa, atau alat sekali pakai yang digunakan selama operasi. Tagihan berjalan dinamis.
4. **Pasca-Operasi:** Pasien diobservasi di Recovery Room (RR). Laporan Operasi diketik oleh dokter bedah.
5. **Siklus CSSD:** Alat operasi berdarah/kotor dikirim ke CSSD. CSSD mencuci, men-sterilisasi (Autoclave), menempel *barcode* steril, dan mendistribusikan kembali ke OK.

## 4. Trigger & Integrasi
- **Menembak Event:** `OK.OperasiSelesai` -> Memicu Ranap untuk menyiapkan penerimaan kembali pasien, memicu Kasir untuk memisahkan *fee* Jasa Bedah, Asisten, dan Anestesi.

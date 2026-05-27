# Workflow Modul Manajemen Rekam Medis (Filing & Casemix)
## 1. Deskripsi Umum
Back-office pengolahan resume medis pasca pasien pulang untuk keperluan statistik Kemenkes dan penagihan INA-CBG.

## 2. Aktor Terlibat
- Koder Medis
- Petugas Casemix BPJS

## 3. Alur Kerja (Ideal & Fallback)
1. **Analisa Kelengkapan (KLPCM):** Petugas mengecek apakah dokter sudah melengkapi TTE dan diagnosa. Jika belum, sistem memblokir klaim dan mengirim notifikasi teguran ke dokter.
2. **Koding Medis:** Koder membaca EMR dan memberikan kode akhir ICD-10 (Penyakit) dan ICD-9CM (Prosedur).
3. **Casemix / Grouping INA-CBG:** Petugas mengirim kode tersebut ke server INA-CBG untuk mendapatkan *Tarif Paket BPJS*.
4. **Klaim Piutang:** Tagihan pasien-pasien BPJS yang sudah lengkap dikonsolidasikan dan dikirim sebagai Piutang BPJS ke dalam sistem Akuntansi.

## 4. Trigger & Integrasi
- **Menembak Event:** `Casemix.KlaimFinal` -> Memicu Akuntansi untuk mengakui Piutang BPJS dan mencatat selisih tarif riil RS vs Tarif INA-CBG sebagai laba/rugi asuransi.
- **Bridging:** E-Klaim INA-CBG Kemenkes.

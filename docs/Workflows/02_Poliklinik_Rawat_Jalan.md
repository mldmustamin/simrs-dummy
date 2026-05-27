# Workflow Modul Poliklinik (Rawat Jalan)
## 1. Deskripsi Umum
Tempat dilakukannya Asuhan Keperawatan awal dan Pemeriksaan Medis (SOAP) oleh dokter spesialis.

## 2. Aktor Terlibat
- Perawat Poli
- Dokter DPJP Poli

## 3. Alur Kerja (Ideal & Fallback)
1. **Pemanggilan Antrean:** Perawat memanggil nomor antrean.
2. **Kajian Awal Perawat:** Perawat mengukur TTV (Tensi, Suhu, Nadi, Berat, Tinggi) dan anamnesis keluhan utama. Disimpan ke EMR Perawat.
3. **Pemeriksaan Dokter (SOAP):**
   - Dokter memanggil pasien. Membuka EMR, melihat riwayat kunjungan sebelumnya.
   - *Mode Pragmatis:* Jika dokter sangat sibuk, pengisian SOAP bisa dilakukan *retrospektif* (jam input di-set mundur).
4. **Order Penunjang (CPOE):** Dokter memesan Darah Rutin (Modul Lab) atau Rontgen (Modul Radiologi) via sistem tanpa kertas pengantar.
5. **E-Resep:** Dokter memasukkan obat ke dalam sistem. *Warning* akan muncul jika pasien alergi obat tersebut.
6. **Closing Poli:** Dokter menyelesaikan layanan. *Trigger* status antrean menjadi "Selesai".

## 4. Trigger & Integrasi
- **Menembak Event:** `Poli.PeriksaSelesai` -> Memicu Apotek (memunculkan E-Resep), memicu Kasir (menambah tagihan tindakan/jasa dokter).
- **Bridging:** SATUSEHAT (Resume Medis Rawat Jalan).

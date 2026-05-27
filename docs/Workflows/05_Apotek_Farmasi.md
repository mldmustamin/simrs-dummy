# Workflow Modul Instalasi Farmasi (Apotek)
## 1. Deskripsi Umum
Manajemen peracikan resep, pengurangan stok FIFO/FEFO, kalkulasi margin, dan penyerahan obat ke pasien.

## 2. Aktor Terlibat
- Apoteker
- Asisten Apoteker

## 3. Alur Kerja (Ideal & Fallback)
1. **Penerimaan E-Resep:** Notifikasi muncul di *dashboard* Apotek saat dokter Poli/IGD menekan tombol "Kirim Resep".
2. **Telaah Resep:** Apoteker memvalidasi dosis dan interaksi obat.
3. **Kalkulasi Biaya:** Sistem otomatis menghitung harga (HNA + Margin) + Tuslah + Embalase.
4. **Penyiapan & Racik:** Obat disiapkan/diracik. Stok virtual otomatis berkurang (Pessimistic Lock).
5. **Validasi Kasir (Hanya Pasien Umum):** Status obat "Menunggu Pembayaran". Setelah Lunas di kasir, status berubah menjadi "Siap Diserahkan". (Pasien BPJS langsung ke langkah 6).
6. **Penyerahan Obat (PIO):** Apoteker memanggil pasien, memberikan edukasi obat, lalu menekan tombol "Diserahkan".

## 4. Trigger & Integrasi
- **Menembak Event:** `Farmasi.ResepDiserahkan` -> Memicu Akuntansi (HPP & Pengurangan Persediaan), mengunci EMR Dokter.
- **Bridging:** Laporan SIPNAP (Narkotika/Psikotropika).

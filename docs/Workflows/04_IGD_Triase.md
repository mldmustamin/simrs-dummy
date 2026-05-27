# Workflow Modul Instalasi Gawat Darurat (IGD)
## 1. Deskripsi Umum
Penanganan pasien dengan prioritas kecepatan tinggi. Melibatkan Triase dan tindakan *Life-Saving*.

## 2. Aktor Terlibat
- Perawat Triase
- Dokter Jaga IGD

## 3. Alur Kerja (Ideal & Fallback)
1. **Kedatangan & Triase:** Pasien datang, dinilai < 2 menit (Merah/Kuning/Hijau/Hitam). Input ke EMR Triase.
2. **Fast-Track Pendaftaran:** Pasien Merah langsung masuk ruang Resusitasi. Pendaftaran dilakukan paralel oleh keluarga.
3. **Verbal Order (Darurat):** Dokter memberikan perintah lisan "Suntik Epinephrine 1mg". Perawat mengeksekusi tanpa menunggu input EMR. Obat dikeluarkan langsung dari Depo IGD (Emergency Kit).
4. **Validasi Retrospektif:** Setelah pasien stabil, Dokter menginput order obat tersebut secara mundur (*Retrospektif*) di EMR untuk keperluan audit dan *billing*.
5. **Keputusan Medis:** Pasien Dirawat Inap, Dirujuk ke RS lain, atau Pulang.

## 4. Trigger & Integrasi
- **Menembak Event:** `IGD.MutasiRanap` -> Memicu pemesanan Bed di modul Rawat Inap.
- **Bridging:** SPGDT (Sistem Penanggulangan Gawat Darurat Terpadu).

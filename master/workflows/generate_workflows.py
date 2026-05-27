import os

folder_path = "/home/gudang-data-kantor/simrs-web/docs/Workflows"
os.makedirs(folder_path, exist_ok=True)

workflows = {
    "01_Pendaftaran_Admisi.md": """# Workflow Modul Pendaftaran & Admisi
## 1. Deskripsi Umum
Modul ini adalah pintu masuk pertama pasien. Bertanggung jawab mencatat demografi, mencetak RM baru, mendistribusikan antrean ke Poli/IGD, dan menerbitkan SEP BPJS.

## 2. Aktor Terlibat
- Petugas Loket Pendaftaran
- Pasien / Keluarga Pasien
- KiosK Mandiri (Self-Service)

## 3. Alur Kerja (Ideal & Fallback)
1. **Identifikasi:** Pasien menyerahkan KTP/BPJS.
2. **Pencarian RM:** Sistem memvalidasi apakah NIK/No.BPJS sudah terdaftar. Jika belum, *Create RM Baru*.
3. **Pilih Layanan:** Petugas memilih Poli Tujuan dan Dokter.
4. **Validasi Finansial:**
   - *Tunai:* Generate tagihan karcis/pendaftaran awal di sistem Kasir.
   - *BPJS (Mode Ideal):* Tarik rujukan dari V-Claim, terbitkan SEP instan.
   - *BPJS (Mode Pragmatis):* Jika V-Claim timeout, bypass SEP, teruskan pendaftaran dengan `no_rawat` lokal, masukkan request SEP ke `Background Job`.
5. **Cetak Bukti:** Cetak karcis antrean Poli dan Tracer/Lembar Poli untuk Rekam Medis fisik (jika masih Hybrid).

## 4. Trigger & Integrasi
- **Menembak Event:** `Pendaftaran.Selesai` -> Memicu modul Poli (menambah daftar antrean) dan modul Kasir (membuka invoice baru).
- **Bridging:** V-Claim (SEP), Dukcapil (NIK).
""",
    
    "02_Poliklinik_Rawat_Jalan.md": """# Workflow Modul Poliklinik (Rawat Jalan)
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
""",
    
    "03_Rawat_Inap_Bangsal.md": """# Workflow Modul Rawat Inap (Bangsal)
## 1. Deskripsi Umum
Modul paling dinamis untuk manajemen bed, asuhan keperawatan 24/7 (SBAR, CPPT), pemberian obat (E-MAR), dan visite dokter.

## 2. Aktor Terlibat
- Kepala Ruangan
- Perawat Pelaksana (Shift)
- Dokter DPJP
- Petugas Gizi (Dietisien)

## 3. Alur Kerja (Ideal & Fallback)
1. **Admisi Ranap:** Pasien ditransfer dari IGD/Poli. Pemilihan Bed di modul Bed Management. Status kasur berubah menjadi `DITEMPATI`.
2. **Asesmen Awal & CPPT:** Perawat melakukan pengkajian awal. Semua entri dokter, perawat, dan ahli gizi digabungkan dalam satu *Timeline* (CPPT).
3. **Pemberian Obat (E-MAR):** Perawat menscan *barcode* obat dan *barcode* gelang pasien sebelum menyuntik untuk memastikan 7 Benar Obat.
4. **Visite Dokter:** Dokter menginput instruksi medis harian.
5. **Auto-Billing (Midnight Census):** Pada jam 00:00, ERP menagihkan biaya kamar otomatis.
6. **Discharge Planning:** Dokter menyatakan Boleh Pulang. Status bed berubah `DIRESERVE CLEANING`.

## 4. Trigger & Integrasi
- **Menembak Event:** `Ranap.PasienPulang` -> Memicu CSSD/Cleaning Service, memicu Kasir untuk *Closing Billing*.
- **Bridging:** SIRANAP Kemenkes (Ketersediaan Bed Real-time).
""",
    
    "04_IGD_Triase.md": """# Workflow Modul Instalasi Gawat Darurat (IGD)
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
""",
    
    "05_Apotek_Farmasi.md": """# Workflow Modul Instalasi Farmasi (Apotek)
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
""",
    
    "06_Kasir_Billing.md": """# Workflow Modul Kasir & Billing
## 1. Deskripsi Umum
Konsolidasi seluruh biaya layanan pasien (Tindakan, Bed, Obat, Lab) menjadi satu *invoice* terpusat.

## 2. Aktor Terlibat
- Petugas Kasir Sentral
- Administrasi Keuangan

## 3. Alur Kerja (Ideal & Fallback)
1. **Pengumpulan Biaya (Auto-Aggregation):** Sistem mengumpulkan seluruh biaya dari Poli, Lab, Apotek, dan Ranap secara *real-time* tanpa perlu di-entri ulang oleh Kasir.
2. **Validasi Final:** Kasir mengecek rincian tagihan akhir.
3. **Pembayaran:**
   - Pembayaran dilakukan via Tunai / EDC / QRIS / Transfer.
   - *Mode BPJS:* Tagihan dikalkulasi nol rupiah untuk pasien (diklaim ke INA-CBG). Jika ada naik kelas VIP, sistem menghitung *Cost Sharing* otomatis.
4. **Emergency Override (Mode Pragmatis):** Jika keluarga tidak bisa bayar, Direktur Keuangan dapat memasukkan *PIN Override* agar pasien boleh pulang (Piutang / Bad Debt).
5. **Cetak Bukti & Lunas:** Kuitansi dicetak, status pasien ditutup.

## 4. Trigger & Integrasi
- **Menembak Event:** `Kasir.PembayaranLunas` -> Memicu Modul Jurnal Akuntansi (Debet Kas, Kredit Pendapatan), melepas *lock* penahanan dokumen rekam medis.
""",
    
    "07_Laboratorium_Radiologi.md": """# Workflow Modul Laboratorium & Radiologi
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
""",
    
    "08_Kamar_Operasi_CSSD.md": """# Workflow Modul Kamar Operasi (OK) & CSSD
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
""",
    
    "09_Logistik_Gudang.md": """# Workflow Modul Gudang Logistik (Supply Chain)
## 1. Deskripsi Umum
Rantai pasok (pembelian, penerimaan, dan distribusi) obat dan alat medis ke seluruh rumah sakit.

## 2. Aktor Terlibat
- Kepala Gudang
- Staf Logistik / Purchasing

## 3. Alur Kerja (Ideal & Fallback)
1. **Purchase Request (PR):** Depo/Poli meminta barang yang mulai menipis.
2. **Purchase Order (PO):** Purchasing menerbitkan PO ke Vendor/PBF.
3. **Goods Receipt (Penerimaan):** Barang tiba. Staf gudang menginput jumlah, Harga Beli, Nomor Batch, dan Tanggal Kadaluarsa (Expired Date). Stok Utama bertambah.
4. **Distribusi / Mutasi:** Stok didistribusikan ke depo apotek Ranap/IGD.
5. **Stock Opname:** Penyesuaian stok sistem dengan stok fisik bulanan (pencatatan barang hilang/rusak).

## 4. Trigger & Integrasi
- **Menembak Event:** `Logistik.PenerimaanSelesai` -> Memicu Modul Hutang Dagang (A/P) di Akuntansi, meng-update HPP (Harga Pokok Penjualan) dengan kalkulasi *Moving Average* atau FIFO.
""",
    
    "10_Rekam_Medis_Casemix.md": """# Workflow Modul Manajemen Rekam Medis (Filing & Casemix)
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
"""
}

for filename, content in workflows.items():
    file_path = os.path.join(folder_path, filename)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

print(f"Berhasil membuat 10 dokumen Workflow di dalam {folder_path}.")

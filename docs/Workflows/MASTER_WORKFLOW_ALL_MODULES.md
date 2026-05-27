# MASTER WORKFLOW: Seluruh Modul ERP
> **Tujuan**: Dokumen gabungan dari ke-22 modul utama dan pendukung rumah sakit untuk mempermudah pembacaan secara menyeluruh (Buku Besar Workflow).

# Workflow Modul Pendaftaran & Admisi
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


---

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


---

# Workflow Modul Rawat Inap (Bangsal)
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


---

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


---

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


---

# Workflow Modul Kasir & Billing
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


---

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


---

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


---

# Workflow Modul Gudang Logistik (Supply Chain)
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


---

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


---

# Workflow Modul Instalasi Gizi & Dapur Sentral
> **Status**: *On-going modul*

## 1. Deskripsi Umum
Memastikan asupan gizi pasien rawat inap sesuai dengan instruksi klinis dokter, mencatat pemakaian bahan mentah dapur harian, serta melacak alergi makanan.

## 2. Aktor Terlibat
- Ahli Gizi (Dietisien)
- Koki / Petugas Dapur RS

## 3. Alur Kerja (Ideal & Fallback)
1. **Penerimaan Order Diet:** Sistem menarik instruksi diet dari EMR Rawat Inap secara *real-time*.
2. **Kompilasi Kebutuhan (Pagi/Siang/Sore):** ERP menghitung otomatis total porsi Bubur, Nasi, Diet Rendah Garam, dll untuk satu rumah sakit.
3. **Pencetakan Barcode Nampan:** Nampan makanan dilabeli *barcode* yang berisi nama pasien, bangsal, dan peringatan alergi (misal: "Alergi Udang").
4. **Distribusi:** Makanan diantar ke bangsal.
5. **Inventaris Dapur:** Pengurangan stok bahan basah dan kering di Gudang Gizi.

## 4. Trigger & Integrasi
- **Menembak Event:** `Gizi.OrderSelesai`.


---

# Workflow Modul IPSRS (Pemeliharaan Fasilitas & Elektro Medik)
> **Status**: *On-going modul*

## 1. Deskripsi Umum
Manajemen pemeliharaan gedung, AC, listrik, genset, serta kalibrasi rutin alat medis (Ventilator, Patient Monitor).

## 2. Aktor Terlibat
- Kepala IPSRS
- Teknisi / Mekanik

## 3. Alur Kerja (Ideal & Fallback)
1. **Sistem Tiket (Helpdesk):** Perawat Bangsal mengirim tiket keluhan (misal: "AC Bocor di Kamar 203").
2. **Penugasan (Dispatch):** Kepala IPSRS menugaskan teknisi. Tiket berubah status menjadi `In Progress`.
3. **Pemakaian Sparepart:** Teknisi mengambil suku cadang (Freon, Kabel) dari Gudang Teknik. Stok dipotong.
4. **Penyelesaian:** Teknisi memfoto bukti perbaikan dari aplikasi *mobile*. Status tiket menjadi `Closed`.
5. **Preventive Maintenance:** ERP membunyikan alarm jadwal kalibrasi alat medis yang akan jatuh tempo dalam 30 hari.

## 4. Trigger & Integrasi
- **Bridging:** ASPAK Kemenkes (Aplikasi Sarana Prasarana dan Alat Kesehatan).


---

# Workflow Modul Kamar Jenazah & Forensik
> **Status**: *On-going modul*

## 1. Deskripsi Umum
Manajemen pemulasaraan jenazah, penyimpanan di lemari pendingin (freezer), visum, dan penyewaan ambulans jenazah.

## 2. Aktor Terlibat
- Dokter Forensik
- Petugas Kamar Jenazah
- Supir Ambulans

## 3. Alur Kerja (Ideal & Fallback)
1. **Penerimaan Jenazah:** Jenazah dikirim dari IGD/Ranap. Status Rekam Medis (RM) pasien dikunci menjadi `Meninggal/Deceased`.
2. **Pemulasaraan:** Tindakan memandikan, mengkafani/memakaikan baju, atau formalin dicatat di sistem.
3. **Sewa Freezer:** Jika keluarga belum mengambil, ERP menghitung sewa freezer per 24 jam.
4. **Penerbitan Surat:** Surat Keterangan Kematian dicetak dan ditandatangani digital.
5. **Keluar:** Ambulans dipesan via sistem Kasir. Jenazah dibawa pulang.

## 4. Trigger & Integrasi
- **Menembak Event:** `Jenazah.Keluar` -> Meng-update laporan mortalitas bulanan RS.


---

# Workflow Modul Kesehatan Lingkungan (Kesling) & Limbah B3
> **Status**: *On-going modul*

## 1. Deskripsi Umum
Pencatatan harian volume sampah infeksius, non-infeksius, dan benda tajam, serta pelaporan vendor pengolah limbah.

## 2. Aktor Terlibat
- Petugas Sanitarian
- Vendor Pihak Ketiga

## 3. Alur Kerja (Ideal & Fallback)
1. **Penimbangan Harian:** Petugas menimbang kantong kuning (infeksius) dari tiap ruangan. Data berat (Kg) dimasukkan ke ERP.
2. **Penyimpanan di TPS B3:** Akumulasi volume limbah dihitung otomatis oleh sistem. Jika mendekati kapasitas maksimal TPS, alarm menyala.
3. **Pengangkutan Vendor:** Vendor (misal: PT. Waste) mengambil limbah. Serah terima (Manifest) dicetak dari sistem.

## 4. Trigger & Integrasi
- **Bridging:** SIRAJA Limbah (Sistem Informasi Pelaporan Pengelolaan Limbah B3 Kementerian LHK).


---

# Workflow Modul Keuangan & Akuntansi Sentral
> **Status**: *On-going modul*

## 1. Deskripsi Umum
Penyusunan Jurnal Umum otomatis dari modul pelayanan, Buku Besar, Neraca, Laba/Rugi, dan Account Payable/Receivable.

## 2. Aktor Terlibat
- Akuntan
- Direktur Keuangan

## 3. Alur Kerja (Ideal & Fallback)
1. **Auto-Posting Jurnal:** Setiap ada pasien bayar, obat dibeli (PO), atau operasi selesai, ERP secara *background* membuat jurnal (Debet/Kredit).
2. **Hutang Dagang (A/P):** Saat barang Farmasi masuk gudang, nilai faktur masuk ke antrean Hutang. Keuangan memproses pembayaran ke vendor.
3. **Piutang BPJS (A/R):** Tagihan Casemix masuk sebagai piutang. Ketika BPJS mentransfer dana, Akuntan mencatat rekonsiliasi pembayaran.
4. **Closing Bulanan:** Laporan Neraca & Laba Rugi digenerate setiap akhir bulan.

## 4. Trigger & Integrasi
- **Integrasi Internal:** Modul sentral (Muara dari semua transaksi).


---

# Workflow Modul HRIS & Kepegawaian (SDM)
> **Status**: *On-going modul*

## 1. Deskripsi Umum
Sistem kepegawaian, *payroll* (penggajian), jadwal *shift* perawat, insentif dokter (Fee for Service), dan absensi.

## 2. Aktor Terlibat
- Staf HRD
- Seluruh Pegawai

## 3. Alur Kerja (Ideal & Fallback)
1. **Manajemen Shift:** Kepala Ruangan menyusun jadwal Pagi/Siang/Malam untuk perawat bangsal di sistem.
2. **Absensi & Lembur:** Data absensi (fingerprint/face recognition) ditarik masuk ke ERP.
3. **Kalkulasi Jasa Medis:** ERP menghitung berapa kali Dokter A melakukan operasi atau periksa poli dalam 1 bulan, dan mengakumulasikan *Fee for Service*-nya.
4. **Payroll:** Gaji pokok + Tunjangan + Jasa Medis - Potongan diproses. Slip gaji elektronik dikirim ke aplikasi/email pegawai.

## 4. Trigger & Integrasi
- **Menembak Event:** `HRIS.PayrollSelesai` -> Memasukkan beban gaji ke dalam Modul Akuntansi.


---

# Workflow Modul Hemodialisa (Cuci Darah)
> **Status**: *On-going modul*

## 1. Deskripsi Umum
Layanan tindakan cuci darah rutin yang membutuhkan manajemen mesin (*Machine Utilization*) dan siklus kunjungan pasien kronis.

## 2. Aktor Terlibat
- Perawat Hemodialisa
- Dokter Spesialis Penyakit Dalam (KGH)

## 3. Alur Kerja (Ideal & Fallback)
1. **Penjadwalan Mesin:** Pasien gagal ginjal kronis dijadwalkan secara reguler (misal: tiap Selasa dan Jumat). Sistem mem-booking *slot* Mesin HD.
2. **Pre-Tindakan:** Pengukuran berat badan basah, tekanan darah.
3. **Intra-Tindakan:** Pencatatan *Ultrafiltration Rate*, BHP (Dialyzer, Bloodline), Heparin.
4. **Post-Tindakan:** Evaluasi klinis. Pengulangan otomatis rujukan internal BPJS (biasanya rujukan berlaku 3 bulan).


---

# Workflow Modul Medical Check Up (MCU)
> **Status**: *On-going modul*

## 1. Deskripsi Umum
Layanan pemeriksaan kesehatan preventif baik untuk individu maupun korporat (Perusahaan).

## 2. Aktor Terlibat
- Petugas MCU
- Dokter Umum / Spesialis

## 3. Alur Kerja (Ideal & Fallback)
1. **Pendaftaran Paket:** Pasien (atau rombongan karyawan pabrik) didaftarkan dengan "Paket MCU Silver/Gold".
2. **Routing Otomatis:** Sistem memecah antrean ke Lab, Radiologi, Audiometri, dan Poli Mata tanpa perlu order manual dokter.
3. **Kompilasi Hasil:** Seluruh hasil dari penunjang otomatis terkumpul dalam satu *dashboard* Buku Laporan MCU.
4. **Verifikasi Kesimpulan:** Dokter MCU menarik kesimpulan akhir (*Fit to Work* / *Unfit*).


---

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


---

# Workflow Modul Bank Darah RS (BDRS)
> **Status**: *On-going modul*

## 1. Deskripsi Umum
Manajemen stok kantong darah, uji silang serasi (Crossmatch), dan donor pengganti.

## 2. Aktor Terlibat
- Petugas BDRS

## 3. Alur Kerja (Ideal & Fallback)
1. **Request Darah:** Dokter operasi / IGD memesan 2 kantong PRC via sistem (Gol. Darah B).
2. **Pengadaan:** Jika stok kosong, petugas menerbitkan surat rujukan darah ke PMI secara sistem.
3. **Crossmatch:** Sampel darah pasien diuji silang dengan kantong darah di lab. Hasil diinput ke ERP.
4. **Distribusi:** Kantong darah dengan *barcode* diambil perawat bangsal. Tagihan biaya pengolahan darah otomatis masuk ke kasir.


---

# Workflow Modul Customer Service & Humas
> **Status**: *On-going modul*

## 1. Deskripsi Umum
Manajemen keluhan pelanggan, informasi RS, dan registrasi pendaftaran pasien *online*.

## 2. Aktor Terlibat
- Customer Service

## 3. Alur Kerja (Ideal & Fallback)
1. **Ticketing Komplain:** Komplain pasien via Whatsapp/Web RS otomatis ditarik menjadi 'Tiket' di ERP (misal: "Toilet lantai 2 kotor").
2. **Eskalasi:** CS mengarahkan tiket ke Cleaning Service / IPSRS.
3. **Broadcast:** Humas mengirimkan notifikasi *blast* jadwal libur dokter spesialis ke pasien *chronic* (prolanis).


---

# Workflow Modul Laundry & Manajemen Linen
> **Status**: *On-going modul*

## 1. Deskripsi Umum
Pengelolaan perputaran linen (sprei, selimut, baju operasi) yang kotor, infeksius, hingga kembali bersih.

## 2. Aktor Terlibat
- Petugas Laundry

## 3. Alur Kerja (Ideal & Fallback)
1. **Penimbangan Kotor:** Linen kotor dari bangsal dibawa dan ditimbang (Kg). Dipisah antara bak Infeksius (Merah) dan Non-Infeksius.
2. **Pencucian:** Mesin dioperasikan, ERP mencatat penggunaan deterjen kimia harian dari gudang linen.
3. **Distribusi Bersih:** Linen bersih disimpan ke lemari penyimpanan. Ruangan menarik (*Request*) stok linen bersih via ERP.


---


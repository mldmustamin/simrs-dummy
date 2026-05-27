import os

folder_path = "/home/gudang-data-kantor/simrs-web/docs/planning_and_roadmaps/"

modules_data = {
    "01_Pendaftaran_Admisi.md": {
        "title": "Pendaftaran & Admisi (Front Office)",
        "desc": "Titik nol perjalanan pasien. Bertanggung jawab atas pencatatan demografi, jaminan, dan distribusi antrean ke poli atau rawat inap.",
        "actors": ["Petugas Pendaftaran", "Supervisor Front Office", "KiosK Mandiri"],
        "journey": [
            "Pasien mengambil tiket dari mesin antrean atau daftar online via Mobile JKN.",
            "Petugas memverifikasi identitas (KTP/Sidik Jari) dan Jaminan (BPJS/Asuransi Swasta).",
            "Sistem membuat/menarik Rekam Medis (RM) pasien.",
            "Sistem menerbitkan nomor antrean Poli tujuan dan mengarahkan pasien."
        ],
        "erp": [
            "Generate `no_rawat` berdasarkan urutan poli per hari.",
            "Insert data ke `reg_periksa` dengan status `Belum Diperiksa`.",
            "Memicu invoice awal di modul `Kasir`."
        ],
        "ideal": "Koneksi V-Claim BPJS merespons < 1 detik. SEP digital terbit otomatis. Fingerprint langsung tervalidasi.",
        "pragmatis": "V-Claim Timeout. Sistem menyimpan antrean secara lokal, mengizinkan pasien langsung ke poli, dan memasukkan request SEP ke `Background Job` untuk di-retry 50x.",
        "integration": "BPJS (V-Claim), Dukcapil (NIK), Mobile JKN.",
        "edge": "Pasien gawat darurat tanpa identitas (Mr. X) masuk. Sistem men-generate RM sementara yang bisa di-merge di kemudian hari."
    },
    "02_Poliklinik_Rawat_Jalan.md": {
        "title": "Poliklinik (Rawat Jalan)",
        "desc": "Modul tempat dokter spesialis dan perawat melakukan asesmen awal, anamnesis, dan penentuan terapi.",
        "actors": ["Perawat Poli", "Dokter Spesialis DPJP"],
        "journey": [
            "Perawat memanggil pasien, melakukan ukur TTV (Tensi, Suhu, Berat) dan Anamnesis.",
            "Dokter memanggil pasien, membuka EMR, memeriksa riwayat historis.",
            "Dokter menginput Diagnosa Utama (ICD-10) dan Tindakan (ICD-9CM).",
            "Dokter meresepkan obat secara elektronik (E-Resep) atau Order Lab/Rad (CPOE)."
        ],
        "erp": [
            "Merekam `pemeriksaan_ralan`.",
            "Mengirim event `Poli.Selesai` yang merilis harga layanan ke `Kasir`.",
            "Membuka kunci antrean di Farmasi/Lab."
        ],
        "ideal": "Dokter mengisi SOAP secara komplit saat pasien duduk di depan meja. Sistem memberi peringatan interaksi obat secara real-time.",
        "pragmatis": "Kekacauan antrean. Dokter hanya menginput diagnosis singkat. SOAP diisi retrospektif (mundur waktu) 2 jam kemudian dengan sistem mencatat `created_at` asli.",
        "integration": "SATUSEHAT (Kunjungan Rawat Jalan).",
        "edge": "Salah input diagnosis setelah di-TTE. Fitur Addendum diaktifkan."
    },
    "03_Rawat_Inap_Bangsal.md": {
        "title": "Rawat Inap & Bangsal",
        "desc": "Modul pengawasan 24/7. Mengelola CPPT (Catatan Terintegrasi), bed management, dan asuhan keperawatan rutin.",
        "actors": ["Kepala Ruangan", "Perawat Shift", "Dokter Visite"],
        "journey": [
            "Transfer in dari IGD/Poli. Orientasi ruangan oleh perawat.",
            "Asesmen risiko jatuh dan nyeri.",
            "Perawat shift Pagi/Siang/Malam melakukan operan (Handover SBAR).",
            "Dokter DPJP melakukan Visite harian.",
            "Pemberian obat injeksi/oral sesuai jadwal E-MAR."
        ],
        "erp": [
            "Status bed berubah dinamis: `Kosong` -> `Ditempati` -> `Reserve Pulang`.",
            "Auto-Billing Midnight Census (00:00) menagih biaya sewa kamar otomatis.",
            "Validasi Barcode Gelang Pasien sebelum obat diberikan (E-MAR Lock)."
        ],
        "ideal": "Smart Ward: TTV langsung ditarik dari Patient Monitor ke sistem via IoT.",
        "pragmatis": "Kertas Lembar Observasi tetap dicetak sebagai backup, lalu di-input massal ke komputer (Double Input) untuk akreditasi.",
        "integration": "SIRANAP Kemenkes (Sistem Informasi Rawat Inap).",
        "edge": "Code Blue (Henti Jantung). Alarm berbunyi, Response Time Tim Resusitasi dicatat otomatis oleh sistem."
    },
    "04_IGD_Triase.md": {
        "title": "Instalasi Gawat Darurat (IGD) & Triase",
        "desc": "Penanganan nyawa. Membutuhkan sistem yang tidak memblokir tindakan di saat kritis.",
        "actors": ["Dokter Jaga IGD", "Perawat Triase"],
        "journey": [
            "Pasien masuk. Triase (<2 menit): Merah, Kuning, Hijau, Hitam.",
            "Pasien prioritas masuk ruang resusitasi tanpa perlu daftar.",
            "Tindakan *Life Saving* dan pemberian obat emergency dari kotak depo."
        ],
        "erp": [
            "Bypass validasi kasir. Tagihan menumpuk secara asinkronus.",
            "Virtual mutasi obat dari `Gudang_IGD`."
        ],
        "ideal": "Integrasi alat EKG langsung ke EMR Dokter.",
        "pragmatis": "Verbal Order (Resep Lisan) diakomodasi. Perawat menyuntik dulu, form resep di-approve dokter 24 jam kemudian (Retrospektif).",
        "integration": "SPGDT Kemenkes.",
        "edge": "Mass Casualty (Kecelakaan Masal). Sistem memiliki fitur 'Batch Admit' Mr.X 1 hingga Mr.X 20."
    },
    "05_Apotek_Farmasi.md": {
        "title": "Instalasi Farmasi (Apotek)",
        "desc": "Jantung pengeluaran stok. Manajemen resep, PIO, dan kalkulasi HNA+Margin.",
        "actors": ["Apoteker", "Asisten Apoteker"],
        "journey": [
            "Menerima E-Resep. Apoteker melakukan telaah (Screening klinis).",
            "Meracik puyer/salep atau menyiapkan obat jadi.",
            "Validasi pembayaran (Pasien Umum).",
            "Penyerahan obat dengan Pelayanan Informasi Obat (PIO)."
        ],
        "erp": [
            "Pessimistic Locking pada tabel `gudangbarang` untuk menghindari Race Condition stok.",
            "Otomatis injeksi harga `Tuslah` dan `Embalase`."
        ],
        "ideal": "Sistem otomatis mengkalkulasi FEFO (First Expired First Out) dan memandu lokasi rak obat.",
        "pragmatis": "Jika stok komputer 0 tapi fisik ada, sistem mengizinkan 'Force Dispense' dengan mencatat minus stok sementara untuk diperbaiki saat Stock Opname.",
        "integration": "E-Katalog Kemenkes, SIPNAP.",
        "edge": "Pasien alergi obat yang diresepkan. Apoteker me-reject E-Resep, sistem mengirim notif ke EMR Poli untuk penggantian obat."
    },
    "06_Kasir_Billing.md": {
        "title": "Kasir & Billing Sentral",
        "desc": "Muara dari seluruh beban biaya pasien (Konsolidasi Invoice).",
        "actors": ["Petugas Kasir", "Direktur Keuangan"],
        "journey": [
            "Pasien datang membawa nomor RM.",
            "Kasir memverifikasi rincian tagihan dari Poli, Lab, Obat, dan Tindakan.",
            "Menerima pembayaran Tunai/EDC/QRIS.",
            "Menerbitkan Kwitansi Lunas dan Surat Bebas Tanggungan."
        ],
        "erp": [
            "Menembakkan event `Kasir.Lunas` yang melepaskan penahanan pasien pulang.",
            "Auto-posting debet Kas dan kredit Pendapatan ke tabel Jurnal."
        ],
        "ideal": "Pasien membayar mandiri via KiosK menggunakan QRIS Dinamis.",
        "pragmatis": "Emergency Override: Pasien tidak punya uang. Direktur memasukkan PIN Otorisasi Khusus untuk mem-bypass sistem agar pasien bisa pulang (Bad Debt).",
        "integration": "Payment Gateway (Moota/Midtrans).",
        "edge": "Mesin EDC mati lampu di tengah swipe. Sistem Kasir dapat mengecek status Suspended Transaction."
    },
    "07_Laboratorium_Radiologi.md": {
        "title": "Laboratorium & Radiologi",
        "desc": "Penunjang medis. Pemrosesan sampel/scan dan pelaporan hasil (Expertise).",
        "actors": ["Analis Lab", "Radiografer", "Dokter Spesialis"],
        "journey": [
            "Pasien menyerahkan barcode CPOE.",
            "Pengambilan spesimen darah / Pemosisian pasien rontgen.",
            "Analisa mesin.",
            "Dokter merilis hasil bacaan (Expertise)."
        ],
        "erp": [
            "Integrasi LIS (Laboratory Information System) - nilai darah masuk otomatis ke kolom ERP.",
            "Integrasi PACS - Gambar DICOM rontgen bisa dibuka langsung dari EMR dokter perujuk."
        ],
        "ideal": "Fully paperless. Hasil muncul instan di layar HP/Tablet dokter DPJP.",
        "pragmatis": "Alat Lab rusak. Pasien dikirim ke lab luar (Rujukan Parsial), hasil luar di-scan PDF dan di-upload ke sistem sebagai Attachment.",
        "integration": "SATUSEHAT (Kirim Hasil Lab/Radiologi).",
        "edge": "Hasil Kritis (Klaim Panik). Darah Hb < 5. Alarm menyala berkedip merah di EMR IGD."
    },
    "08_Kamar_Operasi_CSSD.md": {
        "title": "Kamar Operasi (OK) & CSSD",
        "desc": "Manajemen penjadwalan pembedahan, pencatatan BHP, dan sterilisasi alat.",
        "actors": ["Dokter Bedah", "Perawat Omloop", "Petugas CSSD"],
        "journey": [
            "Asesmen Pra-Bedah oleh Anestesi.",
            "Operasi berjalan (Intra). Perawat mencatat tiap benang dan kassa yang dipakai.",
            "Pasien dipindah ke Recovery Room (RR).",
            "Alat kotor dikirim ke CSSD untuk dicuci dan di-Autoclave."
        ],
        "erp": [
            "Pemotongan inventori BHP secara real-time.",
            "Sistem CSSD men-generate barcode Expired Date sterilisasi per instrumen set."
        ],
        "ideal": "Layar monitor besar di ruang tunggu menampilkan status operasi (Persiapan -> Operasi -> Pemulihan) layaknya bandara.",
        "pragmatis": "Operasi memakan waktu lebih lama dari jadwal (Pendarahan Hebat). Sistem meng-hold dan menunda otomatis jadwal bedah berikutnya.",
        "integration": "Sistem Antrean Operasi RS.",
        "edge": "Mesin Autoclave CSSD rusak. Operasi non-cito dibatalkan sistem otomatis karena set steril tidak tersedia."
    },
    "09_Logistik_Gudang.md": {
        "title": "Logistik & Gudang Umum",
        "desc": "Manajemen Supply Chain. Rantai penerimaan barang dari vendor hingga distribusi ke ruangan.",
        "actors": ["Kepala Gudang", "Purchasing"],
        "journey": [
            "Pembuatan Purchase Request (PR) dari ruangan.",
            "Purchasing mengubah PR menjadi Purchase Order (PO) ke PBF.",
            "Barang datang. Petugas Gudang melakukan Goods Receipt (GR), mengecek Faktur.",
            "Distribusi barang ke depo-depo rumah sakit."
        ],
        "erp": [
            "Kalkulasi Harga Pokok Penjualan (HPP) menggunakan Moving Average.",
            "Pencatatan Nomor Batch dan Tanggal Kadaluarsa mutlak diwajibkan."
        ],
        "ideal": "Auto-Restock. Sistem menembak email PO otomatis ke vendor jika stok menyentuh titik Minimum (Buffer).",
        "pragmatis": "Vendor kirim barang hanya setengah dari PO. Sistem melakukan Partial Receipt dan mengkalkulasi ulang sisa hutang (Account Payable).",
        "integration": "E-Faktur Pajak.",
        "edge": "Pabrik Oksigen cair meledak. Alarm sistem menyala merah ketika Buffer Oksigen medis turun ke level kritis."
    },
    "10_Rekam_Medis_Casemix.md": {
        "title": "Rekam Medis & Casemix",
        "desc": "Back-office untuk audit kelengkapan berkas, koding ICD, dan pengajuan klaim piutang BPJS.",
        "actors": ["Koder", "Petugas Casemix BPJS"],
        "journey": [
            "Pasien pulang. EMR dikunci.",
            "Koder menganalisa kelengkapan (KLPCM).",
            "Pemberian kode ICD-10 dan ICD-9CM.",
            "Grouping INA-CBG untuk menarik nilai tarif klaim.",
            "Pemberkasan (Penggabungan SEP, Resume Medis, Rincian Kasir) menjadi PDF Klaim."
        ],
        "erp": [
            "Pemblokiran klaim jika EMR belum memiliki Tanda Tangan Elektronik dokter.",
            "Jurnal otomatis: Piutang Klaim (Debet)."
        ],
        "ideal": "AI Coding. Sistem menyarankan kode ICD otomatis berdasarkan teks bahasa alami dari SOAP dokter.",
        "pragmatis": "Klaim di-pending oleh BPJS. Petugas Casemix memiliki form Dispute untuk melampirkan alasan sanggahan.",
        "integration": "INA-CBG E-Klaim Kemenkes.",
        "edge": "Dokter tidak mau mengisi EMR lengkap. Sistem mengaktifkan sanksi otomatis: Menahan pencairan Jasa Medis (Fee for Service) dokter tersebut bulan ini."
    },
    "11_Gizi_Dapur_Sentral.md": {
        "title": "Instalasi Gizi & Dapur Sentral",
        "desc": "Manajemen nampan diet pasien dan logistik bahan makanan mentah.",
        "actors": ["Ahli Gizi", "Koki Dapur"],
        "journey": [
            "Dapur menerima kompilasi pesanan diet (Bubur, Nasi, Rendah Garam) dari Ranap.",
            "Memasak dan memporsikan ke nampan pasien berlabel barcode.",
            "Distribusi menggunakan troli tertutup."
        ],
        "erp": [
            "Pemotongan stok bahan basah (beras, sayur) dari Gudang Gizi harian.",
            "Pencegahan Fatal: Sistem langsung membunyikan alarm di layar Dapur jika pasien yang diproses memiliki rekaman `Alergi Telur`."
        ],
        "ideal": "Sistem menghitung nilai kalori pasti per porsi dan melaporkannya ke EMR pasien.",
        "pragmatis": "Keluarga menyelundupkan makanan luar. Perawat bangsal mencatat asupan gizi eksternal sebagai anomali.",
        "integration": "Internal ERP.",
        "edge": "Keracunan makanan massal. Sistem bisa men-trace batch bahan makanan mana (Supplier Sayur X) yang digunakan pada tanggal kejadian."
    },
    "12_IPSRS_Teknisi.md": {
        "title": "IPSRS (Teknisi RS)",
        "desc": "Sistem Helpdesk perbaikan gedung/AC dan jadwal kalibrasi alat medis bernilai miliaran.",
        "actors": ["Mekanik", "Teknisi Elektromedik"],
        "journey": [
            "Ruangan mensubmit Tiket Kerusakan.",
            "Teknisi mengambil sparepart dari gudang teknik dan mengeksekusi perbaikan.",
            "Teknisi menutup tiket."
        ],
        "erp": [
            "Peringatan Kalibrasi (Preventive Maintenance) untuk Ventilator/Mesin Anestesi setiap 12 bulan.",
            "Sistem melarang mesin yang belum dikalibrasi digunakan di modul Kamar Operasi."
        ],
        "ideal": "Sistem IoT dari Genset otomatis mengirim log BBM ke ERP setiap hari.",
        "pragmatis": "Mati lampu, Genset utama gagal menyala 10 detik. Teknisi menerima Push Notification darurat ke HP pribadi.",
        "integration": "ASPAK (Aplikasi Sarana Prasarana Kemenkes).",
        "edge": "Pipa oksigen sentral bocor. Eskalasi darurat level 1 ke Direktur Umum."
    },
    "13_Kamar_Jenazah_Forensik.md": {
        "title": "Kamar Jenazah & Forensik",
        "desc": "Pemulasaraan jenazah, sewa freezer, dan pelayanan forensik medis.",
        "actors": ["Petugas Jenazah", "Dokter Forensik"],
        "journey": [
            "Jenazah diterima dari bangsal.",
            "Jenazah dimandikan/dikafani.",
            "Keluarga membayar sewa ambulans jenazah ke kasir dan membawa jenazah."
        ],
        "erp": [
            "Kalkulasi sewa lemari pendingin (freezer) per 24 jam.",
            "Penguncian mutlak rekam medis menjadi status `Meninggal/Deceased` agar tidak bisa didaftarkan poli lagi."
        ],
        "ideal": "Pencetakan Surat Kematian Digital terenkripsi QRCode.",
        "pragmatis": "Keluarga Mr.X tidak ditemukan. Setelah 3 hari di freezer, sistem mengirim notifikasi integrasi pelaporan ke Dinas Sosial untuk pemakaman gratis.",
        "integration": "Disdukcapil (Pelaporan Kematian Otomatis).",
        "edge": "Polisi meminta Visum et Repertum. Sistem mengamankan (lock) rekam medis dari ahli waris karena berstatus Barang Bukti Hukum."
    },
    "14_Limbah_B3_Kesling.md": {
        "title": "Kesehatan Lingkungan (Limbah B3)",
        "desc": "Pengelolaan limbah medis beracun dan pencatatan Manifest Pengangkutan pihak ketiga.",
        "actors": ["Sanitarian", "Vendor Limbah"],
        "journey": [
            "Sanitarian menimbang limbah infeksius (kantong merah/kuning) harian per bangsal.",
            "Limbah disimpan di TPS B3 RS.",
            "Vendor datang, mengangkut, dan mencetak Surat Manifest."
        ],
        "erp": [
            "Kalkulasi total timbulan limbah bulanan.",
            "Sistem menahan pembayaran tagihan vendor jika dokumen Manifest pemusnahan dari insinerator belum di-upload."
        ],
        "ideal": "Timbangan limbah digital terkoneksi WiFi langsung ke database.",
        "pragmatis": "Penginputan angka berat limbah secara manual di penghujung hari operasional.",
        "integration": "SIRAJA Limbah KLHK.",
        "edge": "Vendor telat datang 3 hari. TPS Overload. Sistem membangkitkan alarm bahaya infeksi silang ke Komite PPI."
    },
    "15_Keuangan_Akuntansi.md": {
        "title": "Keuangan & Akuntansi",
        "desc": "Buku Besar, Jurnal Umum, Laba/Rugi, Neraca. Seluruh transaksi RS bermuara di sini.",
        "actors": ["Akuntan", "Direktur Keuangan"],
        "journey": [
            "Penerimaan Kasir -> Jurnal Pendapatan.",
            "Pembelian Obat -> Jurnal Hutang (A/P).",
            "Klaim BPJS -> Jurnal Piutang (A/R).",
            "Pembayaran Gaji -> Jurnal Beban Gaji."
        ],
        "erp": [
            "Sistem melakukan Auto-Posting secara diam-diam (Background).",
            "Konsolidasi laporan real-time tanpa tutup buku bulanan yang membosankan."
        ],
        "ideal": "Rekonsiliasi Bank Otomatis (Host-to-Host) membaca mutasi rekening BCA/Mandiri RS.",
        "pragmatis": "Akuntan tetap bisa melakukan Jurnal Penyesuaian Manual (Manual Entry) jika ada kas kecil (Petty Cash) yang selisih.",
        "integration": "Sistem Perbankan (Opsional).",
        "edge": "Selisih kurs valuta asing saat membeli mesin MRI dari Jerman. Sistem mengakomodasi perhitungan laba/rugi kurs."
    },
    "16_HRIS_SDM.md": {
        "title": "HRIS & SDM (Kepegawaian)",
        "desc": "Penjadwalan shift, absensi, KPI, payroll, dan Jasa Medis (Remunerasi Dokter).",
        "actors": ["HRD", "Dokter", "Perawat"],
        "journey": [
            "Fingerprint ditarik otomatis.",
            "Penyusunan Shift Perawat Bulanan.",
            "Hitung Payroll (Gaji Pokok + Tunjangan - Pajak).",
            "Hitung Jasa Pelayanan (Jaspel) dari tindakan klinis ERP."
        ],
        "erp": [
            "Kalkulasi `Fee for Service` yang sangat kompleks berdasarkan proporsi jasa Asisten vs Operator saat pembedahan.",
            "Integrasi pemotongan BPJS Ketenagakerjaan dan Kesehatan."
        ],
        "ideal": "Absensi berbasis Face Recognition tersinkron GPS di HP (Mobile App).",
        "pragmatis": "Fingerprint rusak. Admin bangsal mengeklik tombol 'Hadir' secara manual untuk staf shift malam.",
        "integration": "Mesin Absensi, Pajak PPh 21.",
        "edge": "Dokter menuntut transparansi Jaspel. ERP menyediakan Dashboard khusus Dokter untuk melihat rincian pasien mana saja yang sudah ia layani beserta nominal jasanya secara transparan."
    },
    "17_Hemodialisa.md": {
        "title": "Hemodialisa (Cuci Darah)",
        "desc": "Layanan siklik pasien kronis yang memerlukan booking mesin jangka panjang.",
        "actors": ["Perawat HD", "Dokter KGH"],
        "journey": [
            "Pasien datang sesuai jadwal rutin (Booking Slot Mesin).",
            "Pemeriksaan TTV Pre-HD.",
            "Mesin menyala (Intra-HD), pemberian Heparin.",
            "Penyelesaian (Post-HD), penjadwalan bulan depan."
        ],
        "erp": [
            "Sistem menjadwalkan ulang 8 sesi kunjungan secara masal (Bulk Scheduling).",
            "Sistem mengingatkan masa aktif rujukan BPJS yang habis tiap 3 bulan."
        ],
        "ideal": "Mesin Hemodialisa mengirim data *Ultrafiltration Rate* langsung ke sistem.",
        "pragmatis": "Rujukan BPJS habis masa berlaku di tengah siklus. Sistem memasukkan pasien ke mode Penjaminan Sementara sampai keluarga mengurus kertas rujukan baru ke Puskesmas.",
        "integration": "Internal ERP.",
        "edge": "Pasien Drop (Hipotensi) saat dicuci darah. Tindakan Emergency Stop dieksekusi, pasien dialihkan ke ICU tanpa perlu daftar dari awal."
    },
    "18_Medical_Check_Up.md": {
        "title": "Medical Check Up (MCU)",
        "desc": "Pelayanan preventif berpaket (massal/korporat).",
        "actors": ["Petugas MCU", "Dokter Spesialis"],
        "journey": [
            "Pendaftaran Paket (misal: Paket Eksekutif Jantung).",
            "Sistem me-routing pasien untuk antre ke Poli Jantung, Lab, Rontgen, dan Treadmill.",
            "Sistem mengkompilasi seluruh hasil dari berbagai unit menjadi 1 Buku Laporan PDF.",
            "Dokter MCU menarik kesimpulan akhir (*Fit to Work*)."
        ],
        "erp": [
            "Sistem mencegah Modul Kasir menagihkan biaya per item, melainkan menagihkan Harga Paket.",
            "Kalkulasi diskon kolektif untuk Karyawan Perusahaan (Corporate Billing)."
        ],
        "ideal": "Buku Hasil MCU bisa diunduh via Portal Pasien / Mobile App RS oleh pasien dari rumah.",
        "pragmatis": "Perusahaan BUMN X meminta format PDF laporan diubah secara spesifik. ERP menyediakan Template Engine (HTML to PDF) untuk kustomisasi.",
        "integration": "Lab & Radiologi.",
        "edge": "Ditemukan penyakit kritis (misal: Tumor) saat MCU. Pasien di-switch statusnya secara sistem menjadi Pasien Rawat Jalan Kuratif (BPJS) untuk ditindaklanjuti."
    },
    "19_Rehabilitasi_Medik.md": {
        "title": "Rehabilitasi Medik (Fisioterapi)",
        "desc": "Manajemen sesi terapi berulang dan kuota asuransi.",
        "actors": ["Fisioterapis", "Dokter KFR"],
        "journey": [
            "Dokter membuat program terapi (misal: 6x kunjungan).",
            "Fisioterapis melayani pasien setiap datang.",
            "Sistem mencatat kedatangan 1/6, 2/6, dst."
        ],
        "erp": [
            "Pemblokiran sistem (*Hard Stop*) jika pasien datang ke-7 kalinya sementara asuransinya hanya meng-cover 6 kali per siklus rujukan."
        ],
        "ideal": "Sensor gerak/IoT merekam kemajuan sudut tekuk lutut pasien ke dalam ERP.",
        "pragmatis": "Sistem peringatan sisa kuota (Warning) pada kunjungan ke-5 agar pasien siap-siap memperpanjang rujukan.",
        "integration": "Internal ERP.",
        "edge": "Pasien menyerah di sesi ke-3 dan tidak pernah datang lagi. Sistem otomatis melakukan Auto-Discharge setelah 30 hari tidak ada aktivitas."
    },
    "20_Bank_Darah_BDRS.md": {
        "title": "Bank Darah Rumah Sakit (BDRS)",
        "desc": "Manajemen stok kantong darah (PRC, TC, FFP) dan Uji Silang Serasi.",
        "actors": ["Petugas Lab/BDRS"],
        "journey": [
            "Dokter Ranap memesan kantong darah.",
            "BDRS menerima permintaan, mengambil sampel darah pasien, melakukan Crossmatch.",
            "Menyiapkan kantong darah cocok (Compatible).",
            "Menyerahkan ke perawat ruangan."
        ],
        "erp": [
            "Stok kantong darah dikelola per Golongan Darah dan Rhesus.",
            "Sistem menagihkan biaya Pengolahan Darah (Bukan biaya beli darah) ke modul Kasir."
        ],
        "ideal": "Kulkas penyimpan darah dilengkapi sensor suhu IoT. Alarm menyala di ERP jika suhu kulkas naik membahayakan stok darah.",
        "pragmatis": "Kekosongan stok darah RS. Sistem menerbitkan form Rujukan Darah PMI untuk diserahkan keluarga pasien ke PMI Kota.",
        "integration": "Sistem PMI (Jika tersedia).",
        "edge": "Reaksi Transfusi. Pasien gatal/syok saat ditransfusi. EMR memiliki modul Pelaporan Insiden Transfusi Darah (Hemovigilance) untuk investigasi BDRS."
    },
    "21_Customer_Service_Humas.md": {
        "title": "Customer Service & Humas",
        "desc": "Manajemen Front-End publik, portal keluhan, registrasi mandiri, dan informasi ketersediaan bed.",
        "actors": ["CS / Humas"],
        "journey": [
            "Pasien melakukan komplain di Web RS.",
            "Masuk sebagai 'Ticket' di dashboard CS.",
            "CS meresolve atau meneruskan ke unit terkait."
        ],
        "erp": [
            "Dashboard sentral untuk memantau Kepuasan Pelanggan (Survey Bintang 5 di KiosK setelah pulang).",
            "Mekanisme Push Notification/SMS Broadcast ke pasien tentang promosi Poli Estetika."
        ],
        "ideal": "Chatbot AI terintegrasi di Whatsapp Resmi RS yang mengambil jadwal dokter dari API ERP secara langsung.",
        "pragmatis": "Broadcast SMS biasa untuk daerah dengan internet lemah.",
        "integration": "Whatsapp Gateway / SMS Gateway.",
        "edge": "Viralkan di Sosmed. Komplain berat (Kematian diduga Malpraktik) masuk ke tiket sistem dengan bendera MERAH, meng-SMS otomatis Direktur Utama."
    },
    "22_Laundry_Linen.md": {
        "title": "Laundry & Manajemen Linen",
        "desc": "Siklus pembersihan dan pengendalian infeksi linen RS (Sprei, Baju OK, Selimut).",
        "actors": ["Petugas Laundry"],
        "journey": [
            "Pengumpulan linen kotor (Infeksius Merah / Non-Infeksius Hitam) dari bangsal.",
            "Penimbangan total (Kg) di pintu Laundry.",
            "Pencucian, Penyetrikaan, Pelipatan.",
            "Penyimpanan di Rak Bersih, dan didistribusikan ulang."
        ],
        "erp": [
            "Sistem melacak frekuensi cuci per lembar linen menggunakan tag RFID (Mode Enterprise).",
            "Pemotongan stok bahan kimia laundry (Deterjen, Klorin) dari Gudang Utama."
        ],
        "ideal": "Linen dilengkapi chip RFID tahan panas. Setiap melewati pintu bangsal, sistem otomatis mencatat posisi linen (Track & Trace).",
        "pragmatis": "Menghitung berat total (Kiloan) per bangsal dan mencatat serah terima secara manual di komputer logistik.",
        "integration": "Logistik ERP.",
        "edge": "Wabah Penyakit Menular. Sistem mengunci linen dari bangsal isolasi agar masuk ke mesin cuci khusus (Infectious Washing Cycle) tanpa dicampur."
    }
}

for filename, content in modules_data.items():
    template = f"""{content['title']}
=========================================
**Dokumen Arsitektur & Alur Kerja**

## 1. Deskripsi Eksekutif
{content['desc']}

## 2. Aktor & Hak Akses
- {', '.join(content['actors'])}

## 3. Alur Perjalanan Pasien (Patient Journey)
{chr(10).join([f"{i+1}. {step}" for i, step in enumerate(content['journey'])])}

## 4. Alur Perjalanan Sistem (ERP Data Lifecycle)
{chr(10).join([f"- {step}" for step in content['erp']])}

## 5. Implementasi Multi-Model (Arsitektur Fallback)
- **Standar Ideal (Enterprise)**: {content['ideal']}
- **Skenario Pragmatis (Fallback)**: {content['pragmatis']}

## 6. Titik Integrasi & Bridging Eksternal
- {content['integration']}

## 7. Penanganan Bencana & Edge Cases
- ⚠️ **Skenario Ekstrem**: {content['edge']}
"""
    # Overwrite the file with the rich content
    file_path = os.path.join(folder_path, filename)
    with open(file_path, "w", encoding="utf-8") as f:
        # Add the on-going modul remark if it's > 10
        if int(filename[:2]) > 10:
            f.write("> **Status**: *On-going modul (Cetak Biru Masa Depan)*\n\n")
        f.write(template)

print("Berhasil menginjeksi konten masif, komprehensif, dan ultra-rich ke dalam seluruh 22 dokumen workflow.")

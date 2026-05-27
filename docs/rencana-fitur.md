# Master Plan & Arsitektur Fitur ERP SIMRS
*Dokumen ini merupakan penjabaran detail dari roadmap fitur menuju sistem SIMRS (ERP Rumah Sakit) yang battle-proven, komprehensif, dan siap produksi.*

---

## 🏗️ Fase 1: Core Master Data & Pricing Engine (Buku Tarif)
Fondasi dari seluruh perputaran uang di rumah sakit. Kesalahan di sini akan berdampak pada kerugian RS atau penolakan klaim.
- **Manajemen Komponen Tarif:** Pemecahan struktur biaya menjadi Jasa Rumah Sakit, Jasa Medis (Dokter), Jasa Paramedis (Perawat/Analis), KSO, dan BHP (Bahan Habis Pakai).
- **Diferensiasi Kelas & Penjamin:** Pengaturan harga dinamis berdasarkan Kelas Perawatan (VVIP, VIP, 1, 2, 3) dan Jenis Bayar (Mandiri, BPJS, Asuransi Swasta).
- **Paket Tindakan:** Manajemen Paket Operasi (Bedah) dan Paket Laboratorium (Medical Check-up) yang mendistribusikan insentif secara otomatis ke tim medis.

## 🏥 Fase 2: Front Office & Pendaftaran (Admission)
Pintu gerbang pasien yang harus cepat dan anti-antrean panjang.
- **Pendaftaran Terpusat:** Modul pendaftaran Rawat Jalan (Poliklinik), IGD, dan Rawat Inap (Admisi).
- **Kios Antrean Mandiri:** Sistem tiket antrean *touchscreen* (APM) untuk mengurangi beban loket.
- **Integrasi V-Claim BPJS (Bridging):** Pengecekan otomatis kepesertaan aktif, pembuatan SEP (Surat Eligibilitas Peserta), dan validasi rujukan Faskes Tingkat 1.

## 🩺 Fase 3: Electronic Medical Record (EMR) Dinamis
Jantung operasional medis. Mengubah kertas menjadi rekam medis elektronik penuh (Paperless).
- **Dasbor Dokter & Perawat (CPPT):** Catatan Perkembangan Pasien Terintegrasi dengan format SOAP standar.
- **Dynamic Renderer (Form Spesialis):** 
  - *Poli Gigi*: Odontogram Interaktif (klik anatomi gigi).
  - *Poli Obgyn*: Partograf, Data Kehamilan (GPA), dan HPHT.
  - *Poli Mata/THT*: Visus, Buta Warna, dan Audiometri.
- **CPOE (Computerized Provider Order Entry):** Dokter dapat langsung mengirim pesanan Laboratorium, Radiologi, dan E-Resep dari dalam layar EMR tanpa menggunakan kertas.

## 🔬 Fase 4: Penunjang Medis (LIS & RIS)
Administrasi Laboratorium (LIS) dan Radiologi (RIS).
- **Worklist Penunjang:** Antrean sampel darah atau foto rontgen khusus untuk petugas penunjang.
- **Input Nilai Rujukan & Keahlian:** Pengisian nilai hasil tes (normal vs abnormal) untuk Lab, dan *Expertise* (bacaan hasil rontgen) dari Dokter Spesialis Patologi/Radiologi.
- **Auto-Billing:** Otomatisasi pengiriman tagihan tindakan Lab/Rad langsung ke kasir (menghindari kebocoran tagihan).

## 💊 Fase 5: Farmasi & Manajemen Inventori Medis
Modul paling rentan terhadap kebocoran aset jika tidak dirancang dengan ketat.
- **E-Resep & Telaah Apoteker:** Validasi resep dokter, pengecekan alergi pasien, dan pencegahan duplikasi obat.
- **Multi-Depo Farmasi:** Pemisahan stok fisik antara Depo Rawat Jalan, Depo IGD, dan Depo Rawat Inap.
- **Real-time Inventory (Pessimistic Lock):** Pemotongan stok fisik secara akurat (*ACID Compliant*) saat obat diserahkan, mencegah stok menjadi minus akibat *race-condition*.
- **Kalkulasi Harga:** Perhitungan HPP dengan metode FIFO/FEFO, ditambah kalkulasi *Tuslah* (Jasa Profesi Apoteker) dan *Embalase* (Biaya Kemasan).

## 📦 Fase 6: Manajemen Rantai Pasok (Gudang Umum & Pengadaan)
Manajemen pergerakan barang medis dan non-medis sebelum didistribusikan.
- **Procurement (Pengadaan):** Alur Purchase Request (PR) dari ruangan hingga menjadi Purchase Order (PO) ke Supplier/PBF.
- **Penerimaan Barang & Faktur:** Pencatatan penerimaan barang, *expired date*, dan integrasi faktur ke Hutang Dagang (Account Payable).
- **Gudang Aset & Non-Medis:** Pengelolaan inventaris dapur, linen, ATK, dan alat kebersihan.

## 🛏️ Fase 7: Bedah Sentral (OK) & Rawat Inap (Ranap)
- **Bed Management Dashboard:** Monitoring visual sisa tempat tidur, status kamar (Kotor, Pembersihan, Tersedia, Terisi), dan mutasi pindah kamar pasien.
- **Modul Bedah Sentral:** Penjadwalan operasi (Booking OK), catatan laporan pembedahan, dan distribusi otomatis *Fee* operasi ke seluruh anggota tim.

## 👥 Fase 8: Sumber Daya Manusia (HRIS) & Remunerasi
- **Database Pegawai & Jadwal:** Data struktur organisasi RS, jadwal *shift* perawat, dan jadwal praktik dokter.
- **Fee-for-Service Aggregation:** Sistem secara otomatis menghitung *Insentif Jasa Medis* setiap dokter per akhir bulan berdasarkan semua tindakan, resep, dan operasi yang dilakukannya.

## 💰 Fase 9: Kasir, Keuangan & Akuntansi (Core ERP)
Tahap akhir dari seluruh putaran data klinis dan operasional.
- **Kasir Sentral (Billing):** Menyatukan tagihan Pendaftaran, Tindakan Poli, Obat, Lab, dan Rawat Inap ke dalam satu Nota Final. *Auto-numbering generator* akan diproteksi agar kebal dari tabrakan transaksi.
- **Account Receivable (Piutang):** Manajemen tagihan yang ditangguhkan ke BPJS atau Asuransi Swasta, termasuk pencatatan pembayaran klaim (pelunasan piutang).
- **Auto-Posting Jurnal (GL):** Setiap rupiah yang diketik kasir, atau obat yang keluar dari apotek, otomatis menjurnal dirinya sendiri (Debit & Kredit) ke dalam Buku Besar (General Ledger).
- **Laporan Keuangan:** Laba/Rugi (*Income Statement*), Neraca (*Balance Sheet*), dan Laporan Arus Kas secara *real-time*.

---
*Roadmap ini merupakan dokumen hidup yang akan terus diperbarui seiring dengan implementasi sistem di lapangan.*

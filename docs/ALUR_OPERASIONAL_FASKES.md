# Buku Peta Alur Operasional Fasilitas Kesehatan (Faskes)
*Dokumen ini merupakan referensi utama (Golden Reference) dalam merancang arsitektur ERP SIMRS, klinik, maupun Puskesmas. Semua alur divalidasi dengan standar pelayanan Kemenkes (termasuk Integrasi Pelayanan Primer - ILP).*

---

## 1. Pendaftaran & Front Office (Titik Awal)
Berlaku untuk RS, Klinik, maupun Puskesmas.
- **Pasien Mandiri/Umum:**
  - Pasien datang mengambil nomor antrean (bisa via mesin KiosK/APM).
  - Menuju loket, petugas mengecek identitas (KTP) dan *history* RM (Rekam Medis) jika pasien lama.
  - Pasien memilih Poli tujuan. Petugas menerbitkan karcis/bukti pendaftaran. 
  - Status tagihan pendaftaran di Kasir menjadi `Belum Lunas`.
- **Pasien BPJS/Asuransi:**
  - Identitas divalidasi dan di-*bridging* dengan server BPJS (V-Claim) menggunakan rujukan dari faskes tingkat pertama.
  - Jika aktif, terbit SEP (Surat Eligibilitas Peserta). Tagihan pendaftaran dialihkan ke piutang asuransi.

## 2. Poliklinik & Rawat Jalan (Core Pelayanan)
Berlaku untuk RS Umum, Klinik Spesialis, dan Puskesmas. Di Puskesmas modern, poli dibagi berdasarkan Klaster Siklus Hidup (ILP).
- **Skrining (Triage Dasar):** Perawat memanggil pasien, mengecek TTV (Tanda Vital: tensi, suhu, berat badan) dan mencatat asesmen awal keperawatan di EMR.
- **Pemeriksaan Dokter (Anamnesis & Diagnosa):** 
  - Dokter memanggil pasien. Jika Poli Gigi, dokter mengisi *Odontogram*. Jika Kandungan, dokter mengisi data USG/GPA.
  - Dokter memasukkan kode penyakit ICD-10/ICD-9CM.
- **CPOE (Computerized Provider Order Entry):**
  - Jika butuh obat: Dokter meresepkan *e-resep* ke Farmasi.
  - Jika butuh cek darah: Dokter menekan tombol *Order Lab*.
  - Jika butuh foto tulang: Dokter menekan tombol *Order Radiologi*.
- Pasien keluar poli. Status antrean poli menjadi `Selesai`.

## 3. Instalasi Gawat Darurat (IGD) - (Unit Sangat Vital)
Kecepatan adalah kunci, administrasi bisa menyusul.
- **Triage:** Pasien datang, langsung diberi label warna (Merah = Kritis, Kuning = Darurat, Hijau = Tidak Darurat, Hitam = Meninggal).
- **Tindakan Cepat:** Dokter jaga IGD langsung memberikan tindakan penanganan nyawa tanpa harus menunggu pasien mendaftar di loket depan.
- **Administrasi Menyusul:** Keluarga pasien mengurus pendaftaran IGD. Sistem harus mengizinkan *billing* menggantung sampai pasien stabil (atau dirujuk ke Rawat Inap/ICU).

## 4. Laboratorium & Radiologi (Penunjang Medis)
- **Registrasi Penunjang:** Pasien datang membawa *order* dari Poli/IGD. Atau pasien datang sendiri dari luar (APS - Atas Permintaan Sendiri).
- **Pengambilan Sampel / Eksekusi:** Petugas lab mengambil darah; Radiografer mengambil foto rontgen.
- **Input Hasil / Expertise:** Analis menginput angka lab; Mesin lab modern mengirim data otomatis via HL7. Dokter Spesialis Patologi/Radiologi memvalidasi hasil dan membuat *Expertise*.
- **Integrasi ERP:** Begitu hasil divalidasi, tagihan otomatis terkirim ke Kasir, dan hasil digital langsung muncul di layar EMR dokter perujuk.

## 5. Instalasi Farmasi & Apotek
- **Telaah Resep:** Apoteker menerima *e-resep* dan mengecek keamanan klinis (alergi, interaksi obat).
- **Peracikan (Dispensing):** Asisten apoteker mengambil obat, meracik puyer/kapsul, dan mencetak etiket (aturan pakai).
- **Integrasi Stok:** Sistem memotong stok fisik `gudangbarang` pada detik obat diserahkan, mengalkulasi FIFO, dan mencatat mutasi *ledger*. Harga *Tuslah* dan *Embalase* ditambahkan ke *billing*.
- **Penyerahan Obat (PIO):** Apoteker memanggil pasien, memberikan edukasi obat, lalu pasien menyerahkan bukti lunas dari Kasir (jika Pasien Umum).

## 6. Rawat Inap & Bed Management
- **Admisi (SPRI):** Pasien membawa Surat Perintah Rawat Inap. Petugas mengecek ketersediaan kasur (Bed Management) dan mem-*booking* kamar.
- **CPPT Harian:** Perawat melakukan *visite* setiap shift (pagi/siang/malam) untuk memonitor TTV, infus, dan pemberian obat injeksi. Dokter spesialis melakukan *visite* dan mencatat perkembangan (SOAP) harian.
- **Pemulangan (Discharge):** Dokter mengizinkan pulang. Admin ruangan merekap seluruh biaya (ruangan, obat, dokter) lalu menekan tombol *Discharge*.

## 7. Bedah Sentral (Kamar Operasi / OK)
- **Booking & Jadwal:** Poli/Ranap mengirim permintaan operasi. Kepala OK mengatur jadwal dan tim medis.
- **Pelaksanaan Operasi:** Pasien masuk ruang pra-operasi. Tindakan dilakukan. Sistem mencatat *Laporan Operasi* dan *Laporan Anestesi*.
- **Distribusi Billing:** Jasa operasi secara otomatis membelah tagihan menjadi porsi untuk Operator Utama, Asisten, Dokter Anestesi, dan Perawat (Instrumen/Omloop) berdasarkan master Paket Operasi.

## 8. Kasir & Keuangan Akuntansi
- **Pembayaran Terpusat:** Pasien Umum ke kasir untuk membayar total tagihan (Daftar + Poli + Lab + Obat + Ranap).
- **Auto-Jurnal (GL):** Setiap rupiah yang diterima mencetak *Kwitansi/Nota* yang unik secara konkuren. Nilai ini masuk ke jurnal debet/kredit secara *real-time*.
- **Klaim Asuransi (Piutang):** Untuk BPJS, tagihan tidak ditagihkan ke pasien, melainkan dibungkus menjadi *file TXT* INA-CBG untuk diklaimkan ke pemerintah tiap bulan.

## 9. Gudang Medis & Gudang Umum (Supply Chain)
- **Gudang Medis (Farmasi Induk):** Mengelola rantai pasok obat dari PBF (Pedagang Besar Farmasi) -> Gudang Utama -> Depo Rawat Jalan -> Depo Ranap -> Depo IGD.
- **Gudang Umum / Aset:** Menerima barang non-medis (Kertas, ATK, Sabun). Bangsal/Poli membuat *Permintaan Barang*. Gudang menyetujui dan memutasi barang ke ruangan tersebut.

## 10. CSSD (Sterilisasi Sentral) & Laundry
- **CSSD:** Semua instrumen bekas operasi dan tindakan poli dikumpulkan, dicuci, dan disterilkan menggunakan *autoclave* di CSSD. Sistem melacak stok instrumen steril yang tersedia.
- **Laundry / Linen:** Perawat Ranap mendata jumlah seprai, selimut, dan sarung bantal kotor setiap pagi, lalu ditimbang dan diserahkan ke Laundry.

## 11. Instalasi Gizi (Dapur)
- **Ahli Gizi:** Mengecek instruksi diet dari dokter di EMR (misal: Rendah Garam, Lunak, DM).
- **Produksi & Distribusi:** Dapur memproduksi makanan, menempelkan *label diet* per nama pasien, dan mendistribusikannya ke seluruh kamar rawat inap tepat waktu (Pagi/Siang/Malam).

## 12. HRD (Manajemen Pegawai) & Jasa Medis
- Mencatat absensi (integrasi mesin sidik jari).
- Menghitung lembur perawat.
- Menghitung **Fee for Service** bulanan dokter secara dinamis dari tarikan data tindakan medis yang mereka lakukan di Poli/OK/Ranap bulan tersebut, yang akan masuk menjadi *Payroll*.

## 13. IPSRS, Keamanan & Pengolahan Limbah (Unit Pendukung Teknis)
Meskipun sering dianggap "belakang layar", perannya kritikal jika rusak.
- **IPSRS (Pemeliharaan):** Perawat membuat tiket keluhan "AC Poli Anak Mati" atau "Monitor EKG Rusak". Teknisi merespons tiket dan mencatat *spare-part* yang digunakan dari Gudang Umum.
- **Kamar Jenazah:** Administrasi pengeluaran jenazah, pembuatan Surat Kematian, pelayanan *freezer*, dan penagihan biaya ambulans jenazah.
- **Limbah Medis B3:** Pencatatan berat limbah harian (jarum suntik, perban darah) untuk dilaporkan ke Kementerian LHK.
- **Parkir & Keamanan:** Integrasi karcis parkir berbayar (khusus RS besar) ke arus kas non-medis.

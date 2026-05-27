# Master Plan Digitalisasi & Pemetaan Tarif SIMRS

Rencana strategis untuk mengintegrasikan dan digitalisasi seluruh modul pelayanan (Umum & BPJS) yang bertumpu pada **Buku Tarif Master (Jasa Medis, Jasa Sarana, BHP)** dan aliran data dari *front-office* hingga *back-office* (Keuangan).

## Open Questions / Klarifikasi Kebutuhan
1. **Diferensiasi Tarif**: Apakah rumah sakit menggunakan sistem **satu tabel tarif** (`jns_perawatan`) yang sama, lalu nilai tagihan diklaim terpisah berdasarkan jenis bayar (Umum vs BPJS), atau memang ada **kode tindakan/tarif yang benar-benar terpisah** antara BPJS dan Umum di database?
2. **Integrasi Gudang Farmasi vs Umum**: Apakah `gudangbarang` saat ini mencakup semua jenis barang medis maupun non-medis (ATK, Linen, Dapur), atau diperlukan arsitektur terpisah untuk Gudang Umum/Aset?
3. **Akuntansi Kasir**: Apakah *Chart of Accounts* (Rekening Jurnal) sudah baku dari divisi keuangan, atau kita perlu mendefinisikan COA standar baru di dalam tabel `rekening`?

## Fase Pengembangan (Roadmap Fitur)

Karena cakupan ekspansi sangat masif (menyerupai migrasi ERP penuh), rencana ini dibagi menjadi beberapa *Milestones* agar pengembangan terukur dan berisiko rendah.

### Tahap 1: Modul Buku Tarif Dasar (Core Pricing Engine)
Modul ini adalah jantung dari semua layanan. Jika tarif salah, maka seluruh tagihan Kasir dan klaim BPJS akan bocor.
- **Backend (`tarif.module.ts`)**: Pengelola CRUD terpusat untuk `jns_perawatan`, `jns_perawatan_lab`, `jns_perawatan_radiologi`, dan `paket_operasi`.
- **Frontend (`MasterTarif.tsx`)**: Layar admin untuk membagi/merakit komponen tarif (Jasa Dokter, Jasa RS, BHP) yang berlaku untuk asuransi dan pasien mandiri.

### Tahap 2: Administrasi Pelayanan (Radiologi, Lab, Bedah, Poli)
Setiap tindakan memanggil API Buku Tarif dari Tahap 1.
- **Radiologi (`radiologi.module.ts`)**: Mengelola antrean (`antriradiologi`), form keahlian (*expertise*), dan penagihan radiologi ke kasir. Frontend baru: `Radiologi.tsx`.
- **Laboratorium**: Integrasi *billing* lab (APS/Rujukan) dan validasi `template_laboratorium`.
- **Bedah Sentral**: Integrasi dengan pembagian alokasi insentif tim operasi (Operator, Anastesi, Asisten, dsb).
- **Poliklinik Administrasi**: Mengakomodasi *billing* tindakan poliklinik terintegrasi.

### Tahap 3: Modul Farmasi Digital & Buku E-Resep
- **Stok & Ledger**: Mengaktifkan *Pessimistic Lock* untuk memotong stok riil dari `gudangbarang` dan membukukan *ledger* di `riwayat_barang_medis`.
- **E-Resep (`BukuResepDigital.tsx`)**: Dasbor khusus untuk apoteker melakukan telaah E-Resep, verifikasi stok, cetak etiket digital, dan penyerahan obat (rekonsiliasi ke kasir).

### Tahap 4: Modul Gudang Umum & Pengadaan
- **Supply Chain (`gudang-umum.module.ts`)**: Modul pengadaan (PO), penerimaan faktur, dan distribusi barang Non-Medis (ATK, Alkes Non-Farmasi, Linen) antar instalasi/ruangan.
- **Frontend (`GudangUmum.tsx`)**: Dasbor mutasi dan inventarisasi *General Store*.

### Tahap 5: Manajemen Pegawai & HRIS
- **Data SDM (`pegawai.module.ts`)**: Modul agregasi data `pegawai` dan `dokter` untuk pengaturan departemen, jadwal kerja operasional, dan komisi/remunerasi otomatis dari tindakan medis.
- **Frontend (`ManajemenPegawai.tsx`)**: Portal admin SDM Rumah Sakit.

### Tahap 6: Keuangan & Akuntansi Sentral (General Ledger)
- **Auto-Posting Kasir**: Finalisasi pencatatan otomatis ke `jurnal` dan `detailjurnal` secara presisi absolut menggunakan mekanisme *database transactions*.
- **Dasbor Keuangan (`KeuanganAkuntansi.tsx`)**: Laporan Laba-Rugi agregat, Buku Besar, monitoring arus Kas, dan manajemen Piutang (BPJS/Asuransi Lain).

## Rencana Validasi (End-to-End Workflow)
1. **Flow Jasa Poli & Penunjang**: Mensimulasikan pasien mendaftar Poli -> Dokter *order* tindakan berbayar -> Dokter memesan foto Rontgen & Uji Darah -> Perawat memasukkan layanan EKG. Memastikan semua *item* tersebut mengambil harga yang presisi dari **Buku Tarif Tahap 1**.
2. **Flow Apotek**: Dokter membuat E-Resep -> Apoteker meracik obat -> Stok obat fisik berkurang tepat sesuai dengan satuan terkecil.
3. **Flow Kasir & Keuangan**: Pasien (Umum) membayar tagihan di Kasir -> Nota tercetak dengan nomor unik terproteksi -> Pada panel Keuangan, nilai pendapatan bertambah dan jurnal Debit=Kredit terbalans otomatis.

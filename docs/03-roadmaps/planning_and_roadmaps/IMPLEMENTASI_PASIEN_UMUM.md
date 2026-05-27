# Perencanaan Implementasi Fungsional Pasien Umum (SIMRS Web)

Dokumen ini merinci rencana implementasi sistem untuk menangani alur pelayanan "Pasien Umum" (pembayaran mandiri/out-of-pocket).

## 1. Latar Belakang dan Tujuan
Pasien umum tidak menggunakan jaminan BPJS, sehingga alurnya lebih menitikberatkan pada kelancaran dan keamanan transaksi finansial di kasir, serta akurasi pemotongan stok di farmasi. Berdasarkan evaluasi dari `docs/04-status/project_management_and_logs/CURRENT_STATE.md` dan `docs/04-status/project_management_and_logs/Build_Summary.md`, beberapa modul saat ini hanya prototipe dan berisiko tinggi (terutama *race condition* di Kasir dan tidak adanya pemotongan inventori Farmasi).

## 2. Rencana Perubahan Modul

### A. Modul Pendaftaran (Front Office)
* **Kondisi Saat Ini:** Pendaftaran BPJS memicu pembuatan simulasi SEP.
* **Perubahan Pasien Umum:**
  * Memastikan logika pendaftaran membedakan pasien Umum dan BPJS berdasarkan `kd_pj` (Penanggung Jawab).
  * Bypass alur SEP/Casemix untuk pasien umum.
  * *Default* `status_bayar` pada `reg_periksa` menjadi `Belum_Bayar`.
  * Memasukkan tarif pendaftaran poli ke dalam tagihan Kasir.

### B. Modul Kasir & Keuangan (Prioritas Kritis)
* **Kondisi Saat Ini:** *Auto-numbering* `no_nota` dan `no_jurnal` rawan *collision* (*race condition*).
* **Perubahan Pasien Umum:**
  * Pasien umum akan membayar langsung seluruh tagihan (Ralan, Ranap, Farmasi, Lab, OK).
  * **Pengamanan Transaksi:** Mengimplementasikan *Pessimistic Locking* (`SELECT ... FOR UPDATE`) pada pembuatan `no_nota` dan `no_jurnal` menggunakan mekanisme raw query Prisma jika diperlukan, untuk memastikan keunikan nomor di sistem concurrent.
  * **Pencatatan Jurnal:** Memastikan keseimbangan Debit (Kas) dan Kredit (Pendapatan/Piutang) pada `jurnal` dan `detailjurnal`.
  * Update `reg_periksa` menjadi `Sudah_Bayar` secara aman dalam satu scope transaksi.

### C. Modul Farmasi & Apotek
* **Kondisi Saat Ini:** Modul prototipe belum memotong stok fisik `gudangbarang` secara akurat, dan nilai `embalase`/`tuslah` bersifat tetap.
* **Perubahan Pasien Umum:**
  * Menerapkan kalkulasi riil untuk biaya obat, `embalase`, dan `tuslah` (mengambil dari referensi master atau *setting*).
  * **Mutasi Stok:** Menerapkan transaksi database yang mengunci `gudangbarang`, memotong `stok`, dan mencatat riwayat ke `riwayat_barang_medis` saat resep diserahkan (`detail_pemberian_obat`).

### D. Modul Laboratorium & Operasi
* **Kondisi Saat Ini:** Belum dilindungi JWT Guard, namun billing sudah tergabung ke kasir.
* **Perubahan Pasien Umum:**
  * Menambahkan validasi Guard JWT dan RBAC pada *endpoints* ini agar pendaftaran tindakan Pasien Umum tetap aman.
  * Tagihan tindakan langsung diteruskan secara *real-time* ke sistem Kasir.

## 3. Langkah Implementasi
1. **Perbaikan Backend Kasir:** Refaktor `KasirService` untuk membungkus `nota_jalan` dan `jurnal` di dalam Prisma `$transaction` dengan optimasi konkurensi (atau locking table ID).
2. **Perbaikan Backend Farmasi:** Refaktor proses `serahkan` di `FarmasiService` agar melakukan operasi kurangi stok secara ACID.
3. **Penyempurnaan Pendaftaran:** Sesuaikan kondisi pemanggilan SEP.
4. **Testing:**
   - Melakukan simulasi beban (parallel requests) pada Kasir untuk membuktikan *race condition* hilang.
   - Uji transaksi apotek dan pengecekan akhir `gudangbarang` pasien umum.

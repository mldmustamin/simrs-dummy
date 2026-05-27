> **Status**: *On-going modul (Cetak Biru Masa Depan)*

Keuangan & Akuntansi
=========================================
**Dokumen Arsitektur & Alur Kerja**

## 1. Deskripsi Eksekutif
Buku Besar, Jurnal Umum, Laba/Rugi, Neraca. Seluruh transaksi RS bermuara di sini.

## 2. Aktor & Hak Akses
- Akuntan, Direktur Keuangan

## 3. Alur Perjalanan Pasien (Patient Journey)
1. Penerimaan Kasir -> Jurnal Pendapatan.
2. Pembelian Obat -> Jurnal Hutang (A/P).
3. Klaim BPJS -> Jurnal Piutang (A/R).
4. Pembayaran Gaji -> Jurnal Beban Gaji.

## 4. Alur Perjalanan Sistem (ERP Data Lifecycle)
- Sistem melakukan Auto-Posting secara diam-diam (Background).
- Konsolidasi laporan real-time tanpa tutup buku bulanan yang membosankan.

## 5. Implementasi Multi-Model (Arsitektur Fallback)
- **Standar Ideal (Enterprise)**: Rekonsiliasi Bank Otomatis (Host-to-Host) membaca mutasi rekening BCA/Mandiri RS.
- **Skenario Pragmatis (Fallback)**: Akuntan tetap bisa melakukan Jurnal Penyesuaian Manual (Manual Entry) jika ada kas kecil (Petty Cash) yang selisih.

## 6. Titik Integrasi & Bridging Eksternal
- Sistem Perbankan (Opsional).

## 7. Penanganan Bencana & Edge Cases
- ⚠️ **Skenario Ekstrem**: Selisih kurs valuta asing saat membeli mesin MRI dari Jerman. Sistem mengakomodasi perhitungan laba/rugi kurs.

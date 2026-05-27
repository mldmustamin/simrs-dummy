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

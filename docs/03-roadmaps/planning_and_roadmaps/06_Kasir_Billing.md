Kasir & Billing Sentral
=========================================
**Dokumen Arsitektur & Alur Kerja**

## 1. Deskripsi Eksekutif
Muara dari seluruh beban biaya pasien (Konsolidasi Invoice).

## 2. Aktor & Hak Akses
- Petugas Kasir, Direktur Keuangan

## 3. Alur Perjalanan Pasien (Patient Journey)
1. Pasien datang membawa nomor RM.
2. Kasir memverifikasi rincian tagihan dari Poli, Lab, Obat, dan Tindakan.
3. Menerima pembayaran Tunai/EDC/QRIS.
4. Menerbitkan Kwitansi Lunas dan Surat Bebas Tanggungan.

## 4. Alur Perjalanan Sistem (ERP Data Lifecycle)
- Menembakkan event `Kasir.Lunas` yang melepaskan penahanan pasien pulang.
- Auto-posting debet Kas dan kredit Pendapatan ke tabel Jurnal.

## 5. Implementasi Multi-Model (Arsitektur Fallback)
- **Standar Ideal (Enterprise)**: Pasien membayar mandiri via KiosK menggunakan QRIS Dinamis.
- **Skenario Pragmatis (Fallback)**: Emergency Override: Pasien tidak punya uang. Direktur memasukkan PIN Otorisasi Khusus untuk mem-bypass sistem agar pasien bisa pulang (Bad Debt).

## 6. Titik Integrasi & Bridging Eksternal
- Payment Gateway (Moota/Midtrans).

## 7. Penanganan Bencana & Edge Cases
- ⚠️ **Skenario Ekstrem**: Mesin EDC mati lampu di tengah swipe. Sistem Kasir dapat mengecek status Suspended Transaction.

# Modul Operasi (IBS)

Jadwal pembedahan (`Operasi.tsx`).

## Parameter Teknis & Endpoint
- **Katalog Paket Operasi**: `GET /operasi/paket`
- **Input Laporan Operasi**: `POST /operasi/input`

## Mekanisme Sistem
Petugas memilih jenis paket operasi yang menentukan biaya dasar. Tagihan kemudian diekskalasi ke dalam sistem billing kasir secara otomatis sesuai kode paket di tabel `paket_operasi`.

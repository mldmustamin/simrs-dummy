# Modul Apotek (Pelayanan)

Penyerahan obat dan penjualan OTC (`Apotek.tsx`).

## Parameter Teknis & Endpoint
- **Antrean E-Resep (Tunggu Serah)**: `GET /farmasi/antrean-resep`
- **Daftar Depo Aktif**: `GET /farmasi/depo`
- **Master Obat (OTC)**: `GET /farmasi/obat?keyword={keyword}`
- **Jual Bebas**: `POST /farmasi/resep-bebas`
- **Finalisasi & Serah Obat**: `POST /farmasi/serahkan`

## Mekanisme Sistem
Sistem Farmasi memegang proteksi *Financial Lock*. Pada *endpoint* `/farmasi/serahkan`, backend memeriksa tabel `reg_periksa.status_bayar`. Jika `"Belum_Bayar"` (untuk pasien Umum), tombol serah UI dikunci, API merespon 403 Forbidden. Saat obat bebas dijual, mekanisme *Row-Level Locking* (`SELECT ... FOR UPDATE`) menjaga agar stok `gudangbarang` tidak berkurang melebihi batas. Log mutasi diisi nama Apoteker dari Token JWT.

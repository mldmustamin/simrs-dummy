# Modul Farmasi (Gudang & Peracikan)

Penyusunan E-Resep dan inventory (`Farmasi.tsx`).

## Parameter Teknis & Endpoint
- **Pencarian Obat**: `GET /farmasi/obat?keyword={keyword}`
- **Cek Stok Fisik**: `GET /farmasi/stok?kode_brng={kode_brng}`
- **Metode Racik**: `GET /farmasi/metode-racik`
- **Penyusunan Resep**: `POST /farmasi/resep`

## Mekanisme Sistem
Apoteker/Farmasis menarik data stok secara real-time dari relasi tabel `databarang` dan `gudangbarang`. Obat dapat dikonversi ke dalam resep racikan (puyer/kapsul) dengan metode yang ditentukan, lalu disimpan dalam tabel `resep_obat` dan rinciannya di `resep_dokter`.

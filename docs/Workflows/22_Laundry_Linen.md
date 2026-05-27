# Workflow Modul Laundry & Manajemen Linen
> **Status**: *On-going modul*

## 1. Deskripsi Umum
Pengelolaan perputaran linen (sprei, selimut, baju operasi) yang kotor, infeksius, hingga kembali bersih.

## 2. Aktor Terlibat
- Petugas Laundry

## 3. Alur Kerja (Ideal & Fallback)
1. **Penimbangan Kotor:** Linen kotor dari bangsal dibawa dan ditimbang (Kg). Dipisah antara bak Infeksius (Merah) dan Non-Infeksius.
2. **Pencucian:** Mesin dioperasikan, ERP mencatat penggunaan deterjen kimia harian dari gudang linen.
3. **Distribusi Bersih:** Linen bersih disimpan ke lemari penyimpanan. Ruangan menarik (*Request*) stok linen bersih via ERP.

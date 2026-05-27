# Workflow Modul Gudang Logistik (Supply Chain)
## 1. Deskripsi Umum
Rantai pasok (pembelian, penerimaan, dan distribusi) obat dan alat medis ke seluruh rumah sakit.

## 2. Aktor Terlibat
- Kepala Gudang
- Staf Logistik / Purchasing

## 3. Alur Kerja (Ideal & Fallback)
1. **Purchase Request (PR):** Depo/Poli meminta barang yang mulai menipis.
2. **Purchase Order (PO):** Purchasing menerbitkan PO ke Vendor/PBF.
3. **Goods Receipt (Penerimaan):** Barang tiba. Staf gudang menginput jumlah, Harga Beli, Nomor Batch, dan Tanggal Kadaluarsa (Expired Date). Stok Utama bertambah.
4. **Distribusi / Mutasi:** Stok didistribusikan ke depo apotek Ranap/IGD.
5. **Stock Opname:** Penyesuaian stok sistem dengan stok fisik bulanan (pencatatan barang hilang/rusak).

## 4. Trigger & Integrasi
- **Menembak Event:** `Logistik.PenerimaanSelesai` -> Memicu Modul Hutang Dagang (A/P) di Akuntansi, meng-update HPP (Harga Pokok Penjualan) dengan kalkulasi *Moving Average* atau FIFO.

Logistik & Gudang Umum
=========================================
**Dokumen Arsitektur & Alur Kerja**

## 1. Deskripsi Eksekutif
Manajemen Supply Chain. Rantai penerimaan barang dari vendor hingga distribusi ke ruangan.

## 2. Aktor & Hak Akses
- Kepala Gudang, Purchasing

## 3. Alur Perjalanan Pasien (Patient Journey)
1. Pembuatan Purchase Request (PR) dari ruangan.
2. Purchasing mengubah PR menjadi Purchase Order (PO) ke PBF.
3. Barang datang. Petugas Gudang melakukan Goods Receipt (GR), mengecek Faktur.
4. Distribusi barang ke depo-depo rumah sakit.

## 4. Alur Perjalanan Sistem (ERP Data Lifecycle)
- Kalkulasi Harga Pokok Penjualan (HPP) menggunakan Moving Average.
- Pencatatan Nomor Batch dan Tanggal Kadaluarsa mutlak diwajibkan.

## 5. Implementasi Multi-Model (Arsitektur Fallback)
- **Standar Ideal (Enterprise)**: Auto-Restock. Sistem menembak email PO otomatis ke vendor jika stok menyentuh titik Minimum (Buffer).
- **Skenario Pragmatis (Fallback)**: Vendor kirim barang hanya setengah dari PO. Sistem melakukan Partial Receipt dan mengkalkulasi ulang sisa hutang (Account Payable).

## 6. Titik Integrasi & Bridging Eksternal
- E-Faktur Pajak.

## 7. Penanganan Bencana & Edge Cases
- ⚠️ **Skenario Ekstrem**: Pabrik Oksigen cair meledak. Alarm sistem menyala merah ketika Buffer Oksigen medis turun ke level kritis.

# Workflow Modul Bank Darah RS (BDRS)
> **Status**: *On-going modul*

## 1. Deskripsi Umum
Manajemen stok kantong darah, uji silang serasi (Crossmatch), dan donor pengganti.

## 2. Aktor Terlibat
- Petugas BDRS

## 3. Alur Kerja (Ideal & Fallback)
1. **Request Darah:** Dokter operasi / IGD memesan 2 kantong PRC via sistem (Gol. Darah B).
2. **Pengadaan:** Jika stok kosong, petugas menerbitkan surat rujukan darah ke PMI secara sistem.
3. **Crossmatch:** Sampel darah pasien diuji silang dengan kantong darah di lab. Hasil diinput ke ERP.
4. **Distribusi:** Kantong darah dengan *barcode* diambil perawat bangsal. Tagihan biaya pengolahan darah otomatis masuk ke kasir.

# Workflow Modul Instalasi Gizi & Dapur Sentral
> **Status**: *On-going modul*

## 1. Deskripsi Umum
Memastikan asupan gizi pasien rawat inap sesuai dengan instruksi klinis dokter, mencatat pemakaian bahan mentah dapur harian, serta melacak alergi makanan.

## 2. Aktor Terlibat
- Ahli Gizi (Dietisien)
- Koki / Petugas Dapur RS

## 3. Alur Kerja (Ideal & Fallback)
1. **Penerimaan Order Diet:** Sistem menarik instruksi diet dari EMR Rawat Inap secara *real-time*.
2. **Kompilasi Kebutuhan (Pagi/Siang/Sore):** ERP menghitung otomatis total porsi Bubur, Nasi, Diet Rendah Garam, dll untuk satu rumah sakit.
3. **Pencetakan Barcode Nampan:** Nampan makanan dilabeli *barcode* yang berisi nama pasien, bangsal, dan peringatan alergi (misal: "Alergi Udang").
4. **Distribusi:** Makanan diantar ke bangsal.
5. **Inventaris Dapur:** Pengurangan stok bahan basah dan kering di Gudang Gizi.

## 4. Trigger & Integrasi
- **Menembak Event:** `Gizi.OrderSelesai`.

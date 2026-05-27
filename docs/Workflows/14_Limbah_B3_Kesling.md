# Workflow Modul Kesehatan Lingkungan (Kesling) & Limbah B3
> **Status**: *On-going modul*

## 1. Deskripsi Umum
Pencatatan harian volume sampah infeksius, non-infeksius, dan benda tajam, serta pelaporan vendor pengolah limbah.

## 2. Aktor Terlibat
- Petugas Sanitarian
- Vendor Pihak Ketiga

## 3. Alur Kerja (Ideal & Fallback)
1. **Penimbangan Harian:** Petugas menimbang kantong kuning (infeksius) dari tiap ruangan. Data berat (Kg) dimasukkan ke ERP.
2. **Penyimpanan di TPS B3:** Akumulasi volume limbah dihitung otomatis oleh sistem. Jika mendekati kapasitas maksimal TPS, alarm menyala.
3. **Pengangkutan Vendor:** Vendor (misal: PT. Waste) mengambil limbah. Serah terima (Manifest) dicetak dari sistem.

## 4. Trigger & Integrasi
- **Bridging:** SIRAJA Limbah (Sistem Informasi Pelaporan Pengelolaan Limbah B3 Kementerian LHK).

> **Status**: *On-going modul (Cetak Biru Masa Depan)*

Kesehatan Lingkungan (Limbah B3)
=========================================
**Dokumen Arsitektur & Alur Kerja**

## 1. Deskripsi Eksekutif
Pengelolaan limbah medis beracun dan pencatatan Manifest Pengangkutan pihak ketiga.

## 2. Aktor & Hak Akses
- Sanitarian, Vendor Limbah

## 3. Alur Perjalanan Pasien (Patient Journey)
1. Sanitarian menimbang limbah infeksius (kantong merah/kuning) harian per bangsal.
2. Limbah disimpan di TPS B3 RS.
3. Vendor datang, mengangkut, dan mencetak Surat Manifest.

## 4. Alur Perjalanan Sistem (ERP Data Lifecycle)
- Kalkulasi total timbulan limbah bulanan.
- Sistem menahan pembayaran tagihan vendor jika dokumen Manifest pemusnahan dari insinerator belum di-upload.

## 5. Implementasi Multi-Model (Arsitektur Fallback)
- **Standar Ideal (Enterprise)**: Timbangan limbah digital terkoneksi WiFi langsung ke database.
- **Skenario Pragmatis (Fallback)**: Penginputan angka berat limbah secara manual di penghujung hari operasional.

## 6. Titik Integrasi & Bridging Eksternal
- SIRAJA Limbah KLHK.

## 7. Penanganan Bencana & Edge Cases
- ⚠️ **Skenario Ekstrem**: Vendor telat datang 3 hari. TPS Overload. Sistem membangkitkan alarm bahaya infeksi silang ke Komite PPI.

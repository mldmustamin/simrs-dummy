# Workflow Modul Hemodialisa (Cuci Darah)
> **Status**: *On-going modul*

## 1. Deskripsi Umum
Layanan tindakan cuci darah rutin yang membutuhkan manajemen mesin (*Machine Utilization*) dan siklus kunjungan pasien kronis.

## 2. Aktor Terlibat
- Perawat Hemodialisa
- Dokter Spesialis Penyakit Dalam (KGH)

## 3. Alur Kerja (Ideal & Fallback)
1. **Penjadwalan Mesin:** Pasien gagal ginjal kronis dijadwalkan secara reguler (misal: tiap Selasa dan Jumat). Sistem mem-booking *slot* Mesin HD.
2. **Pre-Tindakan:** Pengukuran berat badan basah, tekanan darah.
3. **Intra-Tindakan:** Pencatatan *Ultrafiltration Rate*, BHP (Dialyzer, Bloodline), Heparin.
4. **Post-Tindakan:** Evaluasi klinis. Pengulangan otomatis rujukan internal BPJS (biasanya rujukan berlaku 3 bulan).

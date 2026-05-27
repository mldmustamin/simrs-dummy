# Workflow Modul IPSRS (Pemeliharaan Fasilitas & Elektro Medik)
> **Status**: *On-going modul*

## 1. Deskripsi Umum
Manajemen pemeliharaan gedung, AC, listrik, genset, serta kalibrasi rutin alat medis (Ventilator, Patient Monitor).

## 2. Aktor Terlibat
- Kepala IPSRS
- Teknisi / Mekanik

## 3. Alur Kerja (Ideal & Fallback)
1. **Sistem Tiket (Helpdesk):** Perawat Bangsal mengirim tiket keluhan (misal: "AC Bocor di Kamar 203").
2. **Penugasan (Dispatch):** Kepala IPSRS menugaskan teknisi. Tiket berubah status menjadi `In Progress`.
3. **Pemakaian Sparepart:** Teknisi mengambil suku cadang (Freon, Kabel) dari Gudang Teknik. Stok dipotong.
4. **Penyelesaian:** Teknisi memfoto bukti perbaikan dari aplikasi *mobile*. Status tiket menjadi `Closed`.
5. **Preventive Maintenance:** ERP membunyikan alarm jadwal kalibrasi alat medis yang akan jatuh tempo dalam 30 hari.

## 4. Trigger & Integrasi
- **Bridging:** ASPAK Kemenkes (Aplikasi Sarana Prasarana dan Alat Kesehatan).

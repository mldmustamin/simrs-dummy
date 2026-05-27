# Workflow Modul Rawat Inap (Bangsal)
## 1. Deskripsi Umum
Modul paling dinamis untuk manajemen bed, asuhan keperawatan 24/7 (SBAR, CPPT), pemberian obat (E-MAR), dan visite dokter.

## 2. Aktor Terlibat
- Kepala Ruangan
- Perawat Pelaksana (Shift)
- Dokter DPJP
- Petugas Gizi (Dietisien)

## 3. Alur Kerja (Ideal & Fallback)
1. **Admisi Ranap:** Pasien ditransfer dari IGD/Poli. Pemilihan Bed di modul Bed Management. Status kasur berubah menjadi `DITEMPATI`.
2. **Asesmen Awal & CPPT:** Perawat melakukan pengkajian awal. Semua entri dokter, perawat, dan ahli gizi digabungkan dalam satu *Timeline* (CPPT).
3. **Pemberian Obat (E-MAR):** Perawat menscan *barcode* obat dan *barcode* gelang pasien sebelum menyuntik untuk memastikan 7 Benar Obat.
4. **Visite Dokter:** Dokter menginput instruksi medis harian.
5. **Auto-Billing (Midnight Census):** Pada jam 00:00, ERP menagihkan biaya kamar otomatis.
6. **Discharge Planning:** Dokter menyatakan Boleh Pulang. Status bed berubah `DIRESERVE CLEANING`.

## 4. Trigger & Integrasi
- **Menembak Event:** `Ranap.PasienPulang` -> Memicu CSSD/Cleaning Service, memicu Kasir untuk *Closing Billing*.
- **Bridging:** SIRANAP Kemenkes (Ketersediaan Bed Real-time).

# Workflow Modul Kamar Jenazah & Forensik
> **Status**: *On-going modul*

## 1. Deskripsi Umum
Manajemen pemulasaraan jenazah, penyimpanan di lemari pendingin (freezer), visum, dan penyewaan ambulans jenazah.

## 2. Aktor Terlibat
- Dokter Forensik
- Petugas Kamar Jenazah
- Supir Ambulans

## 3. Alur Kerja (Ideal & Fallback)
1. **Penerimaan Jenazah:** Jenazah dikirim dari IGD/Ranap. Status Rekam Medis (RM) pasien dikunci menjadi `Meninggal/Deceased`.
2. **Pemulasaraan:** Tindakan memandikan, mengkafani/memakaikan baju, atau formalin dicatat di sistem.
3. **Sewa Freezer:** Jika keluarga belum mengambil, ERP menghitung sewa freezer per 24 jam.
4. **Penerbitan Surat:** Surat Keterangan Kematian dicetak dan ditandatangani digital.
5. **Keluar:** Ambulans dipesan via sistem Kasir. Jenazah dibawa pulang.

## 4. Trigger & Integrasi
- **Menembak Event:** `Jenazah.Keluar` -> Meng-update laporan mortalitas bulanan RS.

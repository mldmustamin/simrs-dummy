# Workflow Modul Kasir & Billing
## 1. Deskripsi Umum
Konsolidasi seluruh biaya layanan pasien (Tindakan, Bed, Obat, Lab) menjadi satu *invoice* terpusat.

## 2. Aktor Terlibat
- Petugas Kasir Sentral
- Administrasi Keuangan

## 3. Alur Kerja (Ideal & Fallback)
1. **Pengumpulan Biaya (Auto-Aggregation):** Sistem mengumpulkan seluruh biaya dari Poli, Lab, Apotek, dan Ranap secara *real-time* tanpa perlu di-entri ulang oleh Kasir.
2. **Validasi Final:** Kasir mengecek rincian tagihan akhir.
3. **Pembayaran:**
   - Pembayaran dilakukan via Tunai / EDC / QRIS / Transfer.
   - *Mode BPJS:* Tagihan dikalkulasi nol rupiah untuk pasien (diklaim ke INA-CBG). Jika ada naik kelas VIP, sistem menghitung *Cost Sharing* otomatis.
4. **Emergency Override (Mode Pragmatis):** Jika keluarga tidak bisa bayar, Direktur Keuangan dapat memasukkan *PIN Override* agar pasien boleh pulang (Piutang / Bad Debt).
5. **Cetak Bukti & Lunas:** Kuitansi dicetak, status pasien ditutup.

## 4. Trigger & Integrasi
- **Menembak Event:** `Kasir.PembayaranLunas` -> Memicu Modul Jurnal Akuntansi (Debet Kas, Kredit Pendapatan), melepas *lock* penahanan dokumen rekam medis.

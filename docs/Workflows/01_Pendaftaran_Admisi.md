# Workflow Modul Pendaftaran & Admisi
## 1. Deskripsi Umum
Modul ini adalah pintu masuk pertama pasien. Bertanggung jawab mencatat demografi, mencetak RM baru, mendistribusikan antrean ke Poli/IGD, dan menerbitkan SEP BPJS.

## 2. Aktor Terlibat
- Petugas Loket Pendaftaran
- Pasien / Keluarga Pasien
- KiosK Mandiri (Self-Service)

## 3. Alur Kerja (Ideal & Fallback)
1. **Identifikasi:** Pasien menyerahkan KTP/BPJS.
2. **Pencarian RM:** Sistem memvalidasi apakah NIK/No.BPJS sudah terdaftar. Jika belum, *Create RM Baru*.
3. **Pilih Layanan:** Petugas memilih Poli Tujuan dan Dokter.
4. **Validasi Finansial:**
   - *Tunai:* Generate tagihan karcis/pendaftaran awal di sistem Kasir.
   - *BPJS (Mode Ideal):* Tarik rujukan dari V-Claim, terbitkan SEP instan.
   - *BPJS (Mode Pragmatis):* Jika V-Claim timeout, bypass SEP, teruskan pendaftaran dengan `no_rawat` lokal, masukkan request SEP ke `Background Job`.
5. **Cetak Bukti:** Cetak karcis antrean Poli dan Tracer/Lembar Poli untuk Rekam Medis fisik (jika masih Hybrid).

## 4. Trigger & Integrasi
- **Menembak Event:** `Pendaftaran.Selesai` -> Memicu modul Poli (menambah daftar antrean) dan modul Kasir (membuka invoice baru).
- **Bridging:** V-Claim (SEP), Dukcapil (NIK).

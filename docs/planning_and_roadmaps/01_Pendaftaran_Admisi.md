Pendaftaran & Admisi (Front Office)
=========================================
**Dokumen Arsitektur & Alur Kerja**

## 1. Deskripsi Eksekutif
Titik nol perjalanan pasien. Bertanggung jawab atas pencatatan demografi, jaminan, dan distribusi antrean ke poli atau rawat inap.

## 2. Aktor & Hak Akses
- Petugas Pendaftaran, Supervisor Front Office, KiosK Mandiri

## 3. Alur Perjalanan Pasien (Patient Journey)
1. Pasien mengambil tiket dari mesin antrean atau daftar online via Mobile JKN.
2. Petugas memverifikasi identitas (KTP/Sidik Jari) dan Jaminan (BPJS/Asuransi Swasta).
3. Sistem membuat/menarik Rekam Medis (RM) pasien.
4. Sistem menerbitkan nomor antrean Poli tujuan dan mengarahkan pasien.

## 4. Alur Perjalanan Sistem (ERP Data Lifecycle)
- Generate `no_rawat` berdasarkan urutan poli per hari.
- Insert data ke `reg_periksa` dengan status `Belum Diperiksa`.
- Memicu invoice awal di modul `Kasir`.

## 5. Implementasi Multi-Model (Arsitektur Fallback)
- **Standar Ideal (Enterprise)**: Koneksi V-Claim BPJS merespons < 1 detik. SEP digital terbit otomatis. Fingerprint langsung tervalidasi.
- **Skenario Pragmatis (Fallback)**: V-Claim Timeout. Sistem menyimpan antrean secara lokal, mengizinkan pasien langsung ke poli, dan memasukkan request SEP ke `Background Job` untuk di-retry 50x.

## 6. Titik Integrasi & Bridging Eksternal
- BPJS (V-Claim), Dukcapil (NIK), Mobile JKN.

## 7. Penanganan Bencana & Edge Cases
- ⚠️ **Skenario Ekstrem**: Pasien gawat darurat tanpa identitas (Mr. X) masuk. Sistem men-generate RM sementara yang bisa di-merge di kemudian hari.

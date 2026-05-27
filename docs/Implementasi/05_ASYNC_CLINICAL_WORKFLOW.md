# Panduan Input Asuhan Klinis Asinkron (Retrospektif)
*Panduan teknis untuk menangani kekacauan input dokter/perawat di dunia nyata.*

## 1. Retrospective Data Entry (Pencatatan Mundur)
Sistem harus memfasilitasi dokter IGD atau perawat ICU yang baru sempat membuka komputer di penghujung *shift* kerja mereka.
- Form *EMR / SOAP* di frontend harus memiliki *field* **Jam Tindakan Real** yang bisa diedit mundur oleh perawat secara manual.
- Backend tetap menyimpan `created_at` (jam *server* menyimpan data) untuk menghindari sengketa medikolegal, namun data yang dicetak pada rekam medis fisik/PDF adalah *Jam Tindakan Real* yang diinput.

## 2. Mekanisme Addendum & Revisi EMR
Mengingat kebiasaan "Copy-Paste", kesalahan input pasti terjadi. EMR tidak boleh dikunci absolut tanpa mekanisme revisi yang legal.
- Jika dokumen telah di-TTE (Tanda Tangan Elektronik), maka dokumen terkunci.
- Jika ada perbaikan setelah di-TTE, sistem harus menggunakan mekanisme **Addendum**. Data lama tidak dihapus, melainkan ditumpuk/ditambahkan catatan koreksi dengan penanda waktu baru (menganut kaidah *Write-Once-Read-Many / WORM*).

## 3. Penerimaan Resep Lisan (Verbal Order)
- Apoteker dapat membuat `Draft Resep` tanpa otorisasi digital dokter untuk melayani pasien darurat yang nyawanya terancam (atas perintah lisan/telepon dokter).
- Draft ini dibiarkan menggantung di *dashboard* dokter. Dokter memiliki kewajiban (dan notifikasi *reminder* berkala) untuk me-klik tombol "Validasi Resep Lisan" maksimal dalam waktu 1x24 jam setelah kejadian.

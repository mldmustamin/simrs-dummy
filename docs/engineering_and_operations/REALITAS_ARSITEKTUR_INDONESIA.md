# Arsitektur Pragmatis SIMRS: Menghadapi Realitas Faskes Indonesia

Dokumen ini lahir dari tamparan realitas lapangan. Rancangan *Enterprise* yang terlalu idealis, tersinkronisasi ketat (*hard real-time*), dan mengandalkan konektivitas sempurna **akan hancur** ketika dihadapkan pada realitas operasional di banyak RSUD dan Puskesmas daerah di Indonesia.

Tantangan utama HIS (Hospital Information System) di Indonesia bukanlah **"bagaimana membuat sistem canggih"**, melainkan **"bagaimana membuat sistem tetap hidup di tengah kekacauan operasional nyata."**

Oleh karena itu, ERP ini akan mengadopsi 7 Pilar Arsitektur Pragmatis:

## 1. Offline-First Architecture (Bukan Cloud-First)
- **Kondisi Nyata:** Internet mati, listrik byar-pet, switch jaringan *unmanaged*.
- **Solusi Arsitektur:** 
  - Aplikasi *Frontend* (PWA/Local Worker) harus bisa beroperasi mandiri saat koneksi ke *server* utama terputus.
  - Data pendaftaran dan triase disimpan di *Local Storage* sementara (*Queueing Local*).
  - Sinkronisasi asinkron: Begitu internet/listrik menyala, sistem melakukan *bulk-sync* ke *server* tanpa intervensi manual.

## 2. Human-Failure Tolerant (Anti-Disiplin & Pragmatisme)
- **Kondisi Nyata:** Perawat *burnout*, dokter malas mengetik form panjang, kebiasaan jalan pintas (*shortcut*).
- **Solusi Arsitektur:**
  - *Graceful Degradation of Input*: Jika dokter hanya menginput 1 diagnosis utama tanpa data pendukung, sistem membiarkannya lolos (tidak me-blokir alur pelayanan pasien). Kelengkapan bisa dikejar belakangan oleh admin/koder.
  - Sistem memiliki mekanisme *Copy-Paste* yang cerdas dan aman untuk SBAR agar perawat bangsal malam tidak kehabisan waktu.

## 3. BPJS-Decoupled Workflow (Eventually Consistent)
- **Kondisi Nyata:** Server V-Claim BPJS sering *timeout*. Jika sistem mewajibkan *bridging* sukses sebelum pasien dilayani, seluruh rumah sakit akan lumpuh total.
- **Solusi Arsitektur:**
  - Pelayanan medis dan *bridging* BPJS sepenuhnya **Decoupled** (Dilepas).
  - Pasien bisa terus berjalan ke Poli, Lab, hingga Pulang tanpa harus menunggu SEP (Surat Eligibilitas Peserta) terbit.
  - Terdapat *Background Job / Worker* khusus (misal: Redis Queue) yang me-*retry* pembuatan SEP ke BPJS ratusan kali di balik layar hingga berhasil (Eventually Consistent).

## 4. Async Clinical Workflow (Input Belakangan)
- **Kondisi Nyata:** Dokter IGD menangani kecelakaan massal, tidak mungkin *login* dan mengetik *SOAP* di tengah kekacauan. Perintah diberikan secara lisan (*Verbal Order*).
- **Solusi Arsitektur:**
  - Perawat/Dokter dapat menginput tindakan dan meresepkan obat secara retrospektif (input belakangan) dengan penanda waktu (*timestamp*) mundur.
  - Apotek dapat melayani "Resep Lisan Darurat" yang transaksinya di-*pending* di sistem sampai dokter memvalidasinya secara digital 24 jam kemudian.

## 5. Progressive Complexity (Jangan One-Size-Fits-All)
- **Kondisi Nyata:** Puskesmas gunung dengan 1 komputer dan tenaga rangkap tidak butuh arsitektur *Event-Driven* kamar operasi.
- **Solusi Arsitektur:**
  - Pendekatan Modular / *Feature Flags*.
  - **Mode Lite:** Hanya mengaktifkan Loket, Poli Dasar, dan Kasir Tunai. Layar dibuat sangat sederhana dan ringan.
  - **Mode Enterprise:** Untuk RS Tipe B dengan *Dashboard*, *Bed Management*, CSSD, dan pembagian porsi *Fee-for-Service* yang rumit.

## 6. Hybrid Native (Kertas Belum Mati)
- **Kondisi Nyata:** Akreditasi, ketakutan litigasi medis, dan kenyamanan dokter senior memaksa penggunaan *Double Input* (kertas lalu sistem). Triple workload terjadi (Kertas -> SIMRS -> Excel).
- **Solusi Arsitektur:**
  - Sistem tidak memaksa diri membunuh kertas secara radikal. 
  - ERP memfasilitasi pencetakan form kosong yang sudah terisi identitas pasien (*Barcode*). Kertas tersebut diisi manual, lalu di-*scan* kembali ke dalam SIMRS (Sistem *Document Management* / *Attachment*).

## 7. Governance-First (Faktor Politik & Friksi Organisasi)
- **Kondisi Nyata:** Konflik antara unit (Dokter vs Farmasi soal Formularium, Kasir vs Perawat soal pasien pulang).
- **Solusi Arsitektur:**
  - *Hard-Stop* administratif (misalnya menahan pasien pulang jika belum lunas) bisa di-*Bypass* oleh level Direksi/Manajemen menggunakan *Otorisasi Khusus* (Emergency Override) agar operasional klinis tidak tersandera masalah uang.
  - Modul *Log Audit* yang sangat presisi untuk melacak siapa yang melakukan *Bypass* guna meredam saling tuduh antar unit.

---
*Dokumen ini adalah manifesto bahwa ERP Faskes Indonesia yang sukses bukanlah sistem yang paling futuristik, melainkan sistem yang paling **Bertahan Hidup (Survivable)** di tengah badai operasional dan keterbatasan.*

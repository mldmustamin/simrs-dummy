# Rencana Implementasi & Workflow Modul Spesialisasi Poliklinik
**Referensi Target**: RSUD Bahteramas, Kendari, Sulawesi Tenggara

## 1. Latar Belakang & Ruang Lingkup
Modul ini dirancang agar setiap poliklinik di RSUD Bahteramas memiliki antarmuka Rekam Medis Elektronik (RME) yang dinamis dan terpersonalisasi sesuai dengan kebutuhan spesialisasi mereka, mulai dari Poli Dasar hingga Sub-Spesialis.

## 2. Pemetaan Modul per Spesialisasi

### Fase 1: Poli Dasar & Umum
- **Poliklinik Gigi dan Mulut / Bedah Mulut**
  - **Kebutuhan**: *Odontogram* Interaktif (pemetaan 32 anatomi gigi).
  - **Asesmen Khusus**: Karies, Karang gigi, *Missing teeth*, Kalkulus.
- **Poliklinik Umum & MCU (Medical Check Up)**
  - **Kebutuhan**: Form *Screening* Kesehatan Kerja & Standar SOAP.

### Fase 2: Poli Spesialis Mayor
- **Poli Kebidanan & Kandungan (Obgyn)**
  - **Kebutuhan**: Riwayat Kehamilan/Persalinan (GPA).
  - **Asesmen Khusus**: HPHT, HPL, Data Janin/USG (DJJ).
- **Poli Anak**
  - **Kebutuhan**: Riwayat Imunisasi Dasar & Lanjutan.
  - **Asesmen Khusus**: Tumbuh Kembang (Kurva WHO BB/TB), Lingkar Kepala.
- **Poli Penyakit Dalam & Bedah Umum**
  - **Kebutuhan**: Diagram Anatomi Tubuh (untuk menandai lokasi nyeri atau luka bedah).

### Fase 3: Poli Spesialis Khusus
- **Poli Mata**: *Visual Acuity* (Visus VOD/VOS), Buta Warna (Ishihara), Tonometri.
- **Poli THT**: Audiometri dasar, Otoskopi.
- **Poli Lainnya (Saraf, Jantung, Kulit & Kelamin, Jiwa, Paru, Gizi, Urologi, Orthopedi)**: SOAP standar diperkaya dengan parameter vital masing-masing poli (contoh: input hasil EKG untuk Jantung).

---

## 3. Rencana Workflow (Alur Kerja Pengguna)

Sistem akan beroperasi dengan *Unified Workflow* (Alur Terpusat) di mana aplikasi menyesuaikan wujudnya berdasarkan akses pengguna dan tipe pasien.

### A. Alur Pendaftaran (Admisi / Kiosk)
1. Pasien datang dan mendaftar melalui **Kios Mandiri** atau **Loket Admisi**.
2. Pasien memilih **Poliklinik Tujuan** (misal: Poli Gigi) dan **Dokter Spesialis**.
3. Sistem secara otomatis menempatkan pasien ke dalam tabel `reg_periksa` (antrean poli) dengan status `stts: 'Belum'`.

### B. Alur Dashboard Poliklinik (Dokter / Perawat)
1. Perawat/Dokter login ke SIMRS dan membuka menu **Modul Poli (`PoliDashboard.tsx`)**.
2. Sistem mendeteksi ID Poli petugas dan memuat **Daftar Antrean Pasien** khusus untuk poli tersebut di hari ini secara *real-time*.
3. Perawat/Dokter mengklik tombol **"Periksa"** pada nama pasien.
4. **[CRITICAL STEP]** Aplikasi memuat halaman RME (`MedicalRecord.tsx`). Di balik layar, React akan mengecek `kd_poli` pasien:
   - Jika `kd_poli` = Poli Gigi, maka yang dirender ke layar adalah komponen `<AsesmenGigi />` (Odontogram).
   - Jika `kd_poli` = Poli Obgyn, maka yang dirender adalah `<AsesmenObgyn />`.
   - Jika poli biasa, maka yang dirender adalah `<SoapUmum />`.

### C. Alur Pelayanan RME & Penunjang
1. Dokter menginput data pengkajian spesifik (misal: mengeklik gigi berlubang di Odontogram).
2. Dokter menginput Diagnosa (ICD-10) di tab Diagnosa.
3. **Integrasi Penunjang & Apotek**:
   - Jika dokter membutuhkan tes Lab (misal: Cek Gula Darah), dokter memilih pesanan dari tab *Laboratorium*. Sistem akan otomatis mengirim data pesanan *bypass* ke Unit Laboratorium.
   - Dokter mengetik resep obat di tab *E-Resep*. Resep langsung terkirim secara elektronik ke *Modul Farmasi/Apotek*.
4. Dokter menekan **"Simpan & Selesai"**. Status antrean pasien berubah dari `Belum` menjadi `Sudah` (Selesai).

### D. Alur Penyelesaian (Kasir & Farmasi)
1. Pasien pergi ke **Kasir**. Semua tindakan medis yang diinput dokter (misal: Cabut Gigi), obat dari resep, dan pesanan Lab langsung terakumulasi dalam satu *billing* yang diproteksi *Optimistic Concurrency* (anti-nota ganda).
2. Pasien mengambil obat di **Apotek**. Tombol penyerahan obat akan otomatis aktif jika status pembayaran di Kasir sudah "Lunas".

---

## 4. Perubahan Arsitektur Teknis

1. **Database Backend (Prisma)**
   - Perlu dibuat tabel ekstensi yang berelasi dengan nomor rawat pasien, seperti: `asesmen_gigi`, `asesmen_obgyn`, `asesmen_mata`, dan `asesmen_anak`.
   
2. **REST API (NestJS)**
   - Pembuatan endpoint spesifik poli (contoh: `POST /api/poli/gigi/odontogram`) di bawah modul baru `poli-spesialis.module.ts`.
   - Modifikasi endpoint *Queue* (`GET /api/queues/poli`) agar menyertakan data *metadata poli* sehingga Frontend tahu form apa yang harus dimuat.

3. **Frontend (React)**
   - Pembuatan `PoliDashboard.tsx` sebagai pusat pemantauan antrean.
   - Refaktor `MedicalRecord.tsx` menjadi *Dynamic Module Renderer* yang akan memuat *sub-komponen* spesialis (Gigi, Mata, Obgyn, Anak) secara kondisional (*lazy loading* jika perlu).

---
*Dokumen ini merupakan blue-print awal pembangunan modul spesialisasi poliklinik berbasis standar RSUD Bahteramas.*

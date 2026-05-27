# Pemetaan Layanan Mandiri per Unit Pelayanan (SIMRS Web)

Di dalam ekosistem rumah sakit, setiap unit pelayanan memiliki otonomi untuk melakukan tindakan medis atau layanan penunjang secara mandiri, baik berdasarkan rujukan internal (dari poliklinik/ranap) maupun Atas Permintaan Sendiri (APS) / Rujukan Eksternal. 

Dokumen ini memetakan layanan-layanan apa saja yang *bisa berdiri sendiri* di tiap unit pada SIMRS Web kita.

---

## 1. Instalasi Gawat Darurat (IGD)
IGD adalah garda terdepan dengan otonomi penuh untuk melakukan tindakan sebelum pasien didaftarkan ke rawat inap atau dipulangkan.
*   **Layanan Mandiri / Tindakan:**
    *   Triase dan Resusitasi Jantung Paru (RJP).
    *   Bedah Minor (Jahit luka, insisi abses, cabut kuku / *ekstraksi kuku*).
    *   Pemasangan alat invasif sementara (Infus, Kateter urin, NGT).
    *   Pemeriksaan dasar (EKG, Nebulizer).
    *   Konservasi / Observasi di ruang IGD (< 6 Jam).
*   **Implikasi SIMRS:** IGD harus bisa menagih tindakan (billing) secara langsung tanpa harus menunggu pasien masuk rawat inap.

## 2. Poliklinik (Rawat Jalan)
Tiap poliklinik spesialis memiliki tarif jasa dan tindakan mandiri yang spesifik sesuai spesialisasinya.
*   **Layanan Mandiri / Tindakan:**
    *   **Poli Gigi:** Cabut gigi, tambal, *scaling*, *root canal treatment*.
    *   **Poli Kandungan (Obgyn):** USG kehamilan (sering diletakkan di poli, bukan radiologi), pasang/lepas IUD & implan, pap smear.
    *   **Poli Mata:** Visus, tonometri (cek tekanan bola mata), *slit lamp*, ekstraksi corpus alienum (benda asing).
    *   **Poli THT:** Ekstraksi serumen, laringoskopi, irigasi telinga.
    *   **Poli Bedah:** Rawat luka (wound care), angkat jahitan.
*   **Implikasi SIMRS:** Tabel `jns_perawatan` (Tindakan) harus dipetakan ke masing-masing poli (`kd_poli`) agar perawat poli hanya melihat tindakan yang relevan saat input.

## 3. Instalasi Laboratorium (Patologi Klinik)
Laboratorium melayani rujukan dari internal RS maupun rujukan dari luar (klinik lain / dokter praktik swasta / pasien umum APS).
*   **Layanan Mandiri / Tindakan:**
    *   Pengambilan spesimen (Phlebotomy).
    *   Hematologi Rutin/Lengkap.
    *   Kimia Klinik (Gula darah, Kolesterol, Fungsi Hati, Fungsi Ginjal).
    *   Urinalisa & Faeces rutin.
    *   Serologi / Imunologi (Widal, Dengue, HBsAg, HIV, dll).
*   **Implikasi SIMRS:** SIMRS harus memiliki fitur Pendaftaran Pasien Langsung ke Lab (tanpa lewat poli) untuk pasien Atas Permintaan Sendiri (APS).

## 4. Instalasi Radiologi / Rontgen
Sama seperti laboratorium, radiologi bisa menerima pasien rujukan luar atau APS.
*   **Layanan Mandiri / Tindakan:**
    *   X-Ray / Rontgen Konvensional (Thorax, Ekstremitas, Tulang Belakang).
    *   Ultrasonografi (USG) Abdomen, Mammae, Tiroid.
    *   CT-Scan (dengan atau tanpa kontras).
    *   MRI (Magnetic Resonance Imaging).
*   **Implikasi SIMRS:** Radiologi butuh integrasi ke sistem PACS (Picture Archiving and Communication System) atau minimal kolom unggah hasil bacaan (ekspertise) ke dalam SIMRS.

## 5. Instalasi Farmasi (Apotek)
Selain melayani resep dari poli dan ranap, apotek RS biasanya juga melayani penjualan bebas (OTC).
*   **Layanan Mandiri / Tindakan:**
    *   Tebus resep dari dokter luar / rujukan.
    *   Penjualan obat bebas (Over The Counter - OTC).
    *   Pemberian Konsultasi Informasi Obat (KIE) oleh Apoteker.
*   **Implikasi SIMRS:** Harus ada menu "Resep Bebas" (tanpa `no_rawat` poli) di Modul Farmasi untuk mengakomodir penjualan obat langsung ke masyarakat.

## 6. Instalasi Rehabilitasi Medik (Fisioterapi)
*   **Layanan Mandiri / Tindakan:**
    *   Terapi Fisik (Fisioterapi), Diatermi, Infrared, Terapi Wicara.
*   **Implikasi SIMRS:** Membutuhkan pencatatan jadwal seri (karena pasien fisioterapi biasanya harus datang 6-10 kali kunjungan dengan 1 kali pendaftaran / rujukan).

## 7. Instalasi Kamar Operasi (OK/IBS)
*(Terkunci oleh mekanisme Rawat Inap/IGD/Poliklinik, namun ada pengecualian)*
*   **Layanan Mandiri (One Day Care / ODC):**
    *   Bedah kecil terencana (Lipoma, Kista Ateroma, Sirkumsisi/Sunat, Ekstraksi Katarak tanpa komplikasi).
*   **Implikasi SIMRS:** Modul OK harus bisa membilling tindakan ODC yang pasiennya bisa langsung pulang di hari yang sama tanpa harus menempati *bed* rawat inap reguler.

---

## Rencana Integrasi ke SIMRS Web Saat Ini
Dari pemetaan di atas, progres yang akan kita kejar:
1.  **Poli/Ralan:** Pastikan `rawat_jl_dr` bisa menyimpan banyak tindakan spesifik poli dalam 1 nomor rawat.
2.  **Lab/Radiologi:** Siapkan *form* pendaftaran *bypass* (APS) di mana pasien bisa langsung didaftarkan dengan tujuan Poli = Lab / Poli = Radiologi.
3.  **Farmasi:** Mengaktifkan form penjualan bebas jika diizinkan oleh kebijakan RS (menjual item dari `databarang` tanpa relasi ke `reg_periksa`).

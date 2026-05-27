import os

doc_dir = "/home/gudang-data-kantor/simrs-web/workflow"
os.makedirs(doc_dir, exist_ok=True)

docs = {
    "01_pendaftaran.md": """# Modul Pendaftaran & Kios (APM / APS)

Modul ini memfasilitasi registrasi rawat jalan secara mandiri maupun melalui loket admisi.

## Parameter Teknis & Endpoint (Frontend `Registration.tsx` & `KiosMandiri.tsx`)
- **Pencarian Pasien**: `GET /api/patients/search?q={keyword}&page={pageNum}&limit=10`
- **Pengecekan RM Kios**: `GET /api/kiosk/check-patient?q={searchInput}`
- **Pengambilan Jadwal Aktif**: `GET /api/kiosk/active-schedules`
- **Pendaftaran Poliklinik (APM)**: `POST /api/kiosk/register`
- **Pendaftaran Reguler/Admisi**: `POST /api/registrations`
- **Bypass Penunjang (APS)**: `POST /api/registrations/aps`

## Mekanisme Sistem (Strict Workflow)
1. Pasien input NIK/RM di layar kios. Sistem merender profil (dari `check-patient`).
2. Pasien memilih Poli & Dokter. 
3. *Submit* memicu `register` yang dibungkus `Prisma.$transaction` dengan batasan *Retry-Loop (Max 5x)* untuk mitigasi duplikasi `no_rawat` pada tabel `reg_periksa`.
4. Jika pasien didaftarkan ke Lab/Rad via APS (`/api/registrations/aps`), sistem akan secara otomatis melacak tarif tindakan dari tabel `jns_perawatan_lab` / `radiologi` dan menyuntikkannya sebagai tagihan dasar.
""",
    "02_antrean.md": """# Modul Antrean (Queue Display)

Sistem pemantauan status antrean pasien di poliklinik (`QueueDisplay.tsx`).

## Parameter Teknis & Endpoint
- **Pengambilan Data Antrean**: `GET /api/queues/today`
- **Variabel Utama**: Query ini memfilter tabel `reg_periksa` berdasarkan `tgl_registrasi` hari ini (`startOfDay`) dan `stts: 'Belum'`.
- **Relasi Prisma**: Melakukan *JOIN* ke tabel `pasien` (`nm_pasien`) dan `poliklinik` (`nm_poli`).

## Mekanisme Sistem
Data antrean akan di- *fetch* secara berkala (atau via WebSocket jika di- *upgrade*) untuk menampilkan nomor urut `no_reg` berjalan di layar ruang tunggu poliklinik.
""",
    "03_bed_management.md": """# Modul Bed Management

Pemantauan dan alokasi ranjang kamar inap (`BedManagement.tsx`).

## Parameter Teknis & Endpoint
- **Ketersediaan Kamar**: `GET /api/ranap/kamar`
- **Pendaftaran Ranap (Admisi Inap)**: `POST /api/ranap/admisi`

## Mekanisme Sistem
Memetakan seluruh baris di tabel `kamar` (serta relasi `bangsal`). Saat `POST /ranap/admisi` dieksekusi, status kamar akan di- *update* (misalnya dari 'KOSONG' menjadi 'ISI') seiring dengan terbitnya nomor rawat inap baru.
""",
    "04_rme_rawat_jalan.md": """# Modul RME Rawat Jalan

Catatan klinis poli (`MedicalRecord.tsx`).

## Parameter Teknis & Endpoint
- **Master Lab**: `GET /lab/master?kategori=PK`
- **Riwayat CPPT**: `GET /api/rme/cppt/{rmSearch}`
- **Riwayat Diagnosa**: `GET /api/rme/diagnoses/{rmSearch}`
- **Pencarian ICD-10**: `GET /api/rme/icd10?q={icdKeyword}`
- **Simpan Diagnosa**: `POST /api/rme/diagnosis`
- **Simpan SOAP**: `POST /api/rme/soap`
- **Order Resep**: `POST /farmasi/resep`
- **Order Lab**: `POST /lab/request`

## Mekanisme Sistem
State form yang dikelola meliputi `keluhan`, `pemeriksaan`, `penilaian`, `rtl`, serta tanda vital (`tensi`, `nadi`, `suhu_tubuh`, `respirasi`, `kesadaran`). Seluruh inputan dokter akan dimutasi ke dalam format JSON/teks dan disimpan ke tabel historikal perawatan ralan (`pemeriksaan_ralan`) diiringi dengan ICD-10 ke tabel `diagnosa_pasien`.
""",
    "05_cppt_rawat_inap.md": """# Modul CPPT Rawat Inap

Observasi harian pasien ranap (`RanapCPPT.tsx`).

## Parameter Teknis & Endpoint
- **Riwayat CPPT Ranap**: `GET /api/rme/cppt/{rmSearch}`
- **Simpan CPPT Ranap**: `POST /ranap/cppt`

## Mekanisme Sistem
Berbeda dengan RME Jalan, input CPPT ranap merekam intervensi harian dari perawat jaga dan dokter DPJP (*Dynamic Table Insertion*) dengan mencatat waktu spesifik pergantian shift, yang tersimpan pada tabel `pemeriksaan_ranap`.
""",
    "06_farmasi.md": """# Modul Farmasi (Gudang & Peracikan)

Penyusunan E-Resep dan inventory (`Farmasi.tsx`).

## Parameter Teknis & Endpoint
- **Pencarian Obat**: `GET /farmasi/obat?keyword={keyword}`
- **Cek Stok Fisik**: `GET /farmasi/stok?kode_brng={kode_brng}`
- **Metode Racik**: `GET /farmasi/metode-racik`
- **Penyusunan Resep**: `POST /farmasi/resep`

## Mekanisme Sistem
Apoteker/Farmasis menarik data stok secara real-time dari relasi tabel `databarang` dan `gudangbarang`. Obat dapat dikonversi ke dalam resep racikan (puyer/kapsul) dengan metode yang ditentukan, lalu disimpan dalam tabel `resep_obat` dan rinciannya di `resep_dokter`.
""",
    "07_apotek.md": """# Modul Apotek (Pelayanan)

Penyerahan obat dan penjualan OTC (`Apotek.tsx`).

## Parameter Teknis & Endpoint
- **Antrean E-Resep (Tunggu Serah)**: `GET /farmasi/antrean-resep`
- **Daftar Depo Aktif**: `GET /farmasi/depo`
- **Master Obat (OTC)**: `GET /farmasi/obat?keyword={keyword}`
- **Jual Bebas**: `POST /farmasi/resep-bebas`
- **Finalisasi & Serah Obat**: `POST /farmasi/serahkan`

## Mekanisme Sistem
Sistem Farmasi memegang proteksi *Financial Lock*. Pada *endpoint* `/farmasi/serahkan`, backend memeriksa tabel `reg_periksa.status_bayar`. Jika `"Belum_Bayar"` (untuk pasien Umum), tombol serah UI dikunci, API merespon 403 Forbidden. Saat obat bebas dijual, mekanisme *Row-Level Locking* (`SELECT ... FOR UPDATE`) menjaga agar stok `gudangbarang` tidak berkurang melebihi batas. Log mutasi diisi nama Apoteker dari Token JWT.
""",
    "08_laboratorium.md": """# Modul Laboratorium

Antrean dan hasil pemeriksaan lab (`Laboratorium.tsx`).

## Parameter Teknis & Endpoint
- **Antrean Order Lab**: `GET /lab/antrean`
- **Template Hasil Tes**: `GET /lab/template?kd_jenis_prw={kd_jenis_prw}`
- **Input Hasil Final**: `POST /lab/hasil`

## Mekanisme Sistem
Order lab yang masuk (baik dari RME poli maupun APS Admisi) masuk ke antrean. Sistem mengambil template form berisikan Nilai Rujukan (Satuan, Nilai Normal) berdasarkan ID Perawatan. Saat hasil di-submit via `/lab/hasil`, data tersimpan permanen di tabel `detail_periksa_lab`.
""",
    "09_operasi.md": """# Modul Operasi (IBS)

Jadwal pembedahan (`Operasi.tsx`).

## Parameter Teknis & Endpoint
- **Katalog Paket Operasi**: `GET /operasi/paket`
- **Input Laporan Operasi**: `POST /operasi/input`

## Mekanisme Sistem
Petugas memilih jenis paket operasi yang menentukan biaya dasar. Tagihan kemudian diekskalasi ke dalam sistem billing kasir secara otomatis sesuai kode paket di tabel `paket_operasi`.
""",
    "10_kasir.md": """# Modul Kasir & Billing

Penyelesaian tagihan akhir (`Kasir.tsx`).

## Parameter Teknis & Endpoint
- **Kalkulasi Tagihan (Informed Consent)**: `GET /kasir/tagihan/{formattedNoRawat}`
- **Proses Pembayaran (ACID)**: `POST /kasir/bayar`
- **Integrasi Klaim**: `POST /api/casemix/klaim` (Jika berlaku)

## Mekanisme Sistem
Menerima `no_rawat`. API menghitung total biaya dari `reg_periksa` (karcis), `rawat_jl_dr/pr` (tindakan), `periksa_lab/radiologi`, serta total resep `detail_pemberian_obat`. 
Proses pelunasan `POST /kasir/bayar` dilindungi oleh blok `Prisma.$transaction` yang mengunci pembuatan `nota_jalan` dan `jurnal` akuntansi. Jika gagal akibat konfik *Unique Key* (P2002), sistem me- *rollback* dan mencoba lagi (maksimal 5x *retry*), sebelum mencetak struk dan membuka kunci (lock) apotek.
"""
}

for filename, content in docs.items():
    with open(os.path.join(doc_dir, filename), "w") as f:
        f.write(content)

print(f"Strict workflow docs generated in {doc_dir}")

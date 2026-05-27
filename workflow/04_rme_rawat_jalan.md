# Modul RME Rawat Jalan

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

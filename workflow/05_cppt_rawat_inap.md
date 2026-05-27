# Modul CPPT Rawat Inap

Observasi harian pasien ranap (`RanapCPPT.tsx`).

## Parameter Teknis & Endpoint
- **Riwayat CPPT Ranap**: `GET /api/rme/cppt/{rmSearch}`
- **Simpan CPPT Ranap**: `POST /ranap/cppt`

## Mekanisme Sistem
Berbeda dengan RME Jalan, input CPPT ranap merekam intervensi harian dari perawat jaga dan dokter DPJP (*Dynamic Table Insertion*) dengan mencatat waktu spesifik pergantian shift, yang tersimpan pada tabel `pemeriksaan_ranap`.

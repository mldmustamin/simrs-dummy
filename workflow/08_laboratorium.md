# Modul Laboratorium

Antrean dan hasil pemeriksaan lab (`Laboratorium.tsx`).

## Parameter Teknis & Endpoint
- **Antrean Order Lab**: `GET /lab/antrean`
- **Template Hasil Tes**: `GET /lab/template?kd_jenis_prw={kd_jenis_prw}`
- **Input Hasil Final**: `POST /lab/hasil`

## Mekanisme Sistem
Order lab yang masuk (baik dari RME poli maupun APS Admisi) masuk ke antrean. Sistem mengambil template form berisikan Nilai Rujukan (Satuan, Nilai Normal) berdasarkan ID Perawatan. Saat hasil di-submit via `/lab/hasil`, data tersimpan permanen di tabel `detail_periksa_lab`.

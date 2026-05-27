# Modul Bed Management

Pemantauan dan alokasi ranjang kamar inap (`BedManagement.tsx`).

## Parameter Teknis & Endpoint
- **Ketersediaan Kamar**: `GET /api/ranap/kamar`
- **Pendaftaran Ranap (Admisi Inap)**: `POST /api/ranap/admisi`

## Mekanisme Sistem
Memetakan seluruh baris di tabel `kamar` (serta relasi `bangsal`). Saat `POST /ranap/admisi` dieksekusi, status kamar akan di- *update* (misalnya dari 'KOSONG' menjadi 'ISI') seiring dengan terbitnya nomor rawat inap baru.

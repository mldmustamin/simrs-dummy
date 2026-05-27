# Modul Antrean (Queue Display)

Sistem pemantauan status antrean pasien di poliklinik (`QueueDisplay.tsx`).

## Parameter Teknis & Endpoint
- **Pengambilan Data Antrean**: `GET /api/queues/today`
- **Variabel Utama**: Query ini memfilter tabel `reg_periksa` berdasarkan `tgl_registrasi` hari ini (`startOfDay`) dan `stts: 'Belum'`.
- **Relasi Prisma**: Melakukan *JOIN* ke tabel `pasien` (`nm_pasien`) dan `poliklinik` (`nm_poli`).

## Mekanisme Sistem
Data antrean akan di- *fetch* secara berkala (atau via WebSocket jika di- *upgrade*) untuk menampilkan nomor urut `no_reg` berjalan di layar ruang tunggu poliklinik.

# Modul Pendaftaran & Kios (APM / APS)

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

# Panduan Arsitektur Backend (NestJS)
*Visi Utama: Backend berspesifikasi Smart Hospital (Event-Driven) yang dapat menyesuaikan diri (Feature Flags) dengan infrastruktur daerah.*

## 1. Event-Driven Architecture (Pub/Sub)
Dalam mode Enterprise Ideal, sistem tidak beroperasi secara linear. Gunakan `@nestjs/event-emitter`.
- **Standar Ideal**: `KasirService.bayar()` menembakkan event `kasir.pembayaran_sukses`. Kemudian `ApotekListener`, `AkuntansiListener`, dan `SmartDashboardListener` merespons event tersebut secara *real-time* dan asinkronus.

## 2. Proteksi Concurrency & Pessimistic Locking
Setiap transaksi finansial dan inventori di tingkat RS Besar sangat tinggi. Perlindungan mutlak diperlukan.
- Gunakan Prisma Raw Query untuk mengeksekusi `SELECT ... FOR UPDATE` jika berhadapan dengan data tunggal yang rentan *race-condition*.
- Selalu gunakan blok `$transaction` Prisma yang membungkus semua operasi terkait menjadi satu kesatuan atomik (ACID).

## 3. Mekanisme Multi-Model (Feature Flags & Graceful Degradation)
API Backend dibangun dengan standar parameter yang lengkap dan ketat. Namun, sediakan fleksibilitas (*Feature Toggles*) untuk faskes tipe rendah.
- Gunakan DTO dengan validasi ketat untuk RS Enterprise, namun sediakan mode `LITE_MODE` di konfigurasi global yang dapat mereduksi tingkat kewajiban (Required Fields) menjadi `IsOptional()` untuk data non-kritis, guna menyelamatkan operasional di situasi darurat atau faskes dengan SDM minim.

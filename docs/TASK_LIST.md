# Task List: Refaktor Prioritas (Debt Eradication)

- [x] **Tahap 1: Auth/JWT & RBAC**
  - [x] Stabilkan Auth/JWT (Pastikan identitas tervalidasi dengan benar).
  - [x] Buat `JwtAuthGuard` dan `RoleGuard/PermissionGuard`.
  - [x] Buat `CurrentUser` decorator untuk mengambil `actor_id` and `actor_name`.
  - [x] Pasang autentikasi global `JwtAuthGuard` dengan route publik eksplisit.
  - [ ] Lengkapi `PermissionGuard` per fungsi pada Lab, Ranap, Operasi, RME, Bed, Queue, Casemix, dan monitoring setelah mapping hak legacy dikonfirmasi.

- [x] **Tahap 2: Audit Trail**
  - [x] Tambahkan model `simrs_web_audit_trail` ke `schema.prisma`.
  - [x] Jalankan `npx prisma db push` untuk *development*.
  - [x] Buat `AuditService` yang mendukung eksekusi di dalam blok `$transaction` Prisma agar tidak *silent failure* pada transaksi kritis.

- [x] **Tahap 3: Kasir Optimistic Concurrency**
  - [x] Refaktor *endpoint* bayar Kasir untuk mengulang *seluruh transaksi* jika terkena P2002.
  - [x] Terapkan batas retry maksimal 5 kali & *rollback* total dengan *error explicit* ke UI.
  - [x] Masukkan penulisan *Audit Trail* ke dalam blok transaksi Kasir.
  - [x] Buat *script* `test_kasir_race.py` untuk mensimulasikan >10 request paralel.

- [x] **Tahap 4: Apotek Multi-Depo**
  - [x] Buat *endpoint* `GET /api/farmasi/depo`.
  - [x] Refaktor `POST /farmasi/serahkan` wajib menerima `kd_bangsal_asal`.
  - [x] Validasi kecukupan stok dengan `SELECT ... FOR UPDATE` dan row locking di dalam transaksi.
  - [x] Masukkan penulisan *Audit Trail* ke dalam blok transaksi Farmasi.
  - [x] Update Frontend Apotek: tambahkan *dropdown* depo dan *disable* tombol serah jika belum dipilih.

- [x] **Tahap 5: APS Lab/Radiologi**
  - [x] Buat *endpoint* `POST /api/registrations/aps`.
  - [x] Validasi *payload* APS dan *generate* `no_rawat` / masukkan ke `reg_periksa`.
  - [x] Buat otomatisasi *billing* awal / order penunjang.
  - [x] Masukkan penulisan *Audit Trail*.

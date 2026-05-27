# Best Practice Fix Plan - SIMRS Dummy

**Tanggal penyusunan:** 27 Mei 2026  
**Status dokumen:** Baseline remediation terverifikasi, belum merupakan bukti
kelulusan production  
**Lingkup:** Backend NestJS/Prisma, frontend React/Vite, keamanan API,
integritas transaksi, quality gate, dan sinkronisasi dokumentasi

## 1. Tujuan Dokumen

Dokumen ini menetapkan rencana perbaikan teknis SIMRS Dummy berdasarkan:

1. Pemeriksaan source code yang tersedia pada repository lokal.
2. Validasi build, lint, test, dan kompilasi skrip yang dijalankan pada
   27 Mei 2026.
3. Referensi resmi NestJS, Prisma, OWASP API Security, React, dan
   typescript-eslint.
4. Keputusan arsitektur proyek yang sudah berlaku, terutama kompatibilitas
   terhadap database SIMRS Dummy legacy.

Dokumen ini menggantikan rencana generik sebagai acuan eksekusi perbaikan.
Dokumen status lama tetap perlu diselaraskan setelah perubahan source
diterapkan dan diverifikasi.

## 2. Kesimpulan Eksekutif

SIMRS Dummy sudah memiliki alur fungsional penting: autentikasi, pendaftaran,
antrean, RME, rawat inap, farmasi, kasir, laboratorium, operasi, klaim
simulasi, dan audit trail. Source sudah lebih maju daripada sebagian dokumen:
Farmasi telah memotong stok dalam transaction, Kasir telah memiliki retry
collision dan audit, serta beberapa controller telah dilindungi JWT/permission.

Sistem tetap belum layak production karena:

| Prioritas | Kondisi Aktual | Dampak |
| --- | --- | --- |
| Kritis | Endpoint `lab`, `ranap`, dan `operasi` belum guarded | Perubahan data klinis dapat dipanggil tanpa autentikasi |
| Kritis | Authorization belum `deny-by-default` dan belum object-level | Endpoint baru atau akses record pasien dapat lolos kontrol |
| Tinggi | Kasir membaca status bayar di luar transaction dan belum menangani seluruh konflik transaction | Double-submit dan konflik paralel belum dibuktikan aman |
| Tinggi | Dashboard/Monitoring memanggil endpoint backend yang tidak ada | Fitur gagal saat runtime |
| Tinggi | Validation, CORS restriction, dan throttling belum terlihat pada bootstrap | Input dan endpoint publik belum cukup diperkeras |
| Tinggi | Backend test suite gagal pada dependency setup | Perubahan kritis tidak memiliki regression gate |
| Sedang | Frontend lint gagal besar | Type safety dan React behavior debt aktif |
| Sedang | Dokumen dan tautan README tidak konsisten dengan source/tree | Handover dan keputusan teknis berisiko keliru |

## 3. Batasan Arsitektur Yang Wajib Dipertahankan

Rencana ini mengikuti keputusan di `docs/DECISION_LOG.md`.

| Batasan | Konsekuensi Perbaikan |
| --- | --- |
| Database `sik` juga digunakan aplikasi legacy | Perubahan web wajib menjaga kompatibilitas data legacy |
| Tidak mengubah struktur tabel inti sembarangan | Jangan melakukan `ALTER TABLE` tabel bawaan untuk memudahkan fix |
| Metadata tambahan memakai tabel ekstensi bila disetujui | Audit/idempotency/metadata baru harus dipisahkan dari tabel legacy |
| BPJS riil belum menjadi scope fase sekarang | Gunakan pembacaan SEP existing atau mock yang terkendali |
| Sistem masih prototipe | Tidak ada klaim production-ready sebelum seluruh gate lulus |

## 4. Baseline Source Dan Validasi

### 4.1 Implementasi Yang Sudah Terlihat

| Area | Bukti Source | Status |
| --- | --- | --- |
| Modul backend utama | `simrs-backend/src/app.module.ts` mendaftarkan Auth, Prisma, Patient, Registration, Queue, Bed, RME, Farmasi, Kasir, BPJS, Casemix, Lab, Ranap, Operasi, dan Audit | Ada |
| Permission guard | `simrs-backend/src/auth/permission.guard.ts` membaca permission user | Ada, cakupan belum penuh |
| Mutasi stok farmasi | `simrs-backend/src/farmasi/farmasi.service.ts` memakai `FOR UPDATE`, update `gudangbarang`, serta insert `riwayat_barang_medis` | Ada, perlu uji |
| Audit transaksi farmasi | `FarmasiService.serahkanObat()` mencatat audit dalam transaction | Ada |
| Transaction kasir | `simrs-backend/src/kasir/kasir.service.ts` menulis nota, status bayar, jurnal, dan audit dalam transaction | Ada, perlu penguatan |
| Retry collision kasir | `KasirService.bayar()` menangkap `P2002`, maksimum lima retry | Ada, belum lengkap |

### 4.2 Gap Source Terkonfirmasi

| Gap | Lokasi | Temuan |
| --- | --- | --- |
| Controller klinis tanpa guard | `src/lab/lab.controller.ts`, `src/ranap/ranap.controller.ts`, `src/operasi/operasi.controller.ts` | Endpoint `POST` masih tidak memiliki `JwtAuthGuard`/`PermissionGuard` |
| Public registration belum diberi kontrol abuse terukur | `src/registration/kiosk.controller.ts` | Endpoint kiosk terbuka dan belum terlihat rate limiting |
| Auth belum global | `src/main.ts`, `src/auth/auth.module.ts` | Tidak ditemukan `APP_GUARD` atau pola `@Public()` |
| Input validation global belum terlihat | `src/main.ts` | Tidak ditemukan pemasangan `ValidationPipe` |
| CORS terbuka generik | `src/main.ts` | `app.enableCors()` tidak menetapkan allowed origin |
| Dashboard API tidak tersedia | `simrs-frontend/src/pages/Dashboard.tsx` | Frontend memanggil `/api/stats`, tanpa controller backend terdeteksi |
| Monitoring API tidak tersedia | `simrs-frontend/src/pages/DataMonitoring.tsx` | Frontend memanggil `/api/monitoring/*`, tanpa controller backend terdeteksi |

### 4.3 Hasil Validasi Pada 27 Mei 2026

| Pemeriksaan | Hasil | Keterangan |
| --- | --- | --- |
| `cd simrs-backend && npm run build` | Lulus | Backend dapat dikompilasi |
| `cd simrs-frontend && npm run build` | Lulus | Frontend dapat menghasilkan bundle |
| `python3 -m compileall -q simulation` | Lulus | Skrip Python dapat dikompilasi |
| `cd simrs-frontend && npm run lint` | Gagal | 88 problems, didominasi `any` dan React hooks |
| `cd simrs-backend && npm test -- --runInBand` | Gagal | 19 suite gagal dan 2 lulus; mayoritas dependency/mock test belum lengkap |

## 5. Evaluasi Rencana Lama Terhadap Best Practice

| Area Rencana Lama | Evaluasi | Keputusan Baru |
| --- | --- | --- |
| Menambahkan guard per controller | Membantu menutup gap langsung, tetapi endpoint baru dapat terlupa | Terapkan auth global, route publik harus eksplisit |
| Permission berbasis fungsi | Diperlukan, tetapi tidak mencegah akses ke record pasien yang salah | Tambahkan object-level authorization |
| Retry `P2002` untuk kasir | Valid untuk unique collision, tetapi bukan seluruh kasus transaction conflict | Tangani idempotency/double-submit dan `P2034` bila memakai serializable |
| Endpoint monitoring generik berdasarkan `type` | Praktis, tetapi memperluas risiko data exposure | Gunakan endpoint resource/use-case eksplisit |
| Lint dibenahi setelah fitur | Benar untuk prioritas, tetapi hooks error tidak boleh dibiarkan lama | Perbaiki hooks setelah security/runtime blocker |
| Dokumentasi diperbarui terakhir | Benar, bila dokumen baseline baru mencatat gap saat ini | Dokumen ini menjadi baseline; status lama diperbarui sesudah fix |

## 6. Target Arsitektur Keamanan

### 6.1 Authentication: Protected By Default

Karena hampir semua endpoint mengakses data pasien, layanan, stok, atau
keuangan, authentication harus berlaku global.

**Desain target:**

1. Daftarkan `JwtAuthGuard` sebagai global `APP_GUARD`.
2. Buat decorator `@Public()` untuk route yang benar-benar publik.
3. Route publik minimum:
   - `POST /api/auth/login`
   - route kiosk yang disetujui secara operasional
   - health check yang tidak mengekspos data
4. Endpoint yang tidak diberi `@Public()` wajib menolak request anonymous.

**Alasan:** Dokumentasi NestJS merekomendasikan global authentication guard
ketika mayoritas endpoint harus dilindungi. OWASP API5:2023 juga menyarankan
mekanisme authorization yang menolak akses secara default dan memberi grant
secara eksplisit.

### 6.2 Function-Level Authorization

Authentication hanya membuktikan identitas. Setiap fungsi sensitif harus
memiliki permission yang dapat dipetakan ke kebijakan operasional RS.

| Area | Operasi Minimum Yang Memerlukan Permission |
| --- | --- |
| Registrasi | Buat atau ubah registrasi |
| RME/CPPT | Membaca atau menulis catatan klinis |
| Lab | Order pemeriksaan dan input/validasi hasil |
| Ranap | Admisi dan input CPPT rawat inap |
| Operasi | Membuat tindakan operasi |
| Farmasi | Membuat resep, memvalidasi, menyerahkan obat, resep bebas |
| Kasir | Membaca tagihan detail, bayar, jurnal |
| Monitoring | Statistik dan daftar data sensitif |

### 6.3 Object-Level Authorization

Permission fungsi tidak cukup bila request menyertakan ID dari client.
Setiap service yang mengolah `no_rawat`, `no_resep`, nomor rekam medis, SEP,
atau ID laporan harus memeriksa bahwa actor boleh mengakses record tersebut.

| Objek | Pemeriksaan Target |
| --- | --- |
| `no_rawat` | Encounter ada dan dapat diakses unit/peran actor |
| `no_resep` | Resep terkait layanan yang dapat diproses depo/actor |
| RME/CPPT | Akses klinis sesuai assignment/peran yang disetujui |
| Lab/Operasi | Actor memiliki fungsi dan scope unit |
| Tagihan/nota | Actor berhak menangani transaksi tersebut |
| Monitoring | Data yang dikembalikan dibatasi scope dan field |

**Alasan:** OWASP API1:2023 mensyaratkan pemeriksaan akses record pada setiap
fungsi yang menggunakan ID dari client untuk membaca atau memodifikasi data.

### 6.4 Input, Transport, Dan Abuse Control

| Kontrol | Implementasi Target |
| --- | --- |
| DTO validation | Gunakan DTO dan `ValidationPipe` global dengan whitelist; tolak field tak dikenal pada payload write |
| CORS | Batasi origin berdasarkan konfigurasi deployment frontend |
| Error response | Gunakan HTTP exception terkontrol; jangan memaparkan error database/stack |
| Login throttling | Batasi percobaan autentikasi berulang |
| Kiosk throttling | Batasi pencarian/pendaftaran publik agar tidak menjadi abuse flow |
| Audit security | Catat operasi penting dan denial sensitif sesuai kebijakan privacy |

## 7. Target Integritas Transaksi

### 7.1 Kasir Dan Jurnal

**Masalah saat ini:** `getTagihan()` dan pemeriksaan `status_bayar` dilakukan
sebelum transaction pembayaran. Transaction kemudian membuat nota dan jurnal,
sedangkan retry hanya membedakan `P2002`.

**Desain target:**

1. Baca kembali state pembayaran yang menentukan keputusan di dalam
   transaction.
2. Pastikan transaksi kedua untuk `no_rawat` yang sama mendapat response
   conflict/idempotent, bukan membuat efek bayar ulang.
3. Pertahankan unique constraint existing sebagai pertahanan database.
4. Evaluasi `Serializable` untuk blok pembayaran; bila digunakan, tangani
   konflik/deadlock Prisma `P2034` dengan retry terbatas.
5. Pertahankan audit trail di transaction yang sama dengan posting transaksi.
6. Pertimbangkan idempotency key pada permintaan bayar apabila dapat disimpan
   tanpa melanggar kebijakan database legacy, misalnya pada tabel ekstensi.

**Acceptance criteria:**

| Skenario | Hasil Yang Wajib |
| --- | --- |
| Dua kasir membayar rawat berbeda bersamaan | Nomor nota/jurnal unik dan jurnal balance |
| Dua request membayar `no_rawat` yang sama | Hanya satu transaksi posting; request lain ditolak/idempotent |
| Conflict/deadlock database | Retry terbatas atau error operasional jelas, tanpa partial commit |
| Error saat audit/jurnal | Seluruh pembayaran rollback |

### 7.2 Farmasi Dan Inventori

**Kondisi saat ini:** mutasi stok telah berada dalam transaction dan
menggunakan row lock. Nilai tuslah/embalase masih berupa konstanta source.

**Desain target:**

1. Verifikasi row lock untuk penyerahan dari depo yang sama pada request
   paralel.
2. Pastikan resep regular dan racikan memiliki aturan pemotongan stok yang
   lengkap.
3. Pertahankan `gudangbarang`, `riwayat_barang_medis`, detail billing, status
   penyerahan, dan audit dalam boundary transaction konsisten.
4. Ganti nilai tarif konstan dengan konfigurasi/master yang disetujui.
5. Tolak proses tanpa `kd_bangsal_asal`.

**Acceptance criteria:**

| Skenario | Hasil Yang Wajib |
| --- | --- |
| Stok cukup | Mutasi, riwayat, billing, status resep, audit konsisten |
| Stok kurang | Tidak ada stok/billing/status yang berubah |
| Dua dispense paralel | Tidak ada stok negatif dan tidak ada penyerahan ganda |
| Depo tidak dipilih | Request ditolak sebelum mutasi |

## 8. Target API Dashboard Dan Monitoring

Frontend sekarang telah menyediakan halaman dashboard dan monitoring, namun
backend route yang dipanggil belum terlihat. API pengganti harus tidak menjadi
browser tabel bebas untuk data medis.

**Endpoint target yang disarankan:**

| Endpoint | Isi | Kontrol |
| --- | --- | --- |
| `GET /api/dashboard/summary` | Metric dashboard minimum | JWT + permission, response field terbatas |
| `GET /api/monitoring/registrations` | Daftar kunjungan paginated | JWT + scope unit + filter terbatas |
| `GET /api/monitoring/queues` | Status antrean | JWT/aturan display yang jelas |
| `GET /api/monitoring/beds` | Status bed terpilih | JWT + field minimization |

**Dilarang sebagai default:** endpoint generik yang menerima nama tabel atau
tipe data bebas lalu mengembalikan record internal.

## 9. Target Testing Dan Quality Gate

### 9.1 Backend Automated Tests

Test sekarang belum menjadi gate karena dependency Nest belum tersediakan
dalam `TestingModule`.

| Kelompok Test | Pekerjaan | Gate |
| --- | --- | --- |
| Unit controller/service | Mock `PrismaService`, `AuditService`, `ConfigService`, dan service controller | Seluruh test lama dapat berjalan |
| Guard tests | Test anonymous, permission denied, permission allowed | `401`/`403`/success terbukti |
| Global auth e2e | Test route default protected dan `@Public()` | Endpoint baru tidak terbuka default |
| Object authorization | Test actor mencoba ID record di luar scope | Access denied |
| Kasir integration | Test double-submit dan concurrent payment | Satu posting valid per pembayaran |
| Farmasi integration | Test row lock, insufficient stock, dan rollback | Tidak ada stok negatif/partial state |

NestJS menyediakan `overrideProvider()` dan `overrideGuard()` untuk
menggantikan dependency/guard pada testing module, sementara integration test
harus tetap menggunakan guard nyata untuk membuktikan kebijakan akses.

### 9.2 Frontend Quality Gate

| Urutan | Scope |
| --- | --- |
| 1 | Perbaiki pelanggaran hook yang dapat mengganggu render/effect behavior |
| 2 | Buat contract/interface response API utama |
| 3 | Ganti `any` dengan type konkret atau `unknown` yang dinarrow |
| 4 | Tambahkan route/menu authorization berbasis capability |
| 5 | Jadikan `npm run lint` dan `npm run build` gate wajib |

React mendefinisikan `useEffect` untuk sinkronisasi dengan external system dan
memerlukan dependencies yang benar. `typescript-eslint` merekomendasikan
`unknown` ketimbang `any` bila bentuk data belum diketahui karena akses value
harus dinarrow lebih dahulu.

## 10. Tahapan Eksekusi

### Tahap 0 - Safety Dan Baseline

| Item | Output | Status Awal |
| --- | --- | --- |
| Pulihkan workflow Git yang terhubung ke `origin/main` tanpa menghapus source lokal | Branch/diff dapat diaudit | Belum dikerjakan |
| Rekam hasil build/lint/test baseline | Acuan sebelum fix | Tercatat pada dokumen ini |

### Tahap 1 - Security Foundation

| Item | Output | Definition Of Done |
| --- | --- | --- |
| Global JWT guard + `@Public()` | Default endpoint protected | E2E default-deny lulus |
| Permission mapping | Hak fungsi klinis/finansial konsisten | Matrix permission lulus |
| Guard untuk Lab/Ranap/Operasi | Endpoint write kritis tertutup | Anonymous/forbidden tests lulus |
| Object-level authorization | ID client tidak dapat dipakai lintas scope | BOLA tests lulus |
| Validation/CORS/throttle | Entry point API diperkeras | Invalid payload dan abuse tests lulus |

### Tahap 2 - Runtime Completeness

| Item | Output | Definition Of Done |
| --- | --- | --- |
| Dashboard API | Halaman dashboard memuat metric resmi | Tidak ada `404`; authorization lulus |
| Monitoring API eksplisit | Browse operasional terbatas dan paginated | Scope/field tests lulus |

### Tahap 3 - Transaction Integrity

| Item | Output | Definition Of Done |
| --- | --- | --- |
| Kasir atomic decision + retry policy | Double-submit aman | Concurrency tests lulus |
| Farmasi transaction verification | Stok dan billing konsisten | Stock/rollback tests lulus |
| Tarif non-hardcoded | Billing mengikuti sumber tarif disetujui | Test tarif/config lulus |

### Tahap 4 - Test Infrastructure

| Item | Output | Definition Of Done |
| --- | --- | --- |
| Perbaikan test scaffolding Nest | Unit tests berjalan | `npm test -- --runInBand` lulus |
| Integration/e2e risk tests | Bukti perilaku kritis | Security dan transaction suite lulus |

### Tahap 5 - Frontend Gate

| Item | Output | Definition Of Done |
| --- | --- | --- |
| Hook correction | Effect/render behavior valid | Tidak ada hook lint violation |
| API typing | Data flow typed | Tidak ada `no-explicit-any` error |
| Route authorization UX | Menu/route sesuai izin | UI test/manual verification lulus |

### Tahap 6 - Documentation Alignment

| Dokumen | Pembaruan Wajib |
| --- | --- |
| `CURRENT_STATE.md` | Menggambarkan implementasi dan residual risk aktual |
| `TASK_LIST.md` | Check hanya item yang telah diverifikasi lulus |
| `RISK_REGISTER.md` | Mitigated partial vs open risk terpisah |
| `TESTING_MATRIX.md` | Status diisi dari bukti run, bukan niat implementasi |
| `Build_Summary.md` | Validasi terbaru serta endpoint coverage |
| `README.md` | Tautan dokumen dan asset valid |

## 11. Matriks Prioritas Dan Urutan Kerja

| Urutan | Pekerjaan | Risiko Yang Ditutup | Mengapa Mendahului Yang Lain |
| ---: | --- | --- | --- |
| 1 | Safety Git dan baseline | Kehilangan perubahan/audit buruk | Semua fix berikut perlu diff yang dapat dipercaya |
| 2 | Global auth, permission, object auth | Ekspos/modifikasi data pasien | Keamanan data lebih kritis dari perbaikan tampilan |
| 3 | Validation, CORS, throttle | Abuse/input/misconfiguration | Melengkapi perimeter API |
| 4 | Dashboard/monitoring protected API | Runtime failure/data exposure | Memperbaiki UI tanpa membuka surface baru |
| 5 | Kasir dan farmasi concurrency proof | Korupsi transaksi/stok | Perlu security dan test harness yang memadai |
| 6 | Backend test gate | Regression | Menahan perubahan berisiko berikutnya |
| 7 | Frontend lint/type/authorization UX | Kualitas dan pengalaman akses | Backend tetap otoritas keamanan |
| 8 | Sinkronisasi dokumen | Handover salah | Dokumen final harus berdasarkan hasil terverifikasi |

## 12. Definition Of Done Remediation Inti

Remediation inti hanya dinyatakan selesai bila:

- Auth backend bersifat protected-by-default dengan daftar route publik yang
  eksplisit.
- Endpoint write internal seluruhnya memiliki function authorization.
- Endpoint yang menerima ID pasien/transaksi sensitif memiliki object-level
  authorization.
- DTO validation, CORS policy, error policy, dan throttling endpoint publik
  telah diterapkan dan diuji.
- Dashboard dan monitoring memakai API protected yang tersedia dan
  terdefinisi sempit.
- Kasir terbukti mencegah pembayaran ganda dan collision jurnal pada skenario
  paralel.
- Farmasi terbukti tidak menyebabkan stok negatif atau partial commit.
- Backend build, backend test, frontend build, frontend lint, dan kompilasi
  skrip lulus.
- Dokumen status, risk register, test matrix, dan README sesuai bukti terbaru.
- Status production tetap ditolak sampai verifikasi kompatibilitas operasional
  dengan sistem legacy dan keputusan deployment resmi selesai.

## 13. Referensi Resmi

Referensi berikut diakses untuk menyusun rencana ini pada 27 Mei 2026.

### 13.1 NestJS

| Referensi | Penggunaan Dalam Rencana |
| --- | --- |
| [Authentication - NestJS](https://docs.nestjs.com/security/authentication) | Dasar JWT Bearer, global authentication guard, dan pola public route |
| [Guards - NestJS](https://docs.nestjs.com/guards) | Dasar `CanActivate`, metadata route, dan authorization guard |
| [Testing - NestJS](https://docs.nestjs.com/fundamentals/testing) | Dasar testing module, `overrideProvider()`, `overrideGuard()`, dan e2e testing |
| [Validation - NestJS](https://docs.nestjs.com/techniques/validation) | Dasar DTO validation dan `ValidationPipe` |

### 13.2 Prisma

| Referensi | Penggunaan Dalam Rencana |
| --- | --- |
| [Transactions and batch queries - Prisma](https://www.prisma.io/docs/orm/prisma-client/queries/transactions) | ACID transaction, interactive transaction, isolation `Serializable`, transaction singkat, dan retry konflik `P2034` |
| [Error reference - Prisma](https://www.prisma.io/docs/orm/reference/error-reference) | Interpretasi unique-constraint error `P2002` |

### 13.3 OWASP API Security

| Referensi | Penggunaan Dalam Rencana |
| --- | --- |
| [OWASP API Security Top 10 - 2023](https://owasp.org/API-Security/editions/2023/en/0x00-header/) | Kerangka risiko API untuk sistem data sensitif |
| [API1:2023 Broken Object Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/) | Keharusan verifikasi akses record berdasarkan ID request |
| [API2:2023 Broken Authentication](https://owasp.org/API-Security/editions/2023/en/0xa2-broken-authentication/) | Hardening autentikasi dan endpoint login |
| [API5:2023 Broken Function Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa5-broken-function-level-authorization/) | Default-deny dan explicit grant untuk fungsi sensitif |

### 13.4 Frontend Type Dan Effect Discipline

| Referensi | Penggunaan Dalam Rencana |
| --- | --- |
| [React `useEffect`](https://react.dev/reference/react/useEffect) | Penataan ulang effect/fetch dan dependency yang benar |
| [typescript-eslint `no-explicit-any`](https://typescript-eslint.io/rules/no-explicit-any/) | Mengganti `any` dengan model domain atau `unknown` yang dinarrow |

## 14. Catatan Penggunaan Dokumen

Dokumen ini adalah rencana berbasis source dan validasi lokal, bukan surat
persetujuan produksi. Setelah setiap tahap selesai, hasil eksekusi harus
dicatat pada `TESTING_MATRIX.md`, risiko diperbarui pada `RISK_REGISTER.md`,
dan klaim kondisi terkini diperbarui pada `CURRENT_STATE.md`.

## 15. Progress Eksekusi - 27 Mei 2026

### 15.1 Selesai Diterapkan

| Kontrol | Implementasi | Bukti Validasi |
| --- | --- | --- |
| Protected-by-default API | `JwtAuthGuard` dipasang sebagai `APP_GUARD`; `@Public()` ditambahkan untuk root, login, dan kiosk | E2E memastikan anonymous write ke Lab, Ranap, dan Operasi menghasilkan `401` |
| CORS baseline | `CORS_ORIGINS` dapat dikonfigurasi; default development hanya `http://localhost:5173` | Backend build lulus |
| Public payload validation | `ValidationPipe` global; DTO untuk login, pencarian pasien kiosk, dan registrasi kiosk | E2E memastikan payload login invalid dan field tambahan kiosk ditolak `400` |
| Public abuse control | `ThrottlerGuard` global; login dan registrasi kiosk dibatasi 5 request/menit, pencarian kiosk 20 request/menit | E2E memastikan percobaan login keenam ditolak `429` |
| Production startup path | Script `start:prod` diarahkan ke artifact build aktual `dist/src/main` | Bootstrap memuat route sebelum gagal koneksi database lokal yang tidak aktif |
| Unit-test scaffolding | Spec controller/service menggunakan mock dependency dan guard override sesuai boundary unit test | `npm test -- --runInBand` lulus, 22 suite/22 test |

### 15.2 Validasi Setelah Implementasi

| Perintah | Hasil |
| --- | --- |
| `cd simrs-backend && npm run build` | Lulus |
| `cd simrs-backend && npm test -- --runInBand auth/jwt-auth.guard.spec.ts` | Lulus, 1 test |
| `cd simrs-backend && npm test -- --runInBand` | Lulus, 22 suite/22 test |
| `cd simrs-backend && npm run test:e2e -- --runInBand security.e2e-spec.ts` | Lulus, 6 test |
| `PORT=3100 npm run start:prod` | Artifact path benar; startup berhenti pada `P1001` karena MariaDB lokal tidak berjalan |

### 15.3 Masih Terbuka

| Item | Alasan Belum Diselesaikan Pada Iterasi Ini |
| --- | --- |
| Permission spesifik Lab, Ranap, dan Operasi | Model Prisma `user` tidak memetakan kolom permission legacy; nama hak tidak boleh ditebak tanpa schema/database authoritative |
| Object-level authorization | Memerlukan keputusan mapping unit/actor terhadap encounter, resep, dan transaksi |
| DTO endpoint internal lain | Perlu pemetaan contract payload tiap modul agar tidak memutus frontend existing |
| Dashboard/Monitoring API | Harus dibuat sesudah permission/scope data ditetapkan agar tidak membuka data medis kepada semua user terautentikasi |
| Transaction proof Kasir/Farmasi | Memerlukan database test yang aktif dan fixture terkontrol |
| Frontend lint | Tetap merupakan tahap quality gate lanjutan |

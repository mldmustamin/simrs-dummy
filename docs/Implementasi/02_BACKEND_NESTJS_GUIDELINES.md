# Panduan Arsitektur Backend (NestJS)
*Standard Operating Procedure bagi AI Agent saat menulis kode backend API.*

## 1. Event-Driven Architecture (Pub/Sub)
Jangan memanggil *Service* lintas domain secara berantai panjang (Tight Coupling). Gunakan `@nestjs/event-emitter`.
- **Contoh Buruk**: `KasirService.bayar()` memanggil `ApotekService.kurangiStok()` dan `AkuntansiService.jurnal()`.
- **Contoh Baik**: `KasirService.bayar()` menembakkan event `kasir.pembayaran_sukses`. Kemudian `ApotekListener` dan `AkuntansiListener` merespons event tersebut secara independen.

## 2. Proteksi Concurrency & Pessimistic Locking
Setiap transaksi yang berkaitan dengan pengurangan stok fisik (Gudang/Apotek) dan *auto-numbering* kasir (Nomor Nota/Jurnal) **WAJIB** dikunci.
- Gunakan Prisma Raw Query untuk mengeksekusi `SELECT ... FOR UPDATE` jika berhadapan dengan data tunggal yang rentan *race-condition*.
- Selalu gunakan blok `$transaction` Prisma yang membungkus semua operasi terkait menjadi satu kesatuan atomik (ACID).

## 3. Mekanisme Graceful Degradation
API Backend harus mau menerima *payload* yang tidak lengkap dari frontend jika situasi mensyaratkan demikian.
- Gunakan DTO (Data Transfer Object) dengan validasi `IsOptional()` untuk data-data non-kritis (seperti Suhu, Tinggi Badan). Jangan me-reject keseluruhan EMR hanya karena perawat lupa menginput berat badan di tengah *mass casualty* IGD.

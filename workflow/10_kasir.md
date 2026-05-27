# Modul Kasir & Billing

Penyelesaian tagihan akhir (`Kasir.tsx`).

## Parameter Teknis & Endpoint
- **Kalkulasi Tagihan (Informed Consent)**: `GET /kasir/tagihan/{formattedNoRawat}`
- **Proses Pembayaran (ACID)**: `POST /kasir/bayar`
- **Integrasi Klaim**: `POST /api/casemix/klaim` (Jika berlaku)

## Mekanisme Sistem
Menerima `no_rawat`. API menghitung total biaya dari `reg_periksa` (karcis), `rawat_jl_dr/pr` (tindakan), `periksa_lab/radiologi`, serta total resep `detail_pemberian_obat`. 
Proses pelunasan `POST /kasir/bayar` dilindungi oleh blok `Prisma.$transaction` yang mengunci pembuatan `nota_jalan` dan `jurnal` akuntansi. Jika gagal akibat konfik *Unique Key* (P2002), sistem me- *rollback* dan mencoba lagi (maksimal 5x *retry*), sebelum mencetak struk dan membuka kunci (lock) apotek.

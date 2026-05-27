# Strategi Integrasi BPJS (Eventually Consistent)
*Aturan khusus agen untuk memprogram Bridging V-Claim agar tidak menyandera operasional Faskes.*

## 1. Flowchart Pendaftaran Asinkron
1. Pasien datang membawa rujukan/kartu. Petugas klik "Daftar BPJS".
2. **Frontend** menembak API Backend `POST /api/registrasi`.
3. **Backend** langsung menyimpan pasien ke tabel `reg_periksa` (Lokal) dan men-generate `no_rawat`. Backend menyuntikkan *task* pembuatan SEP ke tabel `simrs_web_background_job`.
4. **Backend** merespons `200 OK` ke frontend dalam waktu kurang dari 500ms. Pasien langsung disuruh duduk di depan Poli, **TANPA** memegang kertas SEP.
5. **Background Worker** (Cron Job) yang berjalan setiap menit mengambil *task* tersebut dan menembak API V-Claim BPJS Kemenkes.
6. Jika V-Claim *timeout* atau MT (Maintenance), *worker* akan menunda (*delay*) dan mencoba lagi (*retry exponential backoff*) 5 menit kemudian.
7. Ketika *worker* berhasil mendapat balasan dari BPJS, nomor SEP diekstrak dan disimpan ke dalam tabel `bridging_sep` milik pasien.

## 2. Penyelesaian Administratif Belakangan
- Kertas SEP bisa di-*print* kolektif oleh admin loket di sore hari, atau cukup ditandatangani pasien secara elektronik di akhir layanan saat mengambil obat di Apotek.
- Arsitektur ini memastikan loket pendaftaran bebas dari penumpukan panjang saat server BPJS nasional sedang tumbang.

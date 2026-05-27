# Strategi Integrasi BPJS (Enterprise to Pragmatic)
*Visi Utama: Sinkronisasi real-time paripurna, didukung oleh sistem *Eventually Consistent* sebagai peredam kejut.*

## 1. Flow Real-time (Mode Ideal)
Pada kondisi jaringan BPJS sehat, integrasi beroperasi 100% *real-time*.
1. Petugas klik "Daftar BPJS".
2. API langsung menembak V-Claim, SEP terbit instan (< 1 detik).
3. Pasien memegang validasi digital dan langsung menuju Poli.
4. *Trigger* ke SEP dan INA-CBG terhubung mulus.

## 2. Flow Asinkron (Mode Fallback / Pragmatis)
Ketika server V-Claim tumbang, ERP kita **TIDAK BOLEH** ikut tumbang. Sistem harus beralih mulus ke mode Asinkron.
1. Frontend mengirim *request* ke backend, backend mendeteksi *timeout* dari V-Claim.
2. Backend seketika mengaktifkan mode *Graceful Degradation*: Pasien tetap disimpan di `reg_periksa` (Lokal) dengan nomor antrean RS.
3. Pembuatan SEP dialihkan ke tabel `simrs_web_background_job`.
4. *Cron Job Worker* akan mencoba kembali (*retry exponential backoff*) tanpa disadari petugas.
5. Saat berhasil, SEP diinjeksi ke tabel pasien. Petugas administrasi menyelesaikan sisa urusan kertas secara kolektif di kemudian waktu tanpa menghalangi jalan pasien ke ruang periksa.

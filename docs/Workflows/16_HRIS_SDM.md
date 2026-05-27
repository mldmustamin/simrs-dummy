# Workflow Modul HRIS & Kepegawaian (SDM)
> **Status**: *On-going modul*

## 1. Deskripsi Umum
Sistem kepegawaian, *payroll* (penggajian), jadwal *shift* perawat, insentif dokter (Fee for Service), dan absensi.

## 2. Aktor Terlibat
- Staf HRD
- Seluruh Pegawai

## 3. Alur Kerja (Ideal & Fallback)
1. **Manajemen Shift:** Kepala Ruangan menyusun jadwal Pagi/Siang/Malam untuk perawat bangsal di sistem.
2. **Absensi & Lembur:** Data absensi (fingerprint/face recognition) ditarik masuk ke ERP.
3. **Kalkulasi Jasa Medis:** ERP menghitung berapa kali Dokter A melakukan operasi atau periksa poli dalam 1 bulan, dan mengakumulasikan *Fee for Service*-nya.
4. **Payroll:** Gaji pokok + Tunjangan + Jasa Medis - Potongan diproses. Slip gaji elektronik dikirim ke aplikasi/email pegawai.

## 4. Trigger & Integrasi
- **Menembak Event:** `HRIS.PayrollSelesai` -> Memasukkan beban gaji ke dalam Modul Akuntansi.

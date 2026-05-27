import re

file_path = "/home/gudang-data-kantor/simrs-web/docs/ALUR_OPERASIONAL_FASKES.md"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

bangsal_content = """## 4. Kehidupan Bangsal (Rawat Inap) & Asuhan Keperawatan
Unit Bangsal adalah tempat di mana pasien menghabiskan 90% waktunya di rumah sakit. Berbeda dengan unit lain yang transaksional, bangsal beroperasi 24/7 tanpa henti dengan dinamika *shift* perawat dan rutinitas medis yang sangat padat.

### A. Perjalanan Pasien & Rutinitas Bangsal (Patient Journey)
1. **Penerimaan Pasien Baru (Transfer In):** Pasien tiba di bangsal dari IGD/Poli/OK. Perawat bangsal melakukan orientasi ruangan (menjelaskan tombol bel, letak kamar mandi, jadwal makan, jam besuk).
2. **Asesmen Awal Keperawatan:** Perawat melakukan pengkajian fisik lengkap (head-to-toe), risiko jatuh (Morse Fall Scale), dan skrining nyeri.
3. **Ronde Medis (Visite Dokter DPJP):** Setiap pagi/sore, dokter penanggung jawab (DPJP) melakukan *visite*, memeriksa pasien, membaca laporan perawat, dan memberikan instruksi pengobatan baru.
4. **Pemberian Obat (Medication Administration):** Perawat memberikan obat ke pasien sesuai jadwal (misal: per 8 jam) dengan prinsip "7 Benar Obat" (Benar Pasien, Obat, Dosis, Cara, Waktu, Dokumentasi, Informasi).
5. **Observasi TTV Berkala:** Pemeriksaan suhu, nadi, pernapasan, dan tekanan darah setiap 4-6 jam atau lebih sering tergantung tingkat keparahan pasien.
6. **Perawatan Luka & Tindakan Mandiri:** Perawat melakukan ganti perban, memandikan pasien (untuk total care), atau membantu mobilisasi.
7. **Pergantian Shift (Handover):** Setiap pergantian shift (Pagi->Siang->Malam), perawat melakukan operan bed-to-bed menggunakan metode SBAR (Situation, Background, Assessment, Recommendation).
8. **Discharge Planning:** Persiapan kepulangan sejak H-1, edukasi perawatan di rumah, dan penyerahan resume medis serta obat pulang.

### B. Perjalanan Sistem ERP (Data Lifecycle)
1. **Bed Management Real-time:** Status kasur berubah dinamis: Kosong -> Dibooking -> Ditempati -> Rencana Pulang -> Kotor (Cleaning) -> Kosong.
2. **E-MAR (Electronic Medication Administration Record):** Sistem mencentang *barcode* obat dan *barcode* gelang pasien sebelum perawat menyuntikkan obat untuk mencegah malpraktik (Salah Obat).
3. **CPPT Terintegrasi:** Catatan Perkembangan Pasien Terintegrasi di mana catatan perawat, instruksi dokter, dan catatan ahli gizi tergabung dalam satu *timeline* berurutan.
4. **Auto-Billing Akomodasi:** Pada pukul 00:00 (Midnight Census), ERP secara otomatis menagihkan biaya sewa kamar, visit dokter, dan asuhan keperawatan ke *billing* pasien tanpa campur tangan manual admin ruangan.
5. **Request Penunjang dari Bangsal:** Perawat dapat meng-klik tombol "Order Darah" atau "Order Rontgen Bed-side" dari tablet di samping kasur pasien.

### C. Integrasi Eksternal (Bridging BPJS/Kemenkes)
- [API/Bridging] Integrasi aplikasi SIRANAP Kemenkes (Sistem Informasi Rawat Inap) yang melaporkan ketersediaan tempat tidur RS secara *real-time* ke publik.
- [API/Bridging] Pengiriman data LOS (Length of Stay) untuk kalkulasi INA-CBG JKN.

### D. Penanganan Edge Cases & Force Majeure
- ⚠️ **Kasus Kritis:** Pasien henti jantung mendadak di bangsal. Perawat menekan tombol *Code Blue*. ERP membunyikan alarm *Code Blue* di seluruh monitor perawat dan paging RS, mencatat waktu *Response Time* tim resusitasi.
- ⚠️ **Kasus Kritis:** Pasien menolak tindakan/obat (Refusal of Treatment). Perawat mengaktifkan form penolakan digital di sistem yang wajib di-TTE (Tanda Tangan Elektronik) oleh keluarga pasien agar terhindar dari tuntutan hukum.
- ⚠️ **Kasus Kritis:** Bayi di bangsal anak diculik. Perawat menekan tombol *Code Pink*, memicu ERP untuk mengunci (*lockdown*) seluruh pintu sayap bangsal.
- ⚠️ **Kasus Kritis:** Pasien BPJS diam-diam naik kelas VIP atas permintaan keluarga tanpa lapor ke BPJS. ERP mendeteksi pelanggaran selisih bayar dan membekukan sementara *billing* kasir hingga administrasi selesai.

### E. Aktor Sistem (Role-Based Access Control)
Akses terhadap modul Bangsal ini dibatasi hanya untuk: `Kepala Ruangan, Perawat Pelaksana (Shift), Dokter DPJP, Ahli Gizi Ruangan, Admin Ruangan`.

"""

# Regex to find section 4 and replace it up to section 5
pattern = re.compile(r"## 4\. Rawat Inap.*?## 5\.", re.DOTALL)
new_content = pattern.sub(bangsal_content + "## 5.", content)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print("Updated Bangsal/Rawat Inap section successfully.")

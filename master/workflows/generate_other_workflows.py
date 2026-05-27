import os

folder_path = "/home/gudang-data-kantor/simrs-web/docs/Workflows"

other_workflows = {
    "11_Gizi_Dapur_Sentral.md": """# Workflow Modul Instalasi Gizi & Dapur Sentral
> **Status**: *On-going modul*

## 1. Deskripsi Umum
Memastikan asupan gizi pasien rawat inap sesuai dengan instruksi klinis dokter, mencatat pemakaian bahan mentah dapur harian, serta melacak alergi makanan.

## 2. Aktor Terlibat
- Ahli Gizi (Dietisien)
- Koki / Petugas Dapur RS

## 3. Alur Kerja (Ideal & Fallback)
1. **Penerimaan Order Diet:** Sistem menarik instruksi diet dari EMR Rawat Inap secara *real-time*.
2. **Kompilasi Kebutuhan (Pagi/Siang/Sore):** ERP menghitung otomatis total porsi Bubur, Nasi, Diet Rendah Garam, dll untuk satu rumah sakit.
3. **Pencetakan Barcode Nampan:** Nampan makanan dilabeli *barcode* yang berisi nama pasien, bangsal, dan peringatan alergi (misal: "Alergi Udang").
4. **Distribusi:** Makanan diantar ke bangsal.
5. **Inventaris Dapur:** Pengurangan stok bahan basah dan kering di Gudang Gizi.

## 4. Trigger & Integrasi
- **Menembak Event:** `Gizi.OrderSelesai`.
""",
    
    "12_IPSRS_Teknisi.md": """# Workflow Modul IPSRS (Pemeliharaan Fasilitas & Elektro Medik)
> **Status**: *On-going modul*

## 1. Deskripsi Umum
Manajemen pemeliharaan gedung, AC, listrik, genset, serta kalibrasi rutin alat medis (Ventilator, Patient Monitor).

## 2. Aktor Terlibat
- Kepala IPSRS
- Teknisi / Mekanik

## 3. Alur Kerja (Ideal & Fallback)
1. **Sistem Tiket (Helpdesk):** Perawat Bangsal mengirim tiket keluhan (misal: "AC Bocor di Kamar 203").
2. **Penugasan (Dispatch):** Kepala IPSRS menugaskan teknisi. Tiket berubah status menjadi `In Progress`.
3. **Pemakaian Sparepart:** Teknisi mengambil suku cadang (Freon, Kabel) dari Gudang Teknik. Stok dipotong.
4. **Penyelesaian:** Teknisi memfoto bukti perbaikan dari aplikasi *mobile*. Status tiket menjadi `Closed`.
5. **Preventive Maintenance:** ERP membunyikan alarm jadwal kalibrasi alat medis yang akan jatuh tempo dalam 30 hari.

## 4. Trigger & Integrasi
- **Bridging:** ASPAK Kemenkes (Aplikasi Sarana Prasarana dan Alat Kesehatan).
""",
    
    "13_Kamar_Jenazah_Forensik.md": """# Workflow Modul Kamar Jenazah & Forensik
> **Status**: *On-going modul*

## 1. Deskripsi Umum
Manajemen pemulasaraan jenazah, penyimpanan di lemari pendingin (freezer), visum, dan penyewaan ambulans jenazah.

## 2. Aktor Terlibat
- Dokter Forensik
- Petugas Kamar Jenazah
- Supir Ambulans

## 3. Alur Kerja (Ideal & Fallback)
1. **Penerimaan Jenazah:** Jenazah dikirim dari IGD/Ranap. Status Rekam Medis (RM) pasien dikunci menjadi `Meninggal/Deceased`.
2. **Pemulasaraan:** Tindakan memandikan, mengkafani/memakaikan baju, atau formalin dicatat di sistem.
3. **Sewa Freezer:** Jika keluarga belum mengambil, ERP menghitung sewa freezer per 24 jam.
4. **Penerbitan Surat:** Surat Keterangan Kematian dicetak dan ditandatangani digital.
5. **Keluar:** Ambulans dipesan via sistem Kasir. Jenazah dibawa pulang.

## 4. Trigger & Integrasi
- **Menembak Event:** `Jenazah.Keluar` -> Meng-update laporan mortalitas bulanan RS.
""",
    
    "14_Limbah_B3_Kesling.md": """# Workflow Modul Kesehatan Lingkungan (Kesling) & Limbah B3
> **Status**: *On-going modul*

## 1. Deskripsi Umum
Pencatatan harian volume sampah infeksius, non-infeksius, dan benda tajam, serta pelaporan vendor pengolah limbah.

## 2. Aktor Terlibat
- Petugas Sanitarian
- Vendor Pihak Ketiga

## 3. Alur Kerja (Ideal & Fallback)
1. **Penimbangan Harian:** Petugas menimbang kantong kuning (infeksius) dari tiap ruangan. Data berat (Kg) dimasukkan ke ERP.
2. **Penyimpanan di TPS B3:** Akumulasi volume limbah dihitung otomatis oleh sistem. Jika mendekati kapasitas maksimal TPS, alarm menyala.
3. **Pengangkutan Vendor:** Vendor (misal: PT. Waste) mengambil limbah. Serah terima (Manifest) dicetak dari sistem.

## 4. Trigger & Integrasi
- **Bridging:** SIRAJA Limbah (Sistem Informasi Pelaporan Pengelolaan Limbah B3 Kementerian LHK).
""",
    
    "15_Keuangan_Akuntansi.md": """# Workflow Modul Keuangan & Akuntansi Sentral
> **Status**: *On-going modul*

## 1. Deskripsi Umum
Penyusunan Jurnal Umum otomatis dari modul pelayanan, Buku Besar, Neraca, Laba/Rugi, dan Account Payable/Receivable.

## 2. Aktor Terlibat
- Akuntan
- Direktur Keuangan

## 3. Alur Kerja (Ideal & Fallback)
1. **Auto-Posting Jurnal:** Setiap ada pasien bayar, obat dibeli (PO), atau operasi selesai, ERP secara *background* membuat jurnal (Debet/Kredit).
2. **Hutang Dagang (A/P):** Saat barang Farmasi masuk gudang, nilai faktur masuk ke antrean Hutang. Keuangan memproses pembayaran ke vendor.
3. **Piutang BPJS (A/R):** Tagihan Casemix masuk sebagai piutang. Ketika BPJS mentransfer dana, Akuntan mencatat rekonsiliasi pembayaran.
4. **Closing Bulanan:** Laporan Neraca & Laba Rugi digenerate setiap akhir bulan.

## 4. Trigger & Integrasi
- **Integrasi Internal:** Modul sentral (Muara dari semua transaksi).
""",
    
    "16_HRIS_SDM.md": """# Workflow Modul HRIS & Kepegawaian (SDM)
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
""",
    
    "17_Hemodialisa.md": """# Workflow Modul Hemodialisa (Cuci Darah)
> **Status**: *On-going modul*

## 1. Deskripsi Umum
Layanan tindakan cuci darah rutin yang membutuhkan manajemen mesin (*Machine Utilization*) dan siklus kunjungan pasien kronis.

## 2. Aktor Terlibat
- Perawat Hemodialisa
- Dokter Spesialis Penyakit Dalam (KGH)

## 3. Alur Kerja (Ideal & Fallback)
1. **Penjadwalan Mesin:** Pasien gagal ginjal kronis dijadwalkan secara reguler (misal: tiap Selasa dan Jumat). Sistem mem-booking *slot* Mesin HD.
2. **Pre-Tindakan:** Pengukuran berat badan basah, tekanan darah.
3. **Intra-Tindakan:** Pencatatan *Ultrafiltration Rate*, BHP (Dialyzer, Bloodline), Heparin.
4. **Post-Tindakan:** Evaluasi klinis. Pengulangan otomatis rujukan internal BPJS (biasanya rujukan berlaku 3 bulan).
""",
    
    "18_Medical_Check_Up.md": """# Workflow Modul Medical Check Up (MCU)
> **Status**: *On-going modul*

## 1. Deskripsi Umum
Layanan pemeriksaan kesehatan preventif baik untuk individu maupun korporat (Perusahaan).

## 2. Aktor Terlibat
- Petugas MCU
- Dokter Umum / Spesialis

## 3. Alur Kerja (Ideal & Fallback)
1. **Pendaftaran Paket:** Pasien (atau rombongan karyawan pabrik) didaftarkan dengan "Paket MCU Silver/Gold".
2. **Routing Otomatis:** Sistem memecah antrean ke Lab, Radiologi, Audiometri, dan Poli Mata tanpa perlu order manual dokter.
3. **Kompilasi Hasil:** Seluruh hasil dari penunjang otomatis terkumpul dalam satu *dashboard* Buku Laporan MCU.
4. **Verifikasi Kesimpulan:** Dokter MCU menarik kesimpulan akhir (*Fit to Work* / *Unfit*).
""",
    
    "19_Rehabilitasi_Medik.md": """# Workflow Modul Rehabilitasi Medik & Fisioterapi
> **Status**: *On-going modul*

## 1. Deskripsi Umum
Pelayanan fisioterapi, terapi okupasi, dan terapi wicara yang sifatnya berseri (beberapa kali kunjungan untuk satu rujukan).

## 2. Aktor Terlibat
- Fisioterapis
- Dokter Spesialis KFR

## 3. Alur Kerja (Ideal & Fallback)
1. **Evaluasi Awal:** Dokter Spesialis KFR menentukan program terapi (misal: 6 kali kunjungan TENS).
2. **Pelaksanaan Terapi:** Fisioterapis mengeksekusi terapi per sesi.
3. **Protokol Klaim:** ERP akan otomatis mengingatkan jika sesi terapi pasien BPJS sudah melebihi batas kuota bulanan.
""",
    
    "20_Bank_Darah_BDRS.md": """# Workflow Modul Bank Darah RS (BDRS)
> **Status**: *On-going modul*

## 1. Deskripsi Umum
Manajemen stok kantong darah, uji silang serasi (Crossmatch), dan donor pengganti.

## 2. Aktor Terlibat
- Petugas BDRS

## 3. Alur Kerja (Ideal & Fallback)
1. **Request Darah:** Dokter operasi / IGD memesan 2 kantong PRC via sistem (Gol. Darah B).
2. **Pengadaan:** Jika stok kosong, petugas menerbitkan surat rujukan darah ke PMI secara sistem.
3. **Crossmatch:** Sampel darah pasien diuji silang dengan kantong darah di lab. Hasil diinput ke ERP.
4. **Distribusi:** Kantong darah dengan *barcode* diambil perawat bangsal. Tagihan biaya pengolahan darah otomatis masuk ke kasir.
""",
    
    "21_Customer_Service_Humas.md": """# Workflow Modul Customer Service & Humas
> **Status**: *On-going modul*

## 1. Deskripsi Umum
Manajemen keluhan pelanggan, informasi RS, dan registrasi pendaftaran pasien *online*.

## 2. Aktor Terlibat
- Customer Service

## 3. Alur Kerja (Ideal & Fallback)
1. **Ticketing Komplain:** Komplain pasien via Whatsapp/Web RS otomatis ditarik menjadi 'Tiket' di ERP (misal: "Toilet lantai 2 kotor").
2. **Eskalasi:** CS mengarahkan tiket ke Cleaning Service / IPSRS.
3. **Broadcast:** Humas mengirimkan notifikasi *blast* jadwal libur dokter spesialis ke pasien *chronic* (prolanis).
""",
    
    "22_Laundry_Linen.md": """# Workflow Modul Laundry & Manajemen Linen
> **Status**: *On-going modul*

## 1. Deskripsi Umum
Pengelolaan perputaran linen (sprei, selimut, baju operasi) yang kotor, infeksius, hingga kembali bersih.

## 2. Aktor Terlibat
- Petugas Laundry

## 3. Alur Kerja (Ideal & Fallback)
1. **Penimbangan Kotor:** Linen kotor dari bangsal dibawa dan ditimbang (Kg). Dipisah antara bak Infeksius (Merah) dan Non-Infeksius.
2. **Pencucian:** Mesin dioperasikan, ERP mencatat penggunaan deterjen kimia harian dari gudang linen.
3. **Distribusi Bersih:** Linen bersih disimpan ke lemari penyimpanan. Ruangan menarik (*Request*) stok linen bersih via ERP.
"""
}

for filename, content in other_workflows.items():
    file_path = os.path.join(folder_path, filename)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

print(f"Berhasil membuat 12 dokumen Workflow tambahan di dalam {folder_path}.")

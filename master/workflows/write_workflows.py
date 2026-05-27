import os
import shutil

doc_dir = "/home/gudang-data-kantor/simrs-web/workflow"
if os.path.exists(doc_dir):
    shutil.rmtree(doc_dir)
os.makedirs(doc_dir, exist_ok=True)

docs = {
    "01_pendaftaran.md": """# Pendaftaran (Registrasi Kunjungan)

Modul ini menangani registrasi kunjungan pasien ke rumah sakit.
- **Fungsionalitas**: Pendaftaran pasien baru/lama, pemilihan poliklinik tujuan, registrasi Kios Mandiri (APM), dan Bypass Lab/Radiologi (APS).
- **Alur Kerja**: Pasien datang -> Input Data RM -> Validasi Database -> Pilih Poli/Dokter -> Generate No Rawat & No Reg -> Cetak Struk.
""",
    "02_antrean.md": """# Antrean (Monitor Poliklinik)

Modul ini berfungsi sebagai layar pemantauan antrean publik dan manajemen antrean di poliklinik.
- **Fungsionalitas**: Menampilkan nomor antrean berjalan, memanggil pasien secara berurutan, dan memberikan visualisasi waktu tunggu.
- **Alur Kerja**: Pasien mendaftar -> Masuk ke list Antrean -> Tampil di Layar TV (QueueDisplay) -> Dipanggil oleh Perawat Poli -> Masuk Ruang Periksa.
""",
    "03_bed_management.md": """# Bed Management (Ketersediaan Kamar)

Modul ini digunakan oleh bagian admisi rawat inap untuk memonitor ketersediaan tempat tidur (bed) secara real-time.
- **Fungsionalitas**: Pemetaan status kamar (Tersedia, Terisi, Dibersihkan, Rusak), mutasi kamar pasien, dan pemesanan kamar (booking).
- **Alur Kerja**: Pasien direkomendasikan Ranap -> Petugas cek BedManagement -> Pilih bed kosong -> Status bed menjadi 'Terisi' -> Saat pasien pulang, status bed menjadi 'Dibersihkan'.
""",
    "04_rme_rawat_jalan.md": """# RME (Catatan Klinis Rawat Jalan)

Modul ini digunakan oleh dokter poliklinik untuk mengisi rekam medis elektronik pasien rawat jalan.
- **Fungsionalitas**: Pengisian SOAP (Subjektif, Objektif, Asesmen, Plan), Diagnosa ICD-10, E-Resep, dan Order Laboratorium.
- **Alur Kerja**: Dokter buka RME Pasien -> Input keluhan & vital signs -> Input Diagnosa -> Input Resep -> Simpan (terkunci).
""",
    "05_cppt_rawat_inap.md": """# CPPT Rawat Inap (Observasi Harian)

Modul ini merupakan Catatan Perkembangan Pasien Terintegrasi (CPPT) khusus untuk pasien yang dirawat inap.
- **Fungsionalitas**: Pencatatan SOAP harian oleh dokter penanggung jawab (DPJP) dan perawat jaga, grafik suhu/nadi, dan instruksi medis berkelanjutan.
- **Alur Kerja**: Perawat operan shift -> Cek pasien ranap -> Input observasi harian di RanapCPPT -> Dokter Visit -> Dokter tambahkan asesmen lanjutan.
""",
    "06_farmasi.md": """# Farmasi (Penyusunan E-Resep)

Modul ini berkaitan dengan gudang farmasi dan peracikan resep sebelum diserahkan ke pasien.
- **Fungsionalitas**: Manajemen stok gudang obat, penerimaan e-resep dari dokter, telaah resep (clinical review), dan peracikan obat (puyer/kapsul).
- **Alur Kerja**: Resep masuk dari RME -> Apoteker telaah interaksi obat -> Apoteker/Asisten meracik dan menyiapkan obat -> Resep divalidasi siap serah.
""",
    "07_apotek.md": """# Apotek (Validasi dan Penyerahan Obat)

Modul ini adalah loket akhir penyerahan obat ke pasien dan penjualan obat bebas (OTC).
- **Fungsionalitas**: Validasi pembayaran kasir (kunci serah obat), penyerahan obat dengan KIE (Konseling Informasi Obat), dan penjualan bebas.
- **Alur Kerja**: Obat selesai diracik -> Cek status lunas di Kasir -> Jika Lunas, panggil pasien -> Serahkan obat -> Stok inventory berkurang otomatis (Row-Level Locking).
""",
    "08_laboratorium.md": """# Laboratorium (Antrean dan Hasil Pemeriksaan)

Modul ini menangani permintaan tes diagnostik, baik dari rujukan poli maupun permintaan sendiri (APS).
- **Fungsionalitas**: Menerima pesanan lab, input hasil pemeriksaan (angka/nilai rujukan), dan cetak PDF ekspertise.
- **Alur Kerja**: Terima order dari Poli/Admisi -> Ambil sampel darah/urin pasien -> Analisis alat -> Petugas Lab input hasil ke sistem -> Hasil terkirim ke layar RME Dokter.
""",
    "09_operasi.md": """# Operasi (Pencatatan Tindakan IBS)

Modul ini mengelola antrean dan pencatatan tindakan di Instalasi Bedah Sentral (IBS).
- **Fungsionalitas**: Jadwal booking operasi, pencatatan tim medis (operator, anestesi, asisten), durasi operasi, dan laporan pembedahan.
- **Alur Kerja**: Poli/Ranap ajukan jadwal operasi -> IBS konfirmasi jadwal -> Pelaksanaan Operasi -> Input tim dan laporan -> Tagihan operasi otomatis masuk ke Kasir.
""",
    "10_kasir.md": """# Kasir (Pembayaran dan Billing)

Modul ini mengakumulasi seluruh biaya selama kunjungan pasien (karcis, tindakan, obat, lab) untuk pembayaran akhir.
- **Fungsionalitas**: Akumulasi billing terpusat, Informed Financial Consent, pembayaran tunai/non-tunai, dan pencetakan nota lunas.
- **Alur Kerja**: Kasir masukkan No. Rawat -> Tampil rincian tagihan -> Pasien bayar -> Prisma Transaction Lock untuk anti-dobel nota -> Cetak Struk -> Apotek otomatis terbuka.
"""
}

for filename, content in docs.items():
    with open(os.path.join(doc_dir, filename), "w") as f:
        f.write(content)

print(f"Successfully created 10 workflow docs in {doc_dir}")

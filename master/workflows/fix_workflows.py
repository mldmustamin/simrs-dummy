import os
import shutil

# Target new folder
new_folder = "/home/gudang-data-kantor/simrs-web/docs/planning_and_roadmaps/Workflows"
os.makedirs(new_folder, exist_ok=True)

# 1. Regenerate the 22 workflows
workflows = {
    "01_Pendaftaran_Admisi.md": "# Workflow Modul Pendaftaran & Admisi\n\nModul ini adalah pintu masuk pertama pasien. Bertanggung jawab mencatat demografi, mencetak RM baru, mendistribusikan antrean ke Poli/IGD, dan menerbitkan SEP BPJS.\n\n*Mode Pragmatis*: Jika BPJS timeout, pendaftaran tetap jalan secara lokal, SEP ditarik di background.",
    "02_Poliklinik_Rawat_Jalan.md": "# Workflow Modul Poliklinik (Rawat Jalan)\n\nTempat dilakukannya Asuhan Keperawatan awal dan Pemeriksaan Medis (SOAP) oleh dokter spesialis.\n\n*Mode Pragmatis*: Mendukung pengisian SOAP retrospektif (input mundur) bagi dokter yang sibuk.",
    "03_Rawat_Inap_Bangsal.md": "# Workflow Modul Rawat Inap (Bangsal)\n\nModul dinamis untuk manajemen bed, asuhan keperawatan 24/7 (SBAR, CPPT), pemberian obat (E-MAR).\n\n*Fitur Ideal*: Auto-Billing Midnight Census.",
    "04_IGD_Triase.md": "# Workflow Modul Instalasi Gawat Darurat (IGD)\n\nPenanganan pasien prioritas tinggi (Triase Merah/Kuning/Hijau/Hitam).\n\n*Mode Pragmatis*: Mendukung Verbal Order darurat tanpa input EMR di muka.",
    "05_Apotek_Farmasi.md": "# Workflow Modul Instalasi Farmasi (Apotek)\n\nManajemen peracikan resep, pengurangan stok FIFO/FEFO, kalkulasi margin HNA, dan PIO.\n\n*Fitur Ideal*: Pessimistic Lock untuk mencegah double-dispensing obat.",
    "06_Kasir_Billing.md": "# Workflow Modul Kasir & Billing\n\nKonsolidasi seluruh biaya layanan pasien menjadi satu invoice terpusat.\n\n*Mode Pragmatis*: Mendukung PIN Emergency Override dari Direksi untuk meloloskan pasien miskin/Bad Debt.",
    "07_Laboratorium_Radiologi.md": "# Workflow Modul Laboratorium & Radiologi\n\nPenunjang medis. Menerima order (CPOE) dari dokter.\n\n*Fitur Ideal*: Mesin LIS/PACS mengirim hasil langsung (HL7/DICOM) ke ERP.",
    "08_Kamar_Operasi_CSSD.md": "# Workflow Modul Kamar Operasi (OK) & CSSD\n\nPenjadwalan operasi ketat, pemotongan BHP intra-operasi, dan siklus Autoclave sterilisasi instrumen bedah.",
    "09_Logistik_Gudang.md": "# Workflow Modul Gudang Logistik\n\nRantai pasok (Purchase Request, PO, Goods Receipt) dan Stock Opname.\n\n*Fitur Ideal*: Menghitung HPP dengan algoritma Moving Average otomatis.",
    "10_Rekam_Medis_Casemix.md": "# Workflow Modul Rekam Medis (Filing & Casemix)\n\nValidasi kelengkapan TTE, Koding ICD-10/9CM, Grouping INA-CBG, dan pengiriman Klaim Piutang BPJS.",
    "11_Gizi_Dapur_Sentral.md": "# Workflow Modul Instalasi Gizi & Dapur Sentral\n> **Status**: *On-going modul*\n\nDistribusi nampan makanan pasien dengan validasi barcode alergi dan penghitungan stok dapur.",
    "12_IPSRS_Teknisi.md": "# Workflow Modul IPSRS (Teknisi)\n> **Status**: *On-going modul*\n\nSistem Tiket Helpdesk (Kerusakan AC/Listrik) dan alarm kalibrasi alat medis berkala.",
    "13_Kamar_Jenazah_Forensik.md": "# Workflow Modul Kamar Jenazah & Forensik\n> **Status**: *On-going modul*\n\nPemulasaraan jenazah, sewa freezer, visum, dan penyewaan ambulans.",
    "14_Limbah_B3_Kesling.md": "# Workflow Modul Kesehatan Lingkungan & Limbah B3\n> **Status**: *On-going modul*\n\nPencatatan volume limbah infeksius harian dan pencetakan Manifest vendor pihak ketiga.",
    "15_Keuangan_Akuntansi.md": "# Workflow Modul Keuangan & Akuntansi\n> **Status**: *On-going modul*\n\nAuto-Posting Jurnal dari kasir/apotek, Buku Besar, Neraca, Laba/Rugi, dan Account Payable/Receivable.",
    "16_HRIS_SDM.md": "# Workflow Modul HRIS & Kepegawaian\n> **Status**: *On-going modul*\n\nPayroll, penjadwalan shift perawat, dan kalkulasi Insentif/Jasa Medis (Fee for Service).",
    "17_Hemodialisa.md": "# Workflow Modul Hemodialisa\n> **Status**: *On-going modul*\n\nPenjadwalan mesin HD rutin, pencatatan Ultrafiltration Rate, dan perpanjangan surat rujukan otomatis.",
    "18_Medical_Check_Up.md": "# Workflow Modul Medical Check Up (MCU)\n> **Status**: *On-going modul*\n\nPendaftaran Paket MCU (Silver/Gold) yang me-routing otomatis pasien ke Lab/Rontgen/Poli Mata.",
    "19_Rehabilitasi_Medik.md": "# Workflow Modul Rehabilitasi Medik\n> **Status**: *On-going modul*\n\nManajemen sesi terapi berseri untuk pasien fisioterapi.",
    "20_Bank_Darah_BDRS.md": "# Workflow Modul Bank Darah RS (BDRS)\n> **Status**: *On-going modul*\n\nPesanan kantong darah, uji silang (Crossmatch) di Lab, dan pemotongan stok darah PMI.",
    "21_Customer_Service_Humas.md": "# Workflow Modul Customer Service & Humas\n> **Status**: *On-going modul*\n\nManajemen keluhan (Ticketing Komplain dari WA/Web) dan broadcast pesan ke pasien kronis.",
    "22_Laundry_Linen.md": "# Workflow Modul Laundry & Manajemen Linen\n> **Status**: *On-going modul*\n\nPenimbangan linen kotor, siklus cuci, dan distribusi linen bersih kembali ke ruangan."
}

for filename, content in workflows.items():
    with open(os.path.join(new_folder, filename), "w", encoding="utf-8") as f:
        f.write(content)

# 2. Move the original massive operational flow into this new folder
old_alur = "/home/gudang-data-kantor/simrs-web/docs/planning_and_roadmaps/ALUR_OPERASIONAL_FASKES.md"
if os.path.exists(old_alur):
    shutil.move(old_alur, os.path.join(new_folder, "00_ALUR_OPERASIONAL_FASKES_MASTER.md"))

# 3. Delete the old workflows folder
old_workflows_dir = "/home/gudang-data-kantor/simrs-web/docs/Workflows"
if os.path.exists(old_workflows_dir):
    shutil.rmtree(old_workflows_dir)

print("Berhasil menyatukan semua workflow (termasuk yang lama) dalam 1 folder di docs/planning_and_roadmaps/Workflows dan menghapus folder lama.")

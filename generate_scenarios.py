import random

facilities = [
    "RS Umum Pemerintah Daerah", 
    "RS Swasta Tipe B", 
    "Puskesmas Kecamatan (Rawat Inap)", 
    "Puskesmas Kelurahan (Rawat Jalan)",
    "Klinik Umum Multi Poli", 
    "Klinik Khusus Spesialis (Mata/Gigi/Kandungan)"
]

patients = [
    "Pasien Umum (Out-of-Pocket / Mandiri)", 
    "Pasien BPJS Kesehatan (PBI/Non-PBI)", 
    "Pasien Asuransi Swasta (Corporate)", 
    "Pasien Rujukan Perusahaan (Inhouse Clinic)"
]

departments = [
    "Pendaftaran (Front Office) & Admisi", 
    "Instalasi Gawat Darurat (IGD)", 
    "Poliklinik Penyakit Dalam",
    "Poliklinik Gigi & Mulut", 
    "Poliklinik Anak", 
    "Poliklinik Kandungan (Obgyn)",
    "Poliklinik Saraf",
    "Poliklinik Jantung",
    "Laboratorium Patologi Klinik", 
    "Radiologi (X-Ray/USG/CT-Scan)", 
    "Apotek & Farmasi Rawat Jalan",
    "Apotek Rawat Inap & IGD", 
    "Ruang Perawatan (Rawat Inap Kelas 1/2/3)", 
    "Kamar Operasi (Bedah Sentral / OK)",
    "Ruang Bersalin (VK)",
    "Ruang Perawatan Intensif (ICU/NICU/PICU)",
    "Kasir Sentral & Billing", 
    "Gudang Logistik Medis & Farmasi", 
    "Gudang ATK & Non-Medis",
    "Instalasi Gizi & Dapur Umum", 
    "IPSRS (Pemeliharaan Sarana Mesin/Alat RS)", 
    "Manajemen Rekam Medis (Filing)",
    "Instalasi Laundry & Linen", 
    "CSSD (Sterilisasi Alat Medis)", 
    "Kamar Jenazah / Instalasi Forensik",
    "Manajemen Pegawai (HRD)",
    "Ruang IT / Server",
    "Customer Service & Pengaduan",
    "Area Parkir & Pos Keamanan (Satpam)",
    "Pengolahan Limbah Medis (Incinerator)"
]

events = [
    "Pasien datang untuk layanan rutin tanpa kendala (Happy Path berjalan lancar).",
    "Koneksi internet terputus secara tiba-tiba di pertengahan pelayanan (Sistem Offline).",
    "Terjadi lonjakan antrean mendadak yang membuat antarmuka sistem melambat (High Load/Timeout).",
    "Alat medis/pendukung elektronik di unit tersebut mengalami kerusakan mendadak.",
    "Pasien ternyata tidak membawa dokumen yang lengkap atau kartu asuransinya sudah tidak aktif.",
    "Terdapat kesalahan input data oleh petugas di sistem (Human Error / Typo).",
    "Pasien mengamuk dan komplain keras karena waktu tunggu atau biaya yang tidak sesuai ekspektasi.",
    "Dokter / Petugas penanggung jawab datang sangat terlambat atau mendadak berhalangan hadir.",
    "Stok barang / obat / reagen / BHP di depo terkait tiba-tiba menipis atau kosong sama sekali.",
    "Terjadi force majeure sesaat (Mati listrik total selama 10 menit, genset gagal menyala).",
    "Terjadi perubahan status penjaminan di tengah jalan (misal: masuk sebagai Umum, lalu keluarga membawa kartu BPJS setelah pasien dirawat).",
    "Sistem pihak ketiga menolak integrasi (Bridging Error ke V-Claim BPJS atau asuransi swasta).",
    "Ditemukan duplikasi data atau nomor rekam medis ganda di sistem ERP.",
    "Pasien menolak tindakan medis yang sudah dipesan di sistem setelah melihat estimasi biayanya.",
    "Terjadi kebocoran pipa air / insiden fisik di ruangan tersebut yang mengharuskan evakuasi operasional."
]

scenarios = []
seen = set()

# Menghasilkan tepat 2000 skenario unik
while len(scenarios) < 2000:
    fac = random.choice(facilities)
    pat = random.choice(patients)
    dep = random.choice(departments)
    evt = random.choice(events)
    
    sig = (fac, pat, dep, evt)
    if sig not in seen:
        seen.add(sig)
        
        desc = f"Di faskes **{fac}**, seorang **{pat}** berada pada proses pelayanan di area **{dep}**. Situasi memburuk atau berkembang ketika: **{evt}** Sistem ERP diuji bagaimana keluwesan dan ketahanannya dalam merekam dan menyolusi insiden operasional ini tanpa kehilangan integritas data."
        
        scenarios.append({
            "facility": fac,
            "patient": pat,
            "department": dep,
            "event": evt,
            "description": desc
        })

# Menyimpan ke dalam markdown file
with open("/home/gudang-data-kantor/simrs-web/docs/SCENARIO_DICTIONARY.md", "w", encoding="utf-8") as f:
    f.write("# Scenario Dictionary: 2000 Skenario Operasional Faskes\n\n")
    f.write("> Dokumen ini dihasilkan secara otomatis dan berisi tepat **2000 skenario** gabungan yang merepresentasikan keadaan operasional di lapangan. Fasilitas yang dicakup meliputi RS Umum, RS Swasta, Puskesmas (Kecamatan & Kelurahan), Klinik Umum, hingga Klinik Spesialis. Pasien mencakup Umum dan BPJS. Unit kerja mencakup Pendaftaran hingga unit penunjang terbawah seperti Laundry, Dapur, Keamanan, dan Pengolahan Limbah.\n\n")
    f.write("---\n\n")
    
    for i, scen in enumerate(scenarios, 1):
        f.write(f"### Skenario #{i}: {scen['department']} - {scen['facility']}\n")
        f.write(f"- **Kategori Faskes**: {scen['facility']}\n")
        f.write(f"- **Jenis Penjaminan**: {scen['patient']}\n")
        f.write(f"- **Unit Terkait**: {scen['department']}\n")
        f.write(f"- **Kondisi / Skenario**: {scen['description']}\n\n")

print("File docs/SCENARIO_DICTIONARY.md dengan 2000 skenario berhasil dibuat.")

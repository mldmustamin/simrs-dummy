Rawat Inap & Bangsal
=========================================
**Dokumen Arsitektur & Alur Kerja**

## 1. Deskripsi Eksekutif
Modul pengawasan 24/7. Mengelola CPPT (Catatan Terintegrasi), bed management, dan asuhan keperawatan rutin.

## 2. Aktor & Hak Akses
- Kepala Ruangan, Perawat Shift, Dokter Visite

## 3. Alur Perjalanan Pasien (Patient Journey)
1. Transfer in dari IGD/Poli. Orientasi ruangan oleh perawat.
2. Asesmen risiko jatuh dan nyeri.
3. Perawat shift Pagi/Siang/Malam melakukan operan (Handover SBAR).
4. Dokter DPJP melakukan Visite harian.
5. Pemberian obat injeksi/oral sesuai jadwal E-MAR.

## 4. Alur Perjalanan Sistem (ERP Data Lifecycle)
- Status bed berubah dinamis: `Kosong` -> `Ditempati` -> `Reserve Pulang`.
- Auto-Billing Midnight Census (00:00) menagih biaya sewa kamar otomatis.
- Validasi Barcode Gelang Pasien sebelum obat diberikan (E-MAR Lock).

## 5. Implementasi Multi-Model (Arsitektur Fallback)
- **Standar Ideal (Enterprise)**: Smart Ward: TTV langsung ditarik dari Patient Monitor ke sistem via IoT.
- **Skenario Pragmatis (Fallback)**: Kertas Lembar Observasi tetap dicetak sebagai backup, lalu di-input massal ke komputer (Double Input) untuk akreditasi.

## 6. Titik Integrasi & Bridging Eksternal
- SIRANAP Kemenkes (Sistem Informasi Rawat Inap).

## 7. Penanganan Bencana & Edge Cases
- ⚠️ **Skenario Ekstrem**: Code Blue (Henti Jantung). Alarm berbunyi, Response Time Tim Resusitasi dicatat otomatis oleh sistem.

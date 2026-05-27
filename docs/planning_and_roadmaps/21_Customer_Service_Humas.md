> **Status**: *On-going modul (Cetak Biru Masa Depan)*

Customer Service & Humas
=========================================
**Dokumen Arsitektur & Alur Kerja**

## 1. Deskripsi Eksekutif
Manajemen Front-End publik, portal keluhan, registrasi mandiri, dan informasi ketersediaan bed.

## 2. Aktor & Hak Akses
- CS / Humas

## 3. Alur Perjalanan Pasien (Patient Journey)
1. Pasien melakukan komplain di Web RS.
2. Masuk sebagai 'Ticket' di dashboard CS.
3. CS meresolve atau meneruskan ke unit terkait.

## 4. Alur Perjalanan Sistem (ERP Data Lifecycle)
- Dashboard sentral untuk memantau Kepuasan Pelanggan (Survey Bintang 5 di KiosK setelah pulang).
- Mekanisme Push Notification/SMS Broadcast ke pasien tentang promosi Poli Estetika.

## 5. Implementasi Multi-Model (Arsitektur Fallback)
- **Standar Ideal (Enterprise)**: Chatbot AI terintegrasi di Whatsapp Resmi RS yang mengambil jadwal dokter dari API ERP secara langsung.
- **Skenario Pragmatis (Fallback)**: Broadcast SMS biasa untuk daerah dengan internet lemah.

## 6. Titik Integrasi & Bridging Eksternal
- Whatsapp Gateway / SMS Gateway.

## 7. Penanganan Bencana & Edge Cases
- ⚠️ **Skenario Ekstrem**: Viralkan di Sosmed. Komplain berat (Kematian diduga Malpraktik) masuk ke tiket sistem dengan bendera MERAH, meng-SMS otomatis Direktur Utama.

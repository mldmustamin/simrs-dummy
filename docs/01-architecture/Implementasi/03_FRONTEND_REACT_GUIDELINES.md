# Panduan Arsitektur Frontend (React/Vite)
*Visi Utama: UI/UX canggih, responsif, dan *paperless* mutlak, dengan fitur Offline-Ready sebagai katup pengaman.*

## 1. Implementasi PWA & Offline Storage (Kapasitas Fallback)
Meskipun didesain untuk Cloud & Local Server bertenaga tinggi, Frontend tidak boleh menampilkan *White Screen of Death* saat LAN terputus sementara.
- **Standar Utama**: Operasi sinkron dan asinkron melalui Websocket/REST yang cepat.
- **Lapisan Pragmatis**: Gunakan Workbox dan `localForage` (IndexedDB) untuk menampung *request* sesaat jika aplikasi mendeteksi `navigator.onLine === false`. Begitu terkoneksi, lakukan sinkronisasi otomatis di latar belakang.

## 2. State Management & Optimistic UI
- Terapkan pola **Optimistic UI Updates** menggunakan React Query atau Zustand. Antarmuka harus menyajikan pengalaman *Enterprise* di mana aksi (simpan, klik, geser) bereaksi instan tanpa hambatan visual (*spinner*).
- Indikator status jaringan harus terlihat elegan di sudut layar (Online / Pending Sync).

## 3. Aksesibilitas: Keyboard-First & Touch-First
- UI/UX harus merespons interaksi *Tablet/Touchscreen* untuk dokter yang *visite* menggunakan iPad di bangsal VIP (Mode Ideal).
- Sekaligus mendukung navigasi ekstrem berbasis *Keyboard* (Tab, Enter, Alt+S) untuk petugas loket BPJS yang dituntut kecepatan tinggi tanpa memegang *mouse* (Mode Pragmatis).

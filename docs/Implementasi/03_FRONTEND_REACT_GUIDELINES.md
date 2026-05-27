# Panduan Arsitektur Frontend (React/Vite)
*Panduan teknis bagi AI Agent untuk membangun antarmuka UI/UX yang Offline-First.*

## 1. Implementasi PWA & Offline Storage
Frontend tidak boleh lumpuh (*White Screen of Death*) saat kabel LAN dicabut.
- **Service Workers**: Gunakan Workbox untuk melakukan *caching* semua aset statis (HTML, JS, CSS).
- **IndexedDB (Lokal Database)**: Gunakan library seperti `localForage` atau `Dexie.js` untuk menyimpan antrean *request* POST/PUT saat aplikasi mendeteksi `navigator.onLine === false`.

## 2. State Management & Optimistic UI
Sistem harus terasa secepat kilat (*snappy*) di mata dokter, tanpa loading *spinner* berlarut-larut.
- Terapkan pola **Optimistic UI Updates** menggunakan React Query atau Zustand. Ketika dokter menekan tombol "Simpan Resep", antarmuka langsung menampilkannya sebagai berhasil tersimpan, sementara *request* sinkronisasi terjadi diam-diam di *background*.
- Jika sinkronisasi gagal karena internet terputus, tambahkan ikon kecil ⚠️ (Pending Sync) di sebelah data tersebut, bukan memblokir layar dengan pesan *Error*.

## 3. Keyboard-First Navigation
Di faskes daerah, mouse sering lambat atau meja perawat terlalu sempit.
- Pastikan semua *form* pelayanan kritis (Kasir, Apotek, Pendaftaran) mendukung navigasi penuh menggunakan tombol `Tab`, `Enter`, dan *Shortcut* keyboard khusus (misal `Alt+S` untuk simpan) tanpa harus menggunakan *mouse*.

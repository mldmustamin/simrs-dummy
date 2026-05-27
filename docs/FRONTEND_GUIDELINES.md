# Frontend Development Guidelines (SIMRS Web)

Dokumen ini disusun berdasarkan analisis desain antarmuka (*mockup dashboard*) SIMRS Dummy. Panduan ini bertujuan untuk memastikan seluruh tim *frontend* membangun aplikasi yang konsisten, estetis, interaktif, dan tidak berantakan secara struktur kode maupun visual.

---

## 1. Visual & Design System (Aesthetics)
Berdasarkan *mockup*, UI SIMRS Web mengusung tema **Modern, Clean, dan Profesional** dengan dominasi ruang putih (*whitespace*) dan kartu (*card-based UI*).

*   **Palet Warna (Color Palette):**
    *   **Primary (Brand):** Hijau Medis / Emerald (seperti `#0f766e` atau `#006C4B`). Digunakan untuk Sidebar, tombol utama, dan teks penekanan.
    *   **Background:** Gunakan abu-abu sangat terang (`#f8fafc` atau `bg-slate-50`) untuk *background* utama aplikasi agar elemen *Card* yang berwarna putih (`#ffffff`) bisa menonjol.
    *   **Aksen & Kategori:** Gunakan warna pastel lembut untuk ikon dan *background badge* (Biru pucat, Hijau pucat, Ungu pucat).
*   **Tipografi:**
    *   Wajib menggunakan *font sans-serif* modern dan bersih seperti **Inter** atau **Roboto**.
    *   Gunakan hierarki visual yang kuat: Angka metrik (*Total Pasien*) sangat besar dan tebal, sedangkan teks deskripsi menggunakan warna abu-abu redup (`text-gray-500`).
*   **Bentuk & Bayangan (Shadows & Borders):**
    *   Sudut elemen membulat (*rounded corners*), gunakan `rounded-xl` atau `rounded-2xl` untuk *Card*.
    *   Gunakan bayangan lembut (`shadow-sm` secara *default*, dan `shadow-md` pada efek *hover*). Hindari garis batas (*border*) yang terlalu tebal atau gelap.

## 2. Standar Komponen (Component Architecture)
Jangan membuat elemen berulang dari nol. Buat dan gunakan ulang komponen standar yang terletak di `src/components/ui/`:

1.  **Card (Kartu):**
    *   Bungkus metrik, menu akses cepat, dan tabel ke dalam komponen `<Card>`.
    *   **Interaktivitas (Penting!):** Untuk kartu yang bisa diklik (seperti menu *Akses Cepat*), tambahkan *micro-animation* saat kursor diarahkan, misalnya efek sedikit terangkat (`hover:-translate-y-1 transition-transform`) atau pendaran bayangan (`hover:shadow-lg`), agar aplikasi terasa "hidup" dan responsif.
2.  **Status Badges:**
    *   Tabel antrean menampilkan status. Gunakan komponen `<Badge>`.
    *   Pola warna: `Menunggu` (Kuning/Orange pastel), `Diproses` (Biru pastel), `Selesai` (Hijau pastel). Gunakan kombinasi warna latar terang dan teks gelap senada (contoh Tailwind: `bg-yellow-100 text-yellow-800`).
3.  **Data Tables:**
    *   Tabel harus bersih tanpa garis vertikal. Gunakan garis horizontal tipis (`border-b border-gray-100`).
    *   Tambahkan efek *hover* pada baris tabel (`hover:bg-gray-50`) agar mata pengguna mudah menelusuri data pasien yang panjang.

## 3. Struktur Direktori React/Vite
Agar *codebase* tidak berantakan seiring bertambahnya modul (Kasir, Farmasi, Lab), ikuti konvensi folder berikut:
```text
simrs-frontend/src/
|-- assets/         # Gambar, logo, icon statis
|-- components/     
|   |-- ui/         # Komponen dasar yang bisa dipakai ulang (Button, Card, Badge, Modal)
|   |-- layout/     # Komponen tata letak (Sidebar, Header, MainContent)
|-- features/       # (Atau pages/) Pengelompokan berdasarkan Modul (Pendaftaran, Farmasi, Kasir)
|-- hooks/          # Custom React hooks (misal: useAuth, useFetch)
|-- lib/            # Konfigurasi library eksternal (Axios, utility class merging)
|-- utils/          # Fungsi pembantu murni (formatRupiah, formatDate)
|-- App.tsx
`-- main.tsx
```

## 4. Praktik Terbaik (Best Practices) Pengembangan
*   **Tailwind CSS Strictness:** Dilarang keras menggunakan *inline styles* (`style={{ color: 'red' }}`). Selalu gunakan kelas utilitas Tailwind.
*   **State Management:** Gunakan React Context atau Zustand untuk *state global* sederhana (seperti status *toggle* sidebar). Untuk *fetching* data API, sangat disarankan menggunakan **TanStack Query (React Query)** agar *caching* dan *loading state* tertangani rapi tanpa *callback hell* di `useEffect`.
*   **Skeleton Loaders:** Jangan menggunakan teks "Loading..." sederhana. Saat tabel atau metrik sedang memuat data dari *backend*, tampilkan animasi *skeleton* abu-abu (*pulse*) yang menyerupai bentuk data aslinya. Hal ini akan memunculkan sensasi aplikasi kelas premium.
*   **Responsivitas Penuh:** Gunakan Grid CSS/Tailwind (`grid-cols-1 md:grid-cols-2 lg:grid-cols-4`) agar *dashboard* tetap rapi dan bisa digulir ketika dibuka dari tablet atau layar beresolusi kecil di poliklinik.

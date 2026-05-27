# Agent Guide - SIMRS Web

Dokumen ini adalah titik masuk yang disarankan ketika kamu ingin melanjutkan
pekerjaan atau saat agent butuh arah kerja yang cepat dan konsisten.

Jika kamu ingin jalur paling singkat untuk navigasi AI, buka
[GATEWAY.md](GATEWAY.md) terlebih dahulu.

## Cara Pakai

- Kalau ingin melanjutkan pekerjaan, arahkan agent ke dokumen ini dulu.
- Kalau agent bingung harus mulai dari mana, baca bagian "Urutan Baca".
- Kalau ada bentrok antara dokumen lama dan status terbaru, utamakan bagian
  "Sumber Kebenaran".

## Sumber Kebenaran

1. [last_log.md](04-status/project_management_and_logs/last_log.md)
2. [RELEASE_NOTES.md](04-status/project_management_and_logs/RELEASE_NOTES.md)
3. [TASK_LIST.md](04-status/project_management_and_logs/TASK_LIST.md)
4. [BEST_PRACTICE_FIX_PLAN.md](02-operations/engineering_and_operations/BEST_PRACTICE_FIX_PLAN.md)
5. [DECISION_LOG.md](04-status/project_management_and_logs/DECISION_LOG.md)

## Urutan Baca

1. Baca [INDEX.md](INDEX.md) untuk peta dokumentasi.
2. Baca [last_log.md](04-status/project_management_and_logs/last_log.md)
   untuk progres terakhir.
3. Baca [BEST_PRACTICE_FIX_PLAN.md](02-operations/engineering_and_operations/BEST_PRACTICE_FIX_PLAN.md)
   untuk gap teknis yang masih terbuka.
4. Baca [TASK_LIST.md](04-status/project_management_and_logs/TASK_LIST.md)
   untuk status pekerjaan.
5. Baca dokumen roadmap yang relevan di [03-roadmaps/](03-roadmaps/).
6. Jika tugas menyentuh script Python generator, baca [master/README.md](../master/README.md).

## Aturan Navigasi

- Jangan jadikan README root sebagai sumber utama status implementasi.
- Dokumen roadmap menjelaskan arah, bukan selalu kondisi aktual.
- Dokumen arsip hanya untuk referensi historis.
- Kalau ada konflik, pilih dokumen status terbaru dan best-practice plan.

## Kapan Dipakai

- Saat user bilang `lanjut`, `lanjut dev`, `teruskan`, atau variasi sejenis.
- Saat agent perlu memutuskan langkah aman berikutnya.
- Saat kamu ingin memberi satu file acuan tanpa menjelaskan ulang konteks.

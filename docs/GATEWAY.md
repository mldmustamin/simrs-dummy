# AI Navigation Gateway - SIMRS Web

Dokumen ini adalah titik masuk paling singkat untuk AI agent yang perlu
menavigasi repo, mencari konteks, atau melanjutkan pekerjaan.

## Prioritas Bacaan

1. [AGENT_GUIDE.md](AGENT_GUIDE.md)
2. [INDEX.md](INDEX.md)
3. [04-status/project_management_and_logs/overview/last_log.md](04-status/project_management_and_logs/overview/last_log.md)
4. [02-operations/engineering_and_operations/BEST_PRACTICE_FIX_PLAN.md](02-operations/engineering_and_operations/BEST_PRACTICE_FIX_PLAN.md)
5. [04-status/project_management_and_logs/backlog/TASK_LIST.md](04-status/project_management_and_logs/backlog/TASK_LIST.md)
6. [04-status/project_management_and_logs/governance/DECISION_LOG.md](04-status/project_management_and_logs/governance/DECISION_LOG.md)
7. [master/README.md](../master/README.md)

## Aturan Navigasi

- Jika ada konflik antar dokumen, prioritaskan status terbaru dan rencana
  remediation.
- Dokumen roadmap menjelaskan arah, bukan selalu kondisi aktual.
- Dokumen arsip hanya referensi historis.
- Jangan pakai README root sebagai sumber utama status implementasi.

## Jalur Cepat Berdasarkan Kebutuhan

- Jika user bilang `lanjut`, baca `overview/last_log.md` lalu `backlog/TASK_LIST.md`.
- Jika user minta peta dokumentasi, baca `INDEX.md`.
- Jika user minta status yang paling dapat dipercaya, baca `overview/last_log.md`,
  `governance/RELEASE_NOTES.md`, lalu `BEST_PRACTICE_FIX_PLAN.md`.
- Jika user menyentuh generator Python, baca `master/README.md`.
- Jika user minta analisis desain atau risiko, baca `BEST_PRACTICE_FIX_PLAN.md`
  lalu `RISK_REGISTER.md`.

## Kapan Dipakai

- Saat agent butuh arah kerja dari nol.
- Saat user hanya bilang `lanjut` atau `teruskan`.
- Saat ada bentrok antara roadmap, status, dan keputusan teknis.
- Saat perlu titik masuk yang ringkas dan konsisten untuk AI.

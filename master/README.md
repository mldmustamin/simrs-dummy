# Master Scripts

Folder ini menampung script Python yang sebelumnya tercecer di root proyek.
Strukturnya dibagi berdasarkan fungsi agar lebih mudah dirawat.

## Struktur

- `docs/`
  - script untuk generate atau update dokumen Markdown
- `workflows/`
  - script untuk generate, merge, expand, dan memperbaiki workflow dokumen
- `scenarios/`
  - script untuk generate skenario operasional

## Daftar Singkat

### docs/
- `generate_implementasi_docs.py`
- `update_implementasi_docs.py`

### workflows/
- `expand_alur.py`
- `expand_bangsal.py`
- `fix_workflows.py`
- `generate_workflows.py`
- `generate_other_workflows.py`
- `generate_rich_workflows.py`
- `merge_workflows.py`
- `write_workflows.py`
- `write_workflows_strict.py`

### scenarios/
- `generate_scenarios.py`

## Catatan

Script di sini tetap memakai path absolut atau path repo yang sudah ada.
Kalau nanti ingin dijalankan dari lokasi baru, cek dulu hardcoded path di
masing-masing file.

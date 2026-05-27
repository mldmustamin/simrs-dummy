import os
import glob

folder_path = "/home/gudang-data-kantor/simrs-web/docs/Workflows"
master_file_path = "/home/gudang-data-kantor/simrs-web/docs/Workflows/MASTER_WORKFLOW_ALL_MODULES.md"

# Get all markdown files except the master file
md_files = sorted([f for f in glob.glob(os.path.join(folder_path, "*.md")) if "MASTER_WORKFLOW" not in f])

with open(master_file_path, "w", encoding="utf-8") as master_file:
    master_file.write("# MASTER WORKFLOW: Seluruh Modul ERP\n")
    master_file.write("> **Tujuan**: Dokumen gabungan dari ke-22 modul utama dan pendukung rumah sakit untuk mempermudah pembacaan secara menyeluruh (Buku Besar Workflow).\n\n")
    
    for file_path in md_files:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            master_file.write(content)
            master_file.write("\n\n---\n\n")

# Delete the individual files to prevent clutter
for file_path in md_files:
    os.remove(file_path)

print(f"Berhasil menggabungkan {len(md_files)} file menjadi satu di {master_file_path} dan menghapus file pecahan.")

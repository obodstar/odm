import os
import shutil

# nama folder output
OUTPUT_DIR = "output"

# pastikan folder output ada
if not os.path.isdir(OUTPUT_DIR):
    print(f"❌ Folder '{OUTPUT_DIR}' tidak ditemukan")
else:
    for item in os.listdir(OUTPUT_DIR):
        item_path = os.path.join(OUTPUT_DIR, item)

        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.unlink(item_path)  # hapus file
                print(f"🗑️ File dihapus: {item_path}")

            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)  # hapus folder
                print(f"🗑️ Folder dihapus: {item_path}")

        except Exception as e:
            print(f"⚠️ Gagal menghapus {item_path}: {e}")

    print("✅ Semua isi folder output berhasil dihapus")

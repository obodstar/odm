import os, sys
import random
from PIL import Image, ImageDraw, ImageFont
# max_width
# === Clear terminal ===
if "win" in sys.platform.lower():
    os.system("cls")
else:
    os.system("clear")

# === Pengaturan awal ===
template_folder = "template"
font_folder = "fontlist"
fontlist_file = "fontlist.txt"
teks_file = "teks.txt"
output_folder = "output"

pembuat = "Script Buat Desain Massal | Created By Obod AF"
print(pembuat)

# === Input ukuran font ===
try:
    font_size = int(input("Masukkan ukuran font (misal: 48): ") or 48)
except ValueError:
    font_size = 48

text_color = (0, 0, 0)

# === Pastikan folder ada ===
os.makedirs(output_folder, exist_ok=True)
os.makedirs(font_folder, exist_ok=True)
os.makedirs(template_folder, exist_ok=True)

# === DETEKSI TEMPLATE ===
templates = [
    f for f in os.listdir(template_folder)
    if f.lower().endswith((".png", ".jpg", ".jpeg"))
]

if not templates:
    print("❌ Tidak ada template ditemukan di folder 'template'")
    print("➡️  Masukkan file gambar template terlebih dahulu.")
    exit()

# === MENU PILIH TEMPLATE ===
print("\n📂 Daftar Template:")
for i, t in enumerate(templates, start=1):
    print(f"{i}. {t}")

try:
    pilihan = int(input("\nPilih nomor template yang ingin digunakan: "))
    if pilihan < 1 or pilihan > len(templates):
        raise ValueError
except ValueError:
    print("❌ Pilihan tidak valid.")
    exit()

# === NAMA TEMPLATE TANPA EXTENSION ===
template_name = os.path.splitext(templates[pilihan - 1])[0]

# === PATH TEMPLATE ===
template_path = os.path.join(template_folder, templates[pilihan - 1])


# === FOLDER OUTPUT SESUAI TEMPLATE ===
template_output_folder = os.path.join(output_folder, template_name)
os.makedirs(template_output_folder, exist_ok=True)

# === Buat teks.txt jika belum ada ===
if not os.path.exists(teks_file):
    with open(teks_file, "w", encoding="utf-8") as f:
        f.write("Contoh teks pertama.\nContoh teks kedua.")
    print("✅ teks.txt dibuat otomatis, silakan isi teks Anda.")
    exit()

# === Baca teks ===
with open(teks_file, "r", encoding="utf-8") as f:
    teks_list = [t.strip() for t in f.readlines() if t.strip()]

if not teks_list:
    print("⚠️  teks.txt kosong!")
    exit()

# === Buat fontlist otomatis jika belum ada ===
if not os.path.exists(fontlist_file):
    fonts = [
        os.path.join(font_folder, f)
        for f in os.listdir(font_folder)
        if f.lower().endswith(".ttf")
    ]
    with open(fontlist_file, "w", encoding="utf-8") as f:
        for font in fonts:
            f.write(font + "\n")
    print(f"✅ fontlist.txt dibuat otomatis ({len(fonts)} font).")

# === Baca fontlist ===
with open(fontlist_file, "r", encoding="utf-8") as f:
    fonts_list = [l.strip() for l in f if l.strip()]

if not fonts_list:
    print("❌ Tidak ada font ditemukan!")
    exit()

# === FUNGSI DESAIN ===
def buat_desain(teks, index):
    img = Image.open(template_path).convert("RGBA")
    width, height = img.size

    font_path = random.choice(fonts_list)
    try:
        font = ImageFont.truetype(font_path, font_size)
    except OSError:
        print(f"⚠️ Font gagal dibuka: {font_path}")
        return

    print(f"🎨 Font: {os.path.basename(font_path)}")

    layer = Image.new("RGBA", img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(layer)

    max_width = int(width * 0.7)
    words = teks.split()
    lines, line = [], ""

    for word in words:
        test = line + word + " "
        w = draw.textbbox((0, 0), test, font=font)[2]
        if w <= max_width:
            line = test
        else:
            lines.append(line)
            line = word + " "
    lines.append(line)

    total_height = sum(
        draw.textbbox((0, 0), l, font=font)[3]
        for l in lines
    )

    y = (height - total_height) // 2

    for l in lines:
        bbox = draw.textbbox((0, 0), l, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        x = (width - w) // 2
        draw.text((x, y), l, font=font, fill=text_color)
        y += h

    result = Image.alpha_composite(img, layer)
    # === WAJIB: HILANGKAN ALPHA UNTUK JPG ===
    result = result.convert("RGB")

    output_name = f"{template_name}{index+1:04d}.jpg"
    output_path = os.path.join(template_output_folder, output_name)


    result.save(output_path, "JPEG", quality=95, subsampling=0)
    print(f"✅ Selesai: {output_name}")


# === LOOP ===
for i, teks in enumerate(teks_list):
    buat_desain(teks, i)

print("\n🎉 Semua desain berhasil dibuat!")



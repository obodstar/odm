import os
import random
from PIL import Image, ImageDraw, ImageFont

# === Pengaturan awal ===
template_path = "template.png"
font_folder = "fontlist"
fontlist_file = "fontlist.txt"
quotes_file = "quotes.txt"
output_folder = "output"

pembuat = "Script Buat Desain Massal | Created By Obod AF"
            
print(pembuat)

# === Input ukuran font dari pengguna ===
try:
    font_size = int(input("Masukkan ukuran font (misal: 48): ") or 48)
except ValueError:
    font_size = 48

# Warna teks default hitam
text_color = (0, 0, 0)

# === Pastikan folder dan file penting ada ===
os.makedirs(output_folder, exist_ok=True)
os.makedirs(font_folder, exist_ok=True)

# === Buat template putih jika belum ada ===
if not os.path.exists(template_path):
    img = Image.new("RGBA", (1080, 1080), (255, 255, 255, 255))
    img.save(template_path)
    print("✅ template.png otomatis dibuat (putih polos).")

# === Buat file quotes.txt jika belum ada ===
if not os.path.exists(quotes_file):
    with open(quotes_file, "w", encoding="utf-8") as f:
        f.write("Contoh quote pertama.\nContoh quote kedua.")
    print("✅ quotes.txt otomatis dibuat, silakan isi dengan teks quotes Anda.")
    exit()

# === Baca semua quotes dari file ===
with open(quotes_file, "r", encoding="utf-8") as f:
    quotes = [q.strip() for q in f.readlines() if q.strip()]

if not quotes:
    print("⚠️  File quotes.txt kosong! Silakan isi beberapa quotes dulu.")
    exit()

# === Cek daftar font ===
# Jika fontlist.txt belum ada, buat otomatis berdasarkan isi folder fontlist
if not os.path.exists(fontlist_file):
    all_fonts = [os.path.join(font_folder, f) for f in os.listdir(font_folder) if f.lower().endswith(".ttf")]
    with open(fontlist_file, "w", encoding="utf-8") as f:
        for font_path in all_fonts:
            f.write(font_path + "\n")
    print(f"✅ fontlist.txt dibuat otomatis dengan {len(all_fonts)} font dari folder '{font_folder}'.")

# Baca daftar font dari fontlist.txt
with open(fontlist_file, "r", encoding="utf-8") as f:
    fonts_list = [line.strip() for line in f.readlines() if line.strip()]

if not fonts_list:
    print("❌ Tidak ada font ditemukan! Pastikan file .ttf ada di folder 'fontlist'.")
    exit()

# === Fungsi utama ===
def buat_desain(teks, index):
    img = Image.open(template_path).convert("RGBA")
    width, height = img.size

    # Pilih font acak
    font_path = random.choice(fonts_list)
    try:
        full_font_path = os.path.abspath(os.path.join(os.getcwd(), font_path))
        font = ImageFont.truetype(full_font_path, font_size)
    except OSError:
        print(f"⚠️  Font gagal dibuka: {font_path}")
        return

    print(f"🎨 Menggunakan font: {os.path.basename(font_path)}")

    txt_layer = Image.new("RGBA", img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt_layer)

    # Bungkus teks agar tidak melewati lebar gambar
    max_width = int(width * 0.8)
    lines, line = [], ""
    words = teks.split(" ")

    for word in words:
        test_line = line + word + " "
        bbox = draw.textbbox((0, 0), test_line, font=font)
        w = bbox[2] - bbox[0]
        if w <= max_width:
            line = test_line
        else:
            lines.append(line)
            line = word + " "
    lines.append(line)

    # Hitung tinggi total teks
    text_height = sum(
        draw.textbbox((0, 0), l, font=font)[3] - draw.textbbox((0, 0), l, font=font)[1]
        for l in lines
    )
    y_start = (height - text_height) // 2

    # Gambar teks di tengah gambar
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        x = (width - w) // 2
        draw.text((x, y_start), line, font=font, fill=text_color)
        y_start += h

    hasil = Image.alpha_composite(img, txt_layer)

    # Simpan hasil
    random_num = random.randint(1000, 9999)
    output_path = os.path.join(output_folder, f"quotes_{random_num}.png")
    hasil.save(output_path)
    print(f"✅ Selesai: {output_path}")

# === Jalankan looping ===
for i, quote in enumerate(quotes):
    buat_desain(quote, i)

print("\n🎉 Semua desain berhasil dibuat di folder 'output'!")

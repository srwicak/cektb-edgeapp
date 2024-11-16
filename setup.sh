#!/bin/bash

echo "--== INSTALASI CEKTB - EDGE APPLICATION ==-"

# Cek apakah Python dan PIP sudah tersedia
if ! command -v python3 &> /dev/null
then
  echo "Python3 tidak ditemukan. Harap menginstal Python3 terlebih dahulu."
  exit 1
fi

if ! command -v pip3 &> /dev/null
then
  echo "Pip3 tidak ditemukan. Harap menginstal Pip3 terlebih dahulu."
  exit 1
fi

# Buat virtual environment
echo "Menyiapkan virtual environment..."
python3 -m venv venv

# Aktifkan virtual environment
echo "Mengaktifkan virtual environment..."
source venv/bin/activate

# Install dependensi
echo "Memasang dependensi aplikasi..."
pip3 install --upgrade pip
pip3 install -r backend/requirements.txt

# Buat folder data jika belum ada
mkdir -p data
touch data/local_data.json
touch data/credentials.json

# Tambahkan data dummy awal
echo '{"password_hash": ""}' > data/credentials.json
echo '{"data": []}' > data/local_data.json

# Buat shortcut di desktop (Linux)
DESKTOP_SHORTCUT="$HOME/Desktop/EdgeApp.desktop"

echo "Creating desktop shortcut..."

cat <<EOL > "$DESKTOP_SHORTCUT"
[Desktop Entry]
Name=CekTB-App
Comment=Edge Application CekTB
Exec=$(pwd)/start_app.sh
Type=Application
Terminal=true
Icon=utilities-terminal
EOL

chmod +x "$DESKTOP_SHORTCUT"

chmod +x start_app.sh

echo "=== Instalasi selesai! ==="
echo "Jalankan './start_app.sh' untuk memulai aplikasi atau menekan shortcut CekTB-App yang ada di dekstop."
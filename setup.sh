#!/bin/bash

echo "    ===================================="
echo "--== INSTALASI CEKTB - EDGE APPLICATION ==--"
echo "    ===================================="
echo

# Cek Python3
if ! command -v python3 &> /dev/null; then
  echo "Python3 tidak ditemukan. Harap menginstal Python3 terlebih dahulu."
  exit 1
fi

# Cek Pip3
if ! command -v pip3 &> /dev/null; then
  echo "Pip3 tidak ditemukan. Harap menginstal Pip3 terlebih dahulu."
  exit 1
fi

# Buat virtual environment
if [ -d "venv" ]; then
  echo "Virtual environment sudah ada, melewati pembuatan..."
else
  echo "Membuat virtual environment..."
  python3 -m venv venv
fi

# Aktifkan virtual environment
echo -e "Mengaktifkan virtual environment...\n"
source venv/bin/activate

# Install dependensi
echo -e "Memasang dependensi aplikasi...\n"
pip3 install --upgrade pip
pip3 install -r backend/requirements.txt

# Buat folder data
mkdir -p data logs
touch data/local_data.json
touch data/credentials.json

# Tambahkan data dummy awal
echo '{"data": []}' > data/local_data.json

# Kunci dua arah untuk sinkronasi data
echo '{"device_key": ""}' > data/device_key.json

# Prompt password
echo
echo "=========================================="
echo "Silakan buat password untuk aplikasi ini:"
echo "=========================================="
read -s -p "Password: " APP_PASSWORD
echo
read -s -p "Konfirmasi Password: " APP_PASSWORD_CONFIRM
echo
echo "=========================================="

if [ "$APP_PASSWORD" != "$APP_PASSWORD_CONFIRM" ]; then
  echo -e "\nPassword tidak cocok! Silakan ulangi instalasi."
  exit 1
fi

PASSWORD_HASH=$(echo -n "$APP_PASSWORD" | sha256sum | awk '{print $1}')
echo "{\"password_hash\": \"$PASSWORD_HASH\"}" > data/credentials.json
echo -e "\nPassword berhasil disimpan.\n"

# Buat start_app.sh
START_APP_SCRIPT="start_app.sh"
echo -e "Membuat start_app.sh...\n"

cat <<EOL > "$START_APP_SCRIPT"
#!/bin/bash

echo -e "Memulai Aplikasi CekTB-EdgeApp...\n"

# Navigasi ke direktori script
SCRIPT_DIR=\$(dirname "\$(realpath "\$0")")
cd "\$SCRIPT_DIR"

# Aktifkan virtual environment
if [ ! -d "venv" ]; then
  echo "Virtual environment tidak ditemukan! Harap jalankan 'setup.sh' terlebih dahulu."
  exit 1
fi

echo -e "Mengaktifkan virtual environment...\n"
source venv/bin/activate

# Validasi file utama
if [ ! -f "backend/main.py" ]; then
  echo "File backend/main.py tidak ditemukan. Pastikan file ada di lokasi yang benar."
  exit 1
fi

# Verifikasi password
read -s -p "Masukkan Password Aplikasi: " INPUT_PASSWORD
echo
STORED_HASH=\$(jq -r '.password_hash' data/credentials.json)
INPUT_HASH=\$(echo -n "\$INPUT_PASSWORD" | sha256sum | awk '{print \$1}')

if [ "\$INPUT_HASH" != "\$STORED_HASH" ]; then
  echo "Password salah! Aplikasi tidak dapat dijalankan."
  exit 1
fi

# Jalankan server
LOGFILE="logs/server.log"
echo "Log server disimpan di \$LOGFILE"
fastapi run backend/main.py --host 0.0.0.0 --port 8000 > "\$LOGFILE" 2>&1 &

# Tunggu server
sleep 5

# Buka browser
xdg-open http://localhost:8000

echo -e "Aplikasi CekTB sedang berjalan. Anda dapat menutup terminal ini jika server sedang berjalan.\n"
EOL

chmod +x "$START_APP_SCRIPT"

# Buat shortcut desktop
DESKTOP_SHORTCUT="$HOME/Desktop/CekTB-EdgeApp.desktop"
if [ ! -f "$DESKTOP_SHORTCUT" ]; then
  echo -e "Membuat shortcut desktop...\n"
  cat <<EOL > "$DESKTOP_SHORTCUT"
[Desktop Entry]
Name=CekTB-EdgeApp
Comment=Edge Application CekTB
Exec=$(pwd)/start_app.sh
Type=Application
Terminal=true
Icon=utilities-terminal
EOL
  chmod +x "$DESKTOP_SHORTCUT"
else
  echo -e "Shortcut desktop sudah ada.\n"
fi

# Prompt untuk menunggu user menekan Enter
echo -e "=== Instalasi selesai! === \n"
echo -e "Jalankan './start_app.sh' untuk memulai aplikasi atau gunakan shortcut CekTB-App di desktop.\n"
echo "Tekan Enter untuk menutup terminal."
read -r

#!/bin/bash

echo "Memulai Aplikasi CekTB-EdgeApp..."

# Aktifkan virtual environment
echo "Mengaktifkan virtual environment..."
source venv/bin/activate

# Jalankan server FastAPI
echo "Memulai server..."
fastapi run main.py &

# Tunggu server siap
sleep 5

# Buka aplikasi di browser default
xdg-open http://localhost:8000

echo "Aplikasi CekTB sedang berjalan. Anda dapat menutup terminal ini jika server sedang berjalan."

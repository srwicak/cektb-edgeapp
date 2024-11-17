import httpx
import json
from pathlib import Path

async def get_device_key():
    """Fungsi untuk membaca device_key dari file JSON."""
    try:
        file_path = Path("../data/device_key.json")  # Path ke file JSON
        with file_path.open("r") as file:
            data = json.load(file)
            return data.get("device_key")  # Ambil nilai device_key
    except FileNotFoundError:
        raise ValueError("File device_key.json tidak ditemukan.")
    except json.JSONDecodeError:
        raise ValueError("File device_key.json tidak valid.")

async def send_data_to_server(name: str, bpjs: str, prediction: str, confidence: float):
    """Fungsi untuk mengirimkan data ke server eksternal."""
    device_key = await get_device_key()  # Ambil device_key dari file JSON

    if not device_key:
        raise ValueError("device_key tidak ditemukan di file JSON.")

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "http://your-server-endpoint.com/api/data",  # Ganti dengan endpoint yang sesuai
                json={
                    "device_key": device_key,
                    "name": name,
                    "bpjs": bpjs,
                    "prediction": prediction,
                    "confidence": confidence,
                }
            )
            return response.json()
        except Exception as e:
            raise ValueError(f"Error mengirim data ke server eksternal: {str(e)}")


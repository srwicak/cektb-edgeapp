import httpx

async def send_data_to_server(name: str, bpjs: str, prediction: str, confidence: float):
    """Fungsi untuk mengirimkan data ke server eksternal."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "http://your-server-endpoint.com/api/data",  # Ganti dengan endpoint yang sesuai
                json={
                    "name": name,
                    "bpjs": bpjs,
                    "prediction": prediction,
                    "confidence": confidence
                }
            )
            return response.json()
        except Exception as e:
            raise ValueError(f"Error mengirim data ke server eksternal: {str(e)}")

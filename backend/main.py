from fastapi import FastAPI, File, Form, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse, HTMLResponse
from predict import predict
from utils import send_data_to_server
from pathlib import Path
import time

app = FastAPI()

# Fungsi membaca UI HTML
@app.get("/", response_class=HTMLResponse)
async def get_ui():
    with open("frontend/index.html", "r") as f:
        return f.read()


@app.post("/predict")
async def predict_endpoint(
    name: str = Form(...),  
    bpjs: str = Form(...),
    file: UploadFile = File(...),
):
    try:
        # Periksa format file
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File harus berupa gambar")

        # Baca file gambar
        image_bytes = await file.read()

        # Lakukan prediksi
        start_time = time.time()
        prediction, confidence = predict(image_bytes)
        end_time = time.time()

        # Kirim data ke server eksternal
        #await send_data_to_server(name, bpjs, prediction, confidence)

        # Kembalikan hasil prediksi
        return JSONResponse(content={
            "prediction": prediction,
            "confidence": confidence,
            "inference_time": round(end_time - start_time, 4)  # Waktu inferensi dalam detik
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error dalam memproses gambar: {str(e)}")

# # Endpoint sinkronisasi data ke server
# @app.post("/sync-data")
# async def sync_data(username: str, password: str):
#     # Autentikasi ke server
#     server_token = authenticate_server(username, password)
#     if not server_token:
#         raise HTTPException(status_code=401, detail="Invalid server credentials")
    
#     # Kirim data lokal ke server
#     if not DATA_PATH.exists():
#         return {"message": "No data to sync"}
#     with open(DATA_PATH, "r") as f:
#         local_data = json.load(f)
#     # Simulasi sinkronisasi
#     return {"message": "Data synced successfully", "synced_data": local_data}


# # Endpoint cek dan download model terbaru
# @app.post("/update-model")
# async def update_model():
#     latest_version = check_model_version()
#     if not latest_version:
#         raise HTTPException(status_code=500, detail="Failed to fetch model version")
#     success = download_model(latest_version, MODEL_PATH)
#     if success:
#         return {"message": "Model updated successfully"}
#     raise HTTPException(status_code=500, detail="Failed to download model")

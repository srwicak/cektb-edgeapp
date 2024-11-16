import tflite_runtime.interpreter as tflite
import numpy as np
from PIL import Image
import io

# Muat model TensorFlow Lite
interpreter = tflite.Interpreter(model_path="data/tb_detection_v1.tflite")
interpreter.allocate_tensors()

# Mendapatkan informasi input dan output
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

def predict(image_bytes: bytes):
    """Melakukan prediksi dengan model TensorFlow Lite."""
    try:
        # Baca gambar dan konversi ke grayscale
        image = Image.open(io.BytesIO(image_bytes)).convert("L")
        image_resized = image.resize((224, 224))
        image_array = np.array(image_resized).astype(np.float32)

        # Normalisasi dan tambahkan dimensi batch dan channel
        image_normalized = image_array / 255.0
        image_normalized = np.expand_dims(image_normalized, axis=-1)  # Channel untuk grayscale
        image_normalized = np.expand_dims(image_normalized, axis=0)   # Batch size

        # Jalankan model untuk inferensi
        interpreter.set_tensor(input_details[0]['index'], image_normalized)
        interpreter.invoke()

        # Dapatkan hasil prediksi
        output = interpreter.get_tensor(output_details[0]['index'])
        confidence = float(output[0][0])  # Probabilitas untuk "Ada TB"

        prediction = "Ada TB" if confidence > 0.5 else "Tidak Ada TB"
        return prediction, confidence

    except Exception as e:
        raise ValueError(f"Error dalam memproses gambar: {str(e)}")

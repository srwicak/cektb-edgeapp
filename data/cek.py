from tflite_runtime.interpreter import Interpreter

# Path ke model TFLite Anda
model_path = "tb_detection_model.tflite"

# Load model menggunakan tflite-runtime
interpreter = Interpreter(model_path=model_path)

# Alokasikan tensor
interpreter.allocate_tensors()

# Mendapatkan detail input dan output
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Cetak informasi input
print("Input Details:")
for detail in input_details:
    print(f"Name: {detail['name']}")
    print(f"Shape: {detail['shape']}")
    print(f"Type: {detail['dtype']}")
    print()

# Cetak informasi output
print("Output Details:")
for detail in output_details:
    print(f"Name: {detail['name']}")
    print(f"Shape: {detail['shape']}")
    print(f"Type: {detail['dtype']}")
    print()

# Jalankan inferensi menggunakan input dummy
import numpy as np

# Buat input data dummy sesuai dengan bentuk input model
input_data = np.random.random_sample(input_details[0]['shape']).astype(input_details[0]['dtype'])
interpreter.set_tensor(input_details[0]['index'], input_data)

# Jalankan model
interpreter.invoke()

# Ambil output
output_data = interpreter.get_tensor(output_details[0]['index'])
print("Output dari Model:")
print(output_data)

import streamlit as st
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from PIL import Image
import tempfile, base64, os, json
import gdown
import h5py
from datetime import datetime
from dotenv import load_dotenv

# ----------------------------
# 🌍 Load environment variables
# ----------------------------
load_dotenv()
MODEL_DIR = "models"
MODEL_NAME = "eye_disease_model.h5"
MODEL_PATH = os.path.join(MODEL_DIR, MODEL_NAME)

DRIVE_FILE_ID = os.getenv("DRIVE_FILE_ID")
FIREBASE_DB_URL = os.getenv("FIREBASE_DB_URL")
firebase_json_str = os.getenv("FIREBASE_SERVICE_ACCOUNT")

# ----------------------------
# 🔑 Firebase Initialization
# ----------------------------
import firebase_admin
from firebase_admin import credentials, db

if firebase_json_str:
    try:
        firebase_info = json.loads(firebase_json_str)
        cred = credentials.Certificate(firebase_info)
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred, {'databaseURL': FIREBASE_DB_URL})
    except Exception as e:
        st.error(f"Firebase initialization failed: {e}")
else:
    st.warning("⚠️ Firebase credentials not found. Database logging disabled.")

# ----------------------------
# ⬇️ Download Model if missing
# ----------------------------
os.makedirs(MODEL_DIR, exist_ok=True)
if not os.path.exists(MODEL_PATH) and DRIVE_FILE_ID:
    url = f"https://drive.google.com/uc?id={DRIVE_FILE_ID}"
    with st.spinner("📥 Downloading model... please wait ⏳"):
        gdown.download(url, MODEL_PATH, quiet=False)

# ----------------------------
# 📌 Load Model (Cached)
# ----------------------------
@st.cache_resource
def load_model_cached(path):
    if not os.path.exists(path):
        st.error("❌ Model file not found. Please check DRIVE_FILE_ID or place model in /models/")
        st.stop()
    if not h5py.is_hdf5(path):
        st.error("❌ The model file is not a valid HDF5 file.")
        st.stop()
    return load_model(path)

model = load_model_cached(MODEL_PATH)
input_shape = model.input_shape[1:3]

# ----------------------------
# 🎯 Streamlit App UI
# ----------------------------
st.title("👁️ SMART AI-Driven Ophthalmic Disease Detector")
class_names = ['Cataract', 'Diabetic Retinopathy', 'Glaucoma', 'Normal']

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    img = Image.open(uploaded_file).convert("RGB")
    st.image(img, caption="Uploaded Image", use_container_width=True)

    # Preprocess
    img_resized = img.resize(input_shape)
    img_array = image.img_to_array(img_resized)
    img_array = np.expand_dims(img_array, axis=0) / 255.0

    # Prediction
    with st.spinner("Predicting..."):
        preds = model.predict(img_array)
    predicted_index = np.argmax(preds, axis=1)[0]
    predicted_class = class_names[predicted_index]
    confidence = np.max(preds) * 100

    # Display
    st.markdown(f"### 🩺 Prediction: **{predicted_class}**")
    st.markdown(f"### 📊 Confidence: **{confidence:.2f}%**")
    import pandas as pd
    st.bar_chart(pd.DataFrame(preds[0].reshape(1, -1), columns=class_names))

    # Convert Image to Base64
    buffer = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
    img.save(buffer.name, format="JPEG")
    with open(buffer.name, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode('utf-8')

    # Store in Firebase
    if firebase_json_str:
        try:
            ref = db.reference("detections")
            data = {
                "disease": predicted_class,
                "confidence": round(confidence, 2),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "image_base64": img_base64
            }
            ref.push(data)
            st.success("✅ Detection saved to Firebase Realtime Database!")
        except Exception as e:
            st.error(f"Failed to save to Firebase: {e}")
    else:
        st.warning("⚠️ Firebase not configured. Prediction not saved.")

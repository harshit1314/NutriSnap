# main.py

import cv2
import numpy as np
import requests
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
import io # Used to handle byte streams

# --- Configuration ---
# This is where we define constants for our application
MODEL_PATH = 'best.pt'                          # Path to your trained model file
CREDIT_CARD_REAL_WIDTH_CM = 8.56                # Standard credit card width in cm
# Sign up here for a free key: https://fdc.nal.usda.gov/api-key-signup.html
# Using a DEMO_KEY is fine for testing but it has very low limits.
USDA_API_KEY = 'DEMO_KEY'
USDA_API_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"

# --- Initialize FastAPI App and Load the AI Model ---
# This part of the code runs only ONCE when the server starts.
app = FastAPI(title="NutriSnap API")
model = YOLO(MODEL_PATH)
print("AI Model loaded successfully.")

# --- CORS Middleware ---
# This is a security feature that browsers enforce. It tells the browser
# that it's okay for our frontend (running on a different address)
# to request data from our backend.
origins = [
    "http://localhost:5173",    # Default address for a Vite React app
    "http://127.0.0.1:5173",
     "http://localhost:3000",    # Add this line for create-react-app
    "http://127.0.0.1:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],        # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],        # Allow all headers
)

# --- API Endpoint Definition ---
# This defines the main URL for our analysis.
# The server will listen for POST requests at http://.../analyze-meal/
@app.post("/analyze-meal/")
async def analyze_meal(image_file: UploadFile = File(...)):
    """
    This endpoint receives an image, analyzes it using the YOLOv8 model,
    and returns the detected food items with their estimated weights.
    """
    # Read the image file uploaded by the user into memory
    image_bytes = await image_file.read()
    
    # Convert the bytes into a NumPy array that OpenCV can understand
    np_array = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

    # --- Run the AI Model ---
    # The model processes the image and finds all objects.
    results = model(img)
    annotated_img = results[0].plot() 
    cv2.imwrite("debug_output.jpg", annotated_img)
    detections = results[0].boxes.data.cpu().numpy()  # Get box data [x1, y1, x2, y2, confidence, class_id]
    class_names = results[0].names                  # Get the names of the classes (e.g., 'egg', 'reference_object')

    # --- Analysis Logic ---
    pixels_per_cm = None
    reference_box = None

    # First, loop through all detections to find the reference object
    for det in detections:
        class_id = int(det[5])
        if class_names[class_id] == 'reference_object':
            x1, y1, x2, y2 = det[:4]
            pixel_width = x2 - x1
            pixels_per_cm = pixel_width / CREDIT_CARD_REAL_WIDTH_CM
            reference_box = det # Store the reference box to ignore it later
            print(f"Reference object found. Pixels per cm: {pixels_per_cm}")
            break

    if pixels_per_cm is None:
        return {"error": "Reference object not detected. Please include a credit card in the photo."}

    # Second, loop through detections again to find and analyze food items
    food_items = []
    for det in detections:
        class_id = int(det[5])
        class_name = class_names[class_id]
        
        # Skip the reference object itself in this loop
        if class_name == 'reference_object':
            continue

        # Get bounding box coordinates
        x1, y1, x2, y2 = det[:4]
        
        # Estimate size
        pixel_area = (x2 - x1) * (y2 - y1)
        real_area_cm2 = pixel_area / (pixels_per_cm ** 2)
        
        # This is a VERY simplified estimation. A huge area for improvement!
        # Assumption: Average food height is 2cm, average density is 1g/cm^3
        estimated_volume_cm3 = real_area_cm2 * 2 
        estimated_grams = estimated_volume_cm3 * 1

        food_items.append({
            "name": class_name,
            "estimated_grams": round(estimated_grams, 2),
            "confidence": round(float(det[4]), 2) # Include the model's confidence
        })
        print(f"Detected: {class_name} | Estimated weight: {estimated_grams:.2f}g")

    return {"detected_foods": food_items}

# --- A simple root endpoint to check if the server is running ---
@app.get("/")
def read_root():
    return {"status": "NutriSnap API is running."}
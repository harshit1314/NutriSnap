
# NutriSnap 🥗📸

A web application that combines computer vision and generative AI to identify food from an image and provide its detailed nutritional information. Simply snap a picture of your meal, and let NutriSnap do the rest!



---

## 🌟 About The Project

NutriSnap is a smart nutrition assistant designed to make healthy eating easier. It leverages a deep learning model, trained with a dataset managed on **Roboflow**, to classify food items from user-uploaded images. It then uses the power of Google's Gemini Pro to fetch and display a comprehensive nutritional breakdown for the identified food.

This project is built with:
*   **Python** as the core language.
*   **Flask** for the web framework.
*   **Roboflow** for dataset management, preprocessing, and augmentation.
*   **TensorFlow/Keras** for building and training the food image classification model.
*   **Google Gemini Pro API** for generative nutritional analysis.

---

## ✨ Features

*   **Image-Based Food Recognition**: Upload an image to identify the food item.
*   **Robust Model**: The classification model is trained on a well-managed and augmented dataset from Roboflow.
  
  
*   **Simple Web Interface**: Easy-to-use interface for a seamless user experience.

---

## ⚙️ How It Works

The application follows a simple, powerful workflow:

1.  **Image Upload**: The user selects and uploads a food image through the web interface.
2.  **Flask Backend**: The Flask server receives the image.
3.  **Image Preprocessing**: The image is resized and converted into the format required by the machine learning model.
4.  **Food Classification**: A pre-trained Keras/TensorFlow model (`final_model.h5`), which was trained using Roboflow, predicts the food class (e.g., "pizza", "samosa", "omelette").

5.  **Display Results**: The model's prediction and the detailed nutritional information from Gemini are sent back to the frontend and displayed to the user.

---

## 🤖 The Model & Dataset

The core of the food recognition system is the `final_model.h5`, a Convolutional Neural Network (CNN) built with TensorFlow/Keras.

The effectiveness of this model is heavily reliant on the quality of the training data. **Roboflow** was used to manage the entire data pipeline:

*   **Dataset Collection**: Aggregating images for various food classes.
*   **Annotation**: Labeling images with their correct food categories.
*   **Preprocessing & Augmentation**: Applying transformations like resizing, rotation, and color adjustments to create a larger, more diverse dataset. This helps the model generalize better and reduces overfitting.

By leveraging Roboflow, the dataset was refined and prepared efficiently, leading to a more robust and accurate classification model.

---

## 🛠️ Technology Stack

*   **Backend**: Flask, Gunicorn
*   **ML / Data Pipeline**: **Roboflow**, TensorFlow, Keras
   
*   **Image Processing**: Pillow (PIL)
*   **Frontend**: HTML, CSS, JavaScript


---

## 📝 Future Improvements

*   [ ] Expand the food classification model to recognize more dishes by adding more data in Roboflow.
*   [ ] Implement multi-label classification or object detection to identify multiple food items in a single image.
*   [ ] Add a database to store user history and track nutritional intake over time.
*   [ ] Improve the user interface and overall user experience.
*   [ ] Allow users to specify serving size for more accurate results.

---

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

---

## 📄 License

This project is unlicensed. You are free to use, modify, and distribute the code.

---

## 📧 Contact

Harshit Agarwal - [GitHub Profile](https://github.com/harshit1314)

Project Link: [https://github.com/harshit1314/NutriSnap](https://github.com/harshit1314/NutriSnap)

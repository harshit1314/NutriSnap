// frontend/src/App.jsx

import React, { useState, useRef } from 'react';
import axios from 'axios';
import './App.css'; // We will create this file for styling next

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  
  // A reference to the hidden file input element
  const fileInputRef = useRef(null);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
      setPreview(URL.createObjectURL(file)); // Create a temporary URL for image preview
      setAnalysisResult(null); // Clear previous results
      setError('');
    }
  };

  const handleUploadClick = () => {
    // Trigger the hidden file input when the user clicks our custom button
    fileInputRef.current.click();
  };

  const handleSubmit = async () => {
    if (!selectedFile) {
      setError('Please select an image first.');
      return;
    }

    // Create a FormData object to send the file
    const formData = new FormData();
    formData.append('image_file', selectedFile); // The key 'image_file' must match the backend!

    setIsLoading(true);
    setError('');
    setAnalysisResult(null);

    try {
      // The URL for our backend endpoint
      const API_URL = 'http://127.0.0.1:8000/analyze-meal/';
      const response = await axios.post(API_URL, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      // Check if our backend returned a specific error message
      if (response.data.error) {
        setError(response.data.error);
      } else {
        setAnalysisResult(response.data);
      }

    } catch (err) {
      console.error(err);
      setError('Failed to connect to the server. Is it running?');
    } finally {
      setIsLoading(false); // Stop the loading indicator
    }
  };

  return (
    <div className="container">
      <header>
        <h1>NutriSnap 📸</h1>
        <p>Analyze your meal from a photo. Remember to include a credit card for scale!</p>
      </header>

      <div className="upload-section">
        <input 
          type="file" 
          ref={fileInputRef} 
          onChange={handleFileChange} 
          style={{ display: 'none' }} // Hide the default ugly file input
          accept="image/*"
        />
        <button onClick={handleUploadClick} className="upload-button">
          {selectedFile ? 'Change Image' : 'Choose Image'}
        </button>
        <button onClick={handleSubmit} disabled={isLoading || !selectedFile} className="analyze-button">
          {isLoading ? 'Analyzing...' : 'Analyze Meal'}
        </button>
      </div>

      {error && <p className="error-message">{error}</p>}

      <div className="results-container">
        {preview && (
          <div className="image-preview">
            <h3>Your Image</h3>
            <img src={preview} alt="Selected meal" onLoad={() => URL.revokeObjectURL(preview)} />
          </div>
        )}
        {analysisResult && (
          <div className="analysis-results">
            <h3>Analysis Results</h3>
            {analysisResult.detected_foods.length > 0 ? (
              <ul>
                {analysisResult.detected_foods.map((food, index) => (
                  <li key={index}>
                    <span className="food-name">{food.name}</span>
                    <span className="food-grams">~{food.estimated_grams}g</span>
                    <span className="food-confidence">Conf: {(food.confidence * 100).toFixed(0)}%</span>
                  </li>
                ))}
              </ul>
            ) : (
              <p>No food items were detected in the image.</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
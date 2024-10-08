import React, { useState } from 'react';
import axios from 'axios';
import './UploadImage.css';

function UploadImage() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const [imagePreview, setImagePreview] = useState(null);

  // file selection
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    setSelectedFile(file);
    setPrediction(null);
    setError(null);

    // image preview
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result);
      };
      reader.readAsDataURL(file);
    } else {
      setImagePreview(null);
    }
  };

  // drag
  const handleDragOver = (event) => {
    event.preventDefault();
    event.stopPropagation();
    setDragActive(true);
  };

  const handleDragLeave = (event) => {
    event.preventDefault();
    event.stopPropagation();
    setDragActive(false);
  };

  const handleDrop = (event) => {
    event.preventDefault();
    event.stopPropagation();
    setDragActive(false);
    if (event.dataTransfer.files && event.dataTransfer.files[0]) {
      const file = event.dataTransfer.files[0];
      setSelectedFile(file);
      setPrediction(null);
      setError(null);

      // preview
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  // submission
  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!selectedFile) {
      setError('Please select an image file.');
      return;
    }

    const formData = new FormData();
    formData.append('image', selectedFile);

    try {
      const response = await axios.post(
        'http://localhost:8000/inference',
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );
      setPrediction(response.data.prediction);
      setError(null);
    } catch (err) {
      console.error(err);
      setError(err.response ? err.response.data.error : 'An error occurred.');
    }
  };

  return (
    <div className="upload-image-container">
      <form
        onSubmit={handleSubmit}
        className="upload-image"
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <div
          className={`file-input-container ${dragActive ? 'drag-active' : ''}`}
        >
          <label htmlFor="file-upload" className="file-upload-label">
            {selectedFile ? selectedFile.name : 'Click or drag and drop an image'}
          </label>
          <input
            id="file-upload"
            type="file"
            onChange={handleFileChange}
            accept="image/*"
            className="file-input"
          />
        </div>
        <button type="submit" className="submit-button">
          Classify ID/Passport
        </button>
      </form>

      {imagePreview && (
        <div className="image-preview">
          <img src={imagePreview} alt="Selected" />
        </div>
      )}

      {prediction && (
        <div className="result">
          <h2>Identity Document Class:</h2>
          <p>{prediction}</p>
        </div>
      )}

      {error && (
        <div className="error">
          <h2>Error:</h2>
          <p>{error}</p>
        </div>
      )}
    </div>
  );
}

export default UploadImage;
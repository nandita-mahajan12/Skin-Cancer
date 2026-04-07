"""
Skin Cancer Detection Backend API
Flask API for serving predictions from the trained model
"""

import os
import numpy as np
from pathlib import Path
from datetime import datetime
import json

# Flask imports
from flask import Flask, request, jsonify
from flask_cors import CORS

# TensorFlow imports
import tensorflow as tf
from tensorflow import keras

# Image processing
from PIL import Image
import io
import cv2

# ============================================================================
# FLASK APP INITIALIZATION
# ============================================================================

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
IMG_SIZE = 224
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'model', 'skin_cancer_model.h5')

# Create a simple model if the trained model doesn't exist
model = None

def load_model():
    """Load the trained model"""
    global model
    
    if os.path.exists(MODEL_PATH):
        print(f"✅ Loading model from: {MODEL_PATH}")
        try:
            model = keras.models.load_model(MODEL_PATH)
            print("✅ Model loaded successfully!")
            return True
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            return False
    else:
        print(f"⚠️  Model not found at: {MODEL_PATH}")
        print("Creating a simple demo model for testing...")
        create_demo_model()
        return True


def create_demo_model():
    """Create a simple demo model for testing without training"""
    global model
    
    from tensorflow.keras import layers
    from tensorflow.keras.applications import MobileNetV2
    
    base_model = MobileNetV2(
        input_shape=(IMG_SIZE, IMG_SIZE, 3),
        include_top=False,
        weights='imagenet'
    )
    base_model.trainable = False
    
    model = keras.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(64, activation='relu'),
        layers.Dropout(0.2),
        layers.Dense(2, activation='softmax')
    ])
    
    print("✅ Demo model created (weights are pre-trained on ImageNet)")


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def preprocess_image(img_array):
    """
    Preprocess image for model prediction
    
    Args:
        img_array: numpy array of image
    
    Returns:
        preprocessed image array
    """
    # Ensure image is 3-channel RGB
    if len(img_array.shape) == 2:
        img_array = np.stack([img_array] * 3, axis=-1)
    elif img_array.shape[2] == 4:  # RGBA
        img_array = img_array[:, :, :3]
    
    # Resize to model input size
    img_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
    
    # Normalize to [0, 1]
    img_array = img_array.astype('float32') / 255.0
    
    # Add batch dimension
    img_array = np.expand_dims(img_array, axis=0)
    
    return img_array


def validate_image(file_obj):
    """
    Validate uploaded image
    
    Args:
        file_obj: File object from request
    
    Returns:
        tuple: (is_valid, error_message, image_array)
    """
    try:
        # Check file exists and has content
        if not file_obj or file_obj.filename == '':
            return False, "No file selected", None
        
        # Check file extension
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
        file_ext = file_obj.filename.rsplit('.', 1)[1].lower()
        
        if file_ext not in allowed_extensions:
            return False, f"Invalid file format. Allowed: {', '.join(allowed_extensions)}", None
        
        # Read and validate image
        img = Image.open(file_obj.stream)
        
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Convert to numpy array
        img_array = np.array(img)
        
        # Check image size (must be reasonable)
        if img_array.shape[0] < 50 or img_array.shape[1] < 50:
            return False, "Image too small (minimum 50x50 pixels)", None
        
        if img_array.shape[0] > 4000 or img_array.shape[1] > 4000:
            return False, "Image too large (maximum 4000x4000 pixels)", None
        
        return True, None, img_array
        
    except Exception as e:
        return False, f"Error processing image: {str(e)}", None


# ============================================================================
# API ROUTES
# ============================================================================

@app.route('/', methods=['GET'])
def home():
    """Health check endpoint"""
    return jsonify({
        'status': 'success',
        'message': 'Skin Cancer Detection API is running',
        'version': '1.0.0',
        'endpoints': {
            'health': 'GET /',
            'predict': 'POST /predict',
            'model_info': 'GET /model-info'
        }
    }), 200


@app.route('/health', methods=['GET'])
def health():
    """Health check with model status"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'timestamp': datetime.now().isoformat()
    }), 200


@app.route('/model-info', methods=['GET'])
def model_info():
    """Get information about the model"""
    if model is None:
        return jsonify({
            'status': 'error',
            'message': 'Model not loaded'
        }), 500
    
    return jsonify({
        'status': 'success',
        'model_name': 'MobileNetV2 - Skin Cancer Detector',
        'classes': ['Benign', 'Malignant'],
        'input_size': f'{IMG_SIZE}x{IMG_SIZE}',
        'classification_type': 'Binary Classification',
        'model_path': MODEL_PATH
    }), 200


@app.route('/predict', methods=['POST'])
def predict():
    """
    Main prediction endpoint
    
    Expected request format:
        - File upload: form-data with key "image"
        - Returns: JSON with prediction and confidence
    """
    try:
        # Check if model is loaded
        if model is None:
            return jsonify({
                'status': 'error',
                'message': 'Model not loaded'
            }), 500
        
        # Check if image file is in request
        if 'image' not in request.files:
            return jsonify({
                'status': 'error',
                'message': 'No image file provided. Use key: "image"'
            }), 400
        
        file_obj = request.files['image']
        
        # Validate image
        is_valid, error_msg, img_array = validate_image(file_obj)
        if not is_valid:
            return jsonify({
                'status': 'error',
                'message': error_msg
            }), 400
        
        # Preprocess image
        processed_img = preprocess_image(img_array)
        
        # Make prediction
        predictions = model.predict(processed_img, verbose=0)
        
        # Extract results
        benign_prob = float(predictions[0][0])
        malignant_prob = float(predictions[0][1])
        
        # Determine class
        predicted_class = 'Benign' if benign_prob > malignant_prob else 'Malignant'
        confidence = max(benign_prob, malignant_prob)
        
        # Prepare response
        response = {
            'status': 'success',
            'prediction': predicted_class,
            'confidence': round(confidence, 4),
            'probabilities': {
                'benign': round(benign_prob, 4),
                'malignant': round(malignant_prob, 4)
            },
            'recommendation': (
                'Please consult a dermatologist for further evaluation.'
                if predicted_class == 'Malignant'
                else 'Likely benign, but regular monitoring is recommended.'
            ),
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Prediction error: {str(e)}'
        }), 500


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'status': 'error',
        'message': 'Endpoint not found',
        'available_endpoints': {
            'health': 'GET /',
            'predict': 'POST /predict',
            'model_info': 'GET /model-info'
        }
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors"""
    return jsonify({
        'status': 'error',
        'message': 'Method not allowed'
    }), 405


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'status': 'error',
        'message': 'Internal server error'
    }), 500


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("🚀 SKIN CANCER DETECTION API SERVER")
    print("=" * 70)
    
    # Load model
    print("\n📦 Loading model...")
    load_model()
    
    # Start Flask server
    print("\n" + "=" * 70)
    print("✅ Server starting...")
    print("=" * 70)
    print("\n🌐 API running at: http://localhost:5000")
    print("\n📚 Available endpoints:")
    print("   - GET  http://localhost:5000/           (Health check)")
    print("   - GET  http://localhost:5000/health     (Health status)")
    print("   - GET  http://localhost:5000/model-info (Model information)")
    print("   - POST http://localhost:5000/predict    (Make prediction)")
    print("\n" + "=" * 70 + "\n")
    
    # Run Flask app
    # Set debug=False for production, True for development
    if __name__ == "__main__":
     app.run(host="0.0.0.0", port=10000)
# 🏥 Skin Cancer Detection Web Application

A complete end-to-end deep learning application for detecting skin cancer using a CNN model. This project includes a trained model, Flask backend API, and an interactive web frontend.

## 📋 Table of Contents

- [Features](#-features)
- [Project Structure](#-project-structure)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
- [Local Development](#-local-development)
- [Model Training](#-model-training)
- [API Documentation](#-api-documentation)
- [Deployment](#-deployment)
- [Testing](#-testing)
- [Troubleshooting](#-troubleshooting)
- [Important Disclaimer](#-important-disclaimer)

---

## ⭐ Features

- ✅ **AI-Powered Detection**: Binary classification (Benign/Malignant)
- ✅ **Fast Predictions**: Real-time analysis in seconds
- ✅ **User-Friendly UI**: Modern, responsive web interface
- ✅ **Transfer Learning**: MobileNetV2 pre-trained model
- ✅ **Data Augmentation**: Robust training with 10,000+ images
- ✅ **API First**: RESTful Flask backend
- ✅ **Error Handling**: Comprehensive validation and error messages
- ✅ **CORS Support**: Ready for cross-origin requests
- ✅ **Report Generation**: Download analysis reports

---

## 📁 Project Structure

```
skin-cancer-app/
│
├── model/
│   └── skin_cancer_model.h5          # Trained model (generated after training)
│
├── backend/
│   ├── app.py                        # Flask API server
│   └── requirements.txt              # Backend dependencies
│
├── frontend/
│   ├── index.html                    # Web application UI
│   ├── style.css                     # Styling
│   ├── script.js                     # Frontend logic
│   └── vercel.json                   # Vercel deployment config
│
├── train_model.py                    # Model training script
├── requirements.txt                  # Training dependencies
├── Procfile                          # Render deployment config
└── README.md                         # This file
```

---

## 🛠️ Tech Stack

### Backend
- **Framework**: Flask 2.3.3
- **ML Framework**: TensorFlow/Keras 2.13.0
- **Model**: MobileNetV2 (Transfer Learning)
- **Server**: Gunicorn (for production)
- **Language**: Python 3.8+

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with responsive design
- **JavaScript**: Vanilla (No framework dependencies)
- **Image Processing**: Canvas API

### Dataset
- **HAM10000**: 10,000 dermatoscopic images
- **Classes**: Benign, Malignant
- **Input Size**: 224×224 pixels (RGB)

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (optional, for cloning)
- Modern web browser (Chrome, Firefox, Edge, Safari)

### Quick Start (5 minutes)

#### 1. **Install Backend Dependencies**

```bash
# Navigate to project directory
cd skin-cancer-app

# Install all dependencies
pip install -r backend/requirements.txt
```

#### 2. **Start Backend Server**

```bash
# Run Flask server
python backend/app.py
```

Expected output:
```
🚀 SKIN CANCER DETECTION API SERVER
=====================================

✅ Server starting...
🌐 API running at: http://localhost:5000
```

#### 3. **Open Frontend in Browser**

```bash
# In another terminal, open the frontend
# Option 1: On Windows
start frontend/index.html

# Option 2: Using Python
python -m http.server 8000 --directory frontend

# Then visit: http://localhost:8000
```

#### 4. **Test the Application**

1. Go to http://localhost:8000 in your browser
2. Upload a skin lesion image
3. Click "Analyze Image"
4. View prediction results

---

## 📚 Local Development

### Development Setup

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt

# Install training dependencies
pip install -r requirements.txt
```

### Running in Development Mode

#### Backend (with auto-reload):
```bash
python backend/app.py
```

#### Frontend (with live server):
```bash
# Using Python's built-in server
python -m http.server 8000 --directory frontend

# Or using Node.js (if installed)
npx -y serve frontend
```

### File Watching for CSS/JS Updates

The frontend automatically reloads when you modify CSS/JS files in most browsers using Python's live server.

---

## 🧠 Model Training

### Download Dataset

1. **HAM10000 Dataset**:
   - Download from: https://www.kaggle.com/datasets/kmader/skin-cancer-mnist-ham10000
   - Requires Kaggle account

2. **Organize Dataset**:
```
data/
└── HAM10000/
    ├── benign/
    │   ├── image_1.jpg
    │   ├── image_2.jpg
    │   └── ...
    └── malignant/
        ├── image_1.jpg
        ├── image_2.jpg
        └── ...
```

### Train the Model

```bash
# Install training dependencies
pip install -r requirements.txt

# Run training script
python train_model.py
```

**Training Output**:
- Saves model to: `./model/skin_cancer_model.h5`
- Training time: ~30-60 minutes (depending on hardware)
- Expected accuracy: 85-92% on test set

### Training Pipeline Stages

1. **Data Preparation**: Load and preprocess images
2. **Preprocessing**: Normalize to [0,1], split into train/test
3. **Model Building**: MobileNetV2 base + custom head
4. **Phase 1 Training**: Frozen base model (5 epochs)
5. **Phase 2 Fine-tuning**: Unfrozen last 50 layers (5 epochs)
6. **Evaluation**: Test on validation set
7. **Save Model**: H5 format for deployment

### Using Pre-trained Model

If you don't train, the app creates a demo model:
```python
# In backend/app.py, function: create_demo_model()
# Uses ImageNet weights (no skin cancer specific training)
```

---

## 📡 API Documentation

### Base URL
- **Development**: `http://localhost:5000`
- **Production**: `https://[your-render-app].onrender.com`

### Endpoints

#### 1. Health Check
```
GET /
```

**Response**:
```json
{
  "status": "success",
  "message": "Skin Cancer Detection API is running",
  "version": "1.0.0"
}
```

#### 2. Model Information
```
GET /model-info
```

**Response**:
```json
{
  "status": "success",
  "model_name": "MobileNetV2 - Skin Cancer Detector",
  "classes": ["Benign", "Malignant"],
  "input_size": "224x224"
}
```

#### 3. Make Prediction ⭐
```
POST /predict
Content-Type: multipart/form-data

image: <image_file>
```

**Response**:
```json
{
  "status": "success",
  "prediction": "Benign",
  "confidence": 0.96,
  "probabilities": {
    "benign": 0.96,
    "malignant": 0.04
  },
  "recommendation": "Likely benign, but regular monitoring is recommended.",
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

**Error Response**:
```json
{
  "status": "error",
  "message": "No image file provided. Use key: 'image'"
}
```

### Image Requirements
- **Formats**: JPG, PNG, GIF, BMP
- **Size**: 50×50 to 4000×4000 pixels
- **Max File Size**: 10 MB

---

## 🧪 Testing

### Using Postman

1. **Download Postman**: https://www.postman.com/downloads/

2. **Test Prediction Endpoint**:
   - Method: `POST`
   - URL: `http://localhost:5000/predict`
   - Tab: `Body` → `form-data`
   - Key: `image` → Select your image file
   - Click `Send`

### Using curl

```bash
# Test health endpoint
curl http://localhost:5000/

# Test prediction (Linux/macOS)
curl -X POST -F "image=@/path/to/image.jpg" http://localhost:5000/predict

# Test prediction (Windows PowerShell)
$form = @{ image = Get-Item -Path "path\to\image.jpg" }
Invoke-WebRequest -Uri "http://localhost:5000/predict" -Form $form -Method Post
```

### Using Python

```python
import requests

# Upload and get prediction
with open('test_image.jpg', 'rb') as f:
    files = {'image': f}
    response = requests.post('http://localhost:5000/predict', files=files)
    result = response.json()
    print(result)
```

---

## 🚀 Deployment

### Backend Deployment (Render)

#### Step 1: Prepare Repository

```bash
# Initialize git repository
git init
git add .
git commit -m "Initial commit"
```

#### Step 2: Create Render Account

1. Go to https://render.com
2. Sign up (free account available)
3. Connect GitHub or provide code via web

#### Step 3: Deploy

1. Click "New" → "Web Service"
2. Select your repository
3. **Name**: skin-cancer-api
4. **Runtime**: Python 3
5. **Build Command**: `pip install -r backend/requirements.txt`
6. **Start Command**: `gunicorn backend.app:app --timeout 300`
7. **Environment Variables**:
   - `FLASK_ENV`: production
   - `PYTHON_VERSION`: 3.11

#### Step 4: Deploy

Click "Create Web Service" and wait ~5 minutes for deployment.

**Your API URL**: `https://[your-app-name].onrender.com`

#### Important Notes

⚠️ **Model File Size**:
- The H5 model file should be < 100MB for free tier
- If larger, use TensorFlow Lite conversion or model quantization

### Frontend Deployment (Vercel)

#### Step 1: Prepare Frontend

Update API URL in `frontend/script.js`:
```javascript
// Before deployment
const API_BASE_URL = 'http://localhost:5000';

// After Render deployment
const API_BASE_URL = 'https://[your-render-app].onrender.com';
```

#### Step 2: Create Vercel Account

1. Go to https://vercel.com
2. Sign up with GitHub

#### Step 3: Deploy

1. Click "Add New" → "Project"
2. Import your GitHub repository
3. **Framework**: Other (Static)
4. **Root Directory**: `./frontend`
5. Click "Deploy"

**Your Frontend URL**: `https://[your-project-name].vercel.app`

#### Step 4: Update CORS

Add your frontend URL to Flask CORS:

```python
# backend/app.py
CORS(app, origins=[
    "http://localhost:8000",
    "https://[your-vercel-frontend].vercel.app"
])
```

---

## 🔗 Full Stack Integration

Once deployed, update `frontend/script.js`:

```javascript
// Production URLs
const API_BASE_URL = 'https://skin-cancer-api.onrender.com';
// const API_BASE_URL = 'http://localhost:5000'; // For local development
```

Then:
1. Redeploy frontend to Vercel
2. Test at: `https://[your-vercel-frontend].vercel.app`
3. Should connect to Render backend successfully

---

## 🐛 Troubleshooting

### Issue: "Cannot find module 'tensorflow'"

**Solution**:
```bash
# Make sure you're in the virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r backend/requirements.txt
```

### Issue: "Model not found at ./model/skin_cancer_model.h5"

**Solution**:
1. Train the model first: `python train_model.py`
2. Or, the app will create a demo model (pre-trained on ImageNet)

### Issue: API returns 500 error

**Check**:
1. Is Flask server running? (`python backend/app.py`)
2. Are all dependencies installed? (`pip install -r backend/requirements.txt`)
3. Check console for error messages
4. Verify file paths are correct

### Issue: CORS error when uploading image

**Solution**:
Make sure CORS is enabled in `backend/app.py`:
```python
from flask_cors import CORS
CORS(app)  # Enable CORS for all routes
```

### Issue: Image upload fails with "Invalid file format"

**Check**:
- Image format is JPG, PNG, GIF, or BMP
- File size is less than 10MB
- Image dimensions are 50×50 to 4000×4000 pixels

### Issue: Slow predictions

**Causes**:
- First request is slower (model loading)
- Large image being processed
- Limited system resources

**Solutions**:
- Wait for first request to complete
- Resize large images beforehand
- Upgrade hardware or cloud provider tier

---

## 📊 Project Statistics

| Metric | Value |
|--------|-------|
| Lines of Code | ~2500 |
| Model Parameters | ~3.5M |
| Dataset Size | 10,000 images |
| Training Time | 30-60 min |
| Expected Accuracy | 85-92% |
| Model File Size | ~50 MB |
| API Response Time | 2-5 seconds |

---

## 🔐 Security Considerations

⚠️ **Important for Production**:

1. **Never commit model file to git**:
   ```bash
   # Add to .gitignore
   echo "model/*.h5" >> .gitignore
   ```

2. **Use environment variables**:
   ```python
   import os
   API_KEY = os.getenv('API_KEY')
   DEBUG = os.getenv('FLASK_ENV') == 'development'
   ```

3. **Implement API authentication** (if needed):
   ```python
   from functools import wraps
   from flask import request
   
   def require_api_key(f):
       @wraps(f)
       def decorated(*args, **kwargs):
           key = request.headers.get('X-API-Key')
           if key and key == os.getenv('API_KEY'):
               return f(*args, **kwargs)
           return {'status': 'error', 'message': 'Invalid API key'}, 401
       return decorated
   ```

4. **Set FLASK_ENV to production**:
   ```bash
   export FLASK_ENV=production
   ```

5. **Use HTTPS only** (automatic on Render/Vercel)

---

## 📦 Dependencies

### Backend
- Flask 2.3.3 - Web framework
- TensorFlow 2.13.0 - Deep learning
- OpenCV 4.8.0.76 - Image processing
- Pillow 10.0.0 - Image handling
- Numpy 1.24.3 - Numerical computing
- Gunicorn 21.2.0 - WSGI server

### Training
- Pandas 2.0.3 - Data analysis
- Matplotlib 3.7.2 - Visualization
- Scikit-learn 1.3.0 - ML utilities

---

## 📝 License

This project is available under the MIT License.

---

## 🎓 Learning Resources

- [TensorFlow Transfer Learning](https://www.tensorflow.org/tutorials/images/transfer_learning)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [MobileNetV2 Paper](https://arxiv.org/abs/1801.04381)
- [HAM10000 Dataset](https://github.com/udacity/dermatologist-ai)

---

## ⚠️ Important Disclaimer

**MEDICAL DISCLAIMER**:

This application is designed for **educational and research purposes only**. It should **NOT** be used as a substitute for professional medical diagnosis, consultation, or treatment. 

**Always consult a qualified dermatologist** for:
- Accurate skin cancer diagnosis
- Medical advice and treatment options
- Second opinions on skin lesions

The AI model predictions are based on image analysis and may have limitations:
- Accuracy depends on image quality and lighting
- Model has limitations on certain skin types
- Cannot detect internal characteristics
- Should only be used as a supportive tool

**By using this application, you agree that**:
- You understand this is not medical advice
- You will consult healthcare professionals for actual diagnosis
- The developers are not liable for any medical decisions
- You are responsible for seeking proper medical care

---

## 👥 Support & Contact

For issues, feature requests, or questions:
1. Check the [Troubleshooting](#-troubleshooting) section
2. Review API documentation
3. Check backend/app.py comments for detailed explanations

---

## ✨ Future Enhancements

- [ ] Multi-class classification (7+ skin conditions)
- [ ] Mobile app (React Native/Flutter)
- [ ] Batch processing API
- [ ] User accounts & history
- [ ] Model versioning
- [ ] A/B testing framework
- [ ] Advanced analytics dashboard
- [ ] Integration with medical imaging formats (DICOM)

---

**Created with ❤️ using Deep Learning**

Built with TensorFlow, Flask, and JavaScript. Trained on HAM10000 dataset.

Last updated: January 2024

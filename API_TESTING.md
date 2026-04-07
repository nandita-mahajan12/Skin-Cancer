# API Testing Guide

This guide shows how to test the Skin Cancer Detection API using various tools.

---

## 🔧 Prerequisites

- Backend server running: `python backend/app.py`
- API URL: `http://localhost:5000` (or your deployed URL)
- Test image file (JPG, PNG, GIF, BMP)

---

## 1️⃣ Using CURL (Command Line)

### Test Health Endpoint
```bash
curl -X GET http://localhost:5000/
```

**Expected Response**:
```json
{
  "status": "success",
  "message": "Skin Cancer Detection API is running",
  "version": "1.0.0"
}
```

### Test Health Status
```bash
curl -X GET http://localhost:5000/health
```

### Test Model Info
```bash
curl -X GET http://localhost:5000/model-info
```

### Test Prediction (Linux/macOS)
```bash
curl -X POST -F "image=@/path/to/image.jpg" http://localhost:5000/predict
```

### Test Prediction (Windows)
```bash
# Using curl (if installed)
curl -X POST -F "image=@C:\path\to\image.jpg" http://localhost:5000/predict

# Using PowerShell
$form = @{ image = Get-Item -Path "path\to\image.jpg" }
Invoke-WebRequest -Uri "http://localhost:5000/predict" -Form $form -Method Post
```

---

## 2️⃣ Using Python

### Simple Test Script

```python
import requests
import json

# API URL
API_URL = "http://localhost:5000"

def test_health():
    """Test health endpoint"""
    response = requests.get(f"{API_URL}/")
    print("✅ Health Check:")
    print(json.dumps(response.json(), indent=2))

def test_model_info():
    """Test model info endpoint"""
    response = requests.get(f"{API_URL}/model-info")
    print("\n✅ Model Info:")
    print(json.dumps(response.json(), indent=2))

def test_prediction(image_path):
    """Test prediction endpoint"""
    with open(image_path, 'rb') as f:
        files = {'image': f}
        response = requests.post(f"{API_URL}/predict", files=files)
    
    result = response.json()
    print("\n✅ Prediction Result:")
    print(json.dumps(result, indent=2))
    
    # Extract results
    if result['status'] == 'success':
        prediction = result['prediction']
        confidence = result['confidence']
        print(f"\n🎯 Diagnosis: {prediction}")
        print(f"📊 Confidence: {confidence * 100:.2f}%")
        print(f"💬 Recommendation: {result['recommendation']}")

if __name__ == "__main__":
    # Run tests
    test_health()
    test_model_info()
    
    # Test with image
    image_path = "test_image.jpg"  # Change to your test image
    test_prediction(image_path)
```

### Running the Test Script

```bash
# Install required package
pip install requests

# Run the script
python test_api.py
```

---

## 3️⃣ Using Postman

### Setup

1. **Download Postman**: https://www.postman.com/downloads/
2. **Import Collection** (Optional):
   - You can create requests manually or import our collection

### Test Endpoints

#### Request 1: Health Check
- **Method**: GET
- **URL**: `http://localhost:5000/`
- **Headers**: None
- **Body**: None
- **Send** → Should show success message

#### Request 2: Model Info
- **Method**: GET
- **URL**: `http://localhost:5000/model-info`
- **Headers**: None
- **Body**: None
- **Send** → Should show model configuration

#### Request 3: Image Prediction ⭐
- **Method**: POST
- **URL**: `http://localhost:5000/predict`
- **Headers**: (Auto-generated with form-data)
- **Body**:
  - Type: `form-data`
  - Key: `image`
  - Value: Select your test image file
- **Send** → Should return prediction with confidence

### Save Response
- Click "Save as..." to save response examples
- Name: `successful_prediction_response.json`

---

## 4️⃣ Using JavaScript/Fetch API

### Code Example

```javascript
// Test API from browser console

const API_URL = 'http://localhost:5000';

// Test health
async function testHealth() {
    const response = await fetch(`${API_URL}/`, { method: 'GET' });
    const data = await response.json();
    console.log('Health Check:', data);
}

// Test prediction
async function testPrediction(imageFile) {
    const formData = new FormData();
    formData.append('image', imageFile);
    
    const response = await fetch(`${API_URL}/predict`, {
        method: 'POST',
        body: formData
    });
    
    const result = await response.json();
    console.log('Prediction:', result);
    
    if (result.status === 'success') {
        console.log(`Prediction: ${result.prediction}`);
        console.log(`Confidence: ${(result.confidence * 100).toFixed(2)}%`);
    }
}

// Usage
testHealth();
// For prediction, you need an actual file input
```

### From File Input
```javascript
// Add file input to HTML
// <input type="file" id="imageInput" accept="image/*">

const fileInput = document.getElementById('imageInput');
fileInput.addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (file) {
        await testPrediction(file);
    }
});
```

---

## 5️⃣ Using Insomnia

Insomnia is similar to Postman. Here's how to set it up:

1. **Download**: https://insomnia.rest/
2. **Create Request**:
   - URL: `http://localhost:5000/predict`
   - Method: POST
   - Body: form-data
   - Key: `image` → Select file
3. **Send**: Click "Send"

---

## 📊 Expected Responses

### Success Response (Benign)
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

### Success Response (Malignant)
```json
{
  "status": "success",
  "prediction": "Malignant",
  "confidence": 0.89,
  "probabilities": {
    "benign": 0.11,
    "malignant": 0.89
  },
  "recommendation": "Please consult a dermatologist for further evaluation.",
  "timestamp": "2024-01-15T10:35:22.654321"
}
```

### Error Response
```json
{
  "status": "error",
  "message": "No image file provided. Use key: 'image'"
}
```

---

## ⚠️ Common Issues & Solutions

### Issue: 404 Not Found
```
Problem: curl: (7) Failed to connect to localhost port 5000
Solution: Make sure Flask server is running: python backend/app.py
```

### Issue: CORS Error (Browser)
```
Problem: Access to XMLHttpRequest blocked by CORS
Solution: CORS is already enabled, make sure both frontend and backend are running
```

### Issue: 413 Payload Too Large
```
Problem: File size exceeds limit
Solution: Use image < 10MB
```

### Issue: Invalid Image Format
```
Problem: {"status": "error", "message": "Invalid file format"}
Solution: Use JPG, PNG, GIF, or BMP format
```

### Issue: 500 Internal Server Error
```
Problem: Server error processing image
Solution: 
1. Check console for error details
2. Ensure image is valid
3. Check image size (50×50 to 4000×4000)
```

---

## 🧪 Test Images

### Create a Test Image

```python
# test_image_generator.py
import numpy as np
import cv2
from PIL import Image

# Create a simple test image
img_array = np.random.randint(0, 256, (224, 224, 3), dtype=np.uint8)
img = Image.fromarray(img_array)
img.save('test_image.jpg')

print("✅ Test image created: test_image.jpg")
```

### Run:
```bash
python test_image_generator.py
```

---

## 📈 Performance Testing

### Load Testing with Apache Bench

```bash
# Test with 100 requests
ab -n 100 -c 10 http://localhost:5000/

# Test prediction endpoint (requires POST)
# Use Apache Bench with POST files
```

### Using Python (siege or locust)

```python
# simple_load_test.py
import concurrent.futures
import requests
import time

API_URL = "http://localhost:5000"
IMAGE_PATH = "test_image.jpg"

def make_request():
    with open(IMAGE_PATH, 'rb') as f:
        files = {'image': f}
        start = time.time()
        response = requests.post(f"{API_URL}/predict", files=files)
        elapsed = time.time() - start
    return elapsed, response.status_code

# Run 10 concurrent requests
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(make_request) for _ in range(10)]
    results = [f.result() for f in concurrent.futures.as_completed(futures)]

# Analyze
times = [r[0] for r in results]
print(f"Average Response Time: {np.mean(times):.2f}s")
print(f"Max Response Time: {np.max(times):.2f}s")
print(f"Min Response Time: {np.min(times):.2f}s")
```

---

## ✅ Checklist

- [ ] Flask server is running
- [ ] API responds to GET / endpoint
- [ ] Image file is in supported format
- [ ] Image file is < 10MB
- [ ] Image dimensions are acceptable
- [ ] Can upload image and get prediction
- [ ] Prediction includes confidence score
- [ ] Error messages are clear
- [ ] CORS headers are present
- [ ] Response time is acceptable

---

## 🚀 Next Steps

After successful local testing:
1. Deploy backend to Render
2. Deploy frontend to Vercel
3. Test with production URLs
4. Monitor API performance
5. Gather user feedback

---

**Have issues? Check the main README.md for troubleshooting!**

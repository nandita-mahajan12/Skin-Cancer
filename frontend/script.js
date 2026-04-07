/**
 * Skin Cancer Detection - Frontend Script
 * Handles image upload, API interaction, and result display
 */

// ============================================================================
// CONFIGURATION
// ============================================================================

// Change this to your deployed backend URL for production
// For development: http://localhost:5000
// For production (Render): https://your-app-name.onrender.com
const API_BASE_URL = 'http://localhost:5000';

// ============================================================================
// STATE MANAGEMENT
// ============================================================================

const state = {
    selectedImage: null,
    selectedFileName: '',
    isAnalyzing: false,
    currentResult: null
};

// ============================================================================
// INITIALIZATION
// ============================================================================

document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 Skin Cancer Detection App Initialized');
    setupEventListeners();
    checkAPIConnection();
});

// ============================================================================
// EVENT LISTENERS
// ============================================================================

function setupEventListeners() {
    // File input change
    document.getElementById('imageInput').addEventListener('change', handleImageSelect);

    // Upload area drag and drop
    const uploadArea = document.getElementById('uploadArea');
    
    uploadArea.addEventListener('click', () => {
        document.getElementById('imageInput').click();
    });

    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('drag-over');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('drag-over');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('drag-over');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            document.getElementById('imageInput').files = files;
            handleImageSelect({ target: { files: files } });
        }
    });
}

// ============================================================================
// IMAGE HANDLING
// ============================================================================

function handleImageSelect(event) {
    const files = event.target.files;
    
    if (files.length === 0) {
        return;
    }

    const file = files[0];

    // Validate file
    const validTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/bmp'];
    const maxSize = 10 * 1024 * 1024; // 10MB

    if (!validTypes.includes(file.type)) {
        showError('Invalid image format. Please upload JPG, PNG, GIF, or BMP.');
        return;
    }

    if (file.size > maxSize) {
        showError('Image too large. Maximum size is 10MB.');
        return;
    }

    // Read and display image
    const reader = new FileReader();

    reader.onload = (e) => {
        state.selectedImage = e.target.result;
        state.selectedFileName = file.name;

        // Show preview
        showPreview();
    };

    reader.onerror = () => {
        showError('Error reading image file.');
    };

    reader.readAsDataURL(file);
}

function showPreview() {
    document.getElementById('uploadArea').style.display = 'none';
    document.getElementById('previewSection').style.display = 'block';
    document.getElementById('resultsSection').style.display = 'none';
    document.getElementById('loadingSection').style.display = 'none';
    document.getElementById('errorSection').style.display = 'none';

    document.getElementById('previewImage').src = state.selectedImage;
}

// ============================================================================
// IMAGE ANALYSIS
// ============================================================================

async function analyzeImage() {
    if (!state.selectedImage) {
        showError('No image selected');
        return;
    }

    if (state.isAnalyzing) {
        console.log('Already analyzing...');
        return;
    }

    state.isAnalyzing = true;

    try {
        // Show loading
        showLoading();

        // Convert data URL to blob
        const blob = dataURLToBlob(state.selectedImage);
        
        // Create form data
        const formData = new FormData();
        formData.append('image', blob, state.selectedFileName);

        // Send request
        console.log('Sending image to API...');
        const response = await fetch(`${API_BASE_URL}/predict`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || 'API Error');
        }

        const result = await response.json();
        console.log('Result:', result);

        if (result.status === 'success') {
            displayResults(result);
        } else {
            showError(result.message || 'Prediction failed');
        }

    } catch (error) {
        console.error('Error:', error);
        showError(`Error: ${error.message}`);
    } finally {
        state.isAnalyzing = false;
    }
}

// ============================================================================
// RESULT DISPLAY
// ============================================================================

function displayResults(result) {
    state.currentResult = result;

    // Hide other sections
    document.getElementById('uploadArea').style.display = 'none';
    document.getElementById('previewSection').style.display = 'none';
    document.getElementById('loadingSection').style.display = 'none';
    document.getElementById('errorSection').style.display = 'none';
    document.getElementById('resultsSection').style.display = 'block';

    // Set prediction
    const prediction = result.prediction;
    const confidence = (result.confidence * 100).toFixed(2);

    document.getElementById('predictionText').textContent = prediction;
    document.getElementById('confidenceText').textContent = `Confidence: ${confidence}%`;

    // Set icon
    const icon = prediction === 'Benign' ? '✅' : '⚠️';
    document.getElementById('predictionIcon').textContent = icon;

    // Update card color
    const predictionCard = document.querySelector('.prediction-card');
    if (prediction === 'Benign') {
        predictionCard.style.background = 'linear-gradient(135deg, #4ECDC4 0%, #44A08D 100%)';
    } else {
        predictionCard.style.background = 'linear-gradient(135deg, #FF6B6B 0%, #FF5252 100%)';
    }

    // Set probabilities
    const benignProb = (result.probabilities.benign * 100).toFixed(2);
    const malignantProb = (result.probabilities.malignant * 100).toFixed(2);

    document.getElementById('benignBar').style.width = `${result.probabilities.benign * 100}%`;
    document.getElementById('benignProb').textContent = `${benignProb}%`;

    document.getElementById('malignantBar').style.width = `${result.probabilities.malignant * 100}%`;
    document.getElementById('malignantProb').textContent = `${malignantProb}%`;

    // Set recommendation
    document.getElementById('recommendationText').textContent = result.recommendation;

    console.log('Results displayed successfully');
}

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

function showLoading() {
    document.getElementById('uploadArea').style.display = 'none';
    document.getElementById('previewSection').style.display = 'none';
    document.getElementById('resultsSection').style.display = 'none';
    document.getElementById('errorSection').style.display = 'none';
    document.getElementById('loadingSection').style.display = 'block';
}

function showError(message) {
    document.getElementById('uploadArea').style.display = 'none';
    document.getElementById('previewSection').style.display = 'none';
    document.getElementById('resultsSection').style.display = 'none';
    document.getElementById('loadingSection').style.display = 'none';
    document.getElementById('errorSection').style.display = 'block';

    document.getElementById('errorText').textContent = message;
}

function resetUpload() {
    state.selectedImage = null;
    state.selectedFileName = '';
    state.currentResult = null;
    document.getElementById('imageInput').value = '';

    document.getElementById('uploadArea').style.display = 'block';
    document.getElementById('previewSection').style.display = 'none';
    document.getElementById('resultsSection').style.display = 'none';
    document.getElementById('loadingSection').style.display = 'none';
    document.getElementById('errorSection').style.display = 'none';
}

function dataURLToBlob(dataURL) {
    const parts = dataURL.split(',');
    const mimeMatch = parts[0].match(/:(.*?);/);
    const mime = mimeMatch ? mimeMatch[1] : 'image/jpeg';
    const bstr = atob(parts[1]);
    const n = bstr.length;
    const u8arr = new Uint8Array(n);

    for (let i = 0; i < n; i++) {
        u8arr[i] = bstr.charCodeAt(i);
    }

    return new Blob([u8arr], { type: mime });
}

function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({ behavior: 'smooth' });
    }
}

// ============================================================================
// REPORTING
// ============================================================================

function downloadReport() {
    if (!state.currentResult) {
        showError('No analysis result to download');
        return;
    }

    const result = state.currentResult;
    const timestamp = new Date().toLocaleString();

    // Create report content
    const report = `
SKIN CANCER DETECTION ANALYSIS REPORT
=====================================

Generated: ${timestamp}

ANALYSIS RESULTS
================
Prediction: ${result.prediction}
Confidence: ${(result.confidence * 100).toFixed(2)}%

CLASSIFICATION PROBABILITIES
=============================
Benign:    ${(result.probabilities.benign * 100).toFixed(2)}%
Malignant: ${(result.probabilities.malignant * 100).toFixed(2)}%

MEDICAL RECOMMENDATION
======================
${result.recommendation}

DISCLAIMER
==========
This report is generated by an AI system for informational purposes only.
It should NOT be used as a substitute for professional medical diagnosis.
Always consult a qualified dermatologist for accurate diagnosis and treatment.

System: SkinAI Detector v1.0
Model: MobileNetV2 Transfer Learning
Dataset: HAM10000
    `;

    // Create blob and download
    const blob = new Blob([report], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `skin_analysis_${new Date().getTime()}.txt`;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
}

// ============================================================================
// API CONNECTION CHECK
// ============================================================================

async function checkAPIConnection() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`, {
            method: 'GET'
        });

        if (response.ok) {
            console.log('✅ Connected to API successfully');
        } else {
            console.warn('⚠️ API responded with status:', response.status);
        }
    } catch (error) {
        console.warn('⚠️ Cannot connect to API at:', API_BASE_URL);
        console.warn('Make sure the backend server is running!');
        console.warn('Run: python backend/app.py');
    }
}

// ============================================================================
// ERROR HANDLING FOR REST OF APP
// ============================================================================

window.addEventListener('error', (event) => {
    console.error('Unhandled error:', event.error);
});

window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason);
});

"""
Skin Cancer Detection Model Training Script
Uses HAM10000 dataset with MobileNetV2 Transfer Learning
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# TensorFlow/Keras imports
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import cv2

# Set random seeds for reproducibility
np.random.seed(42)
tf.random.set_seed(42)

# ============================================================================
# CONFIGURATION
# ============================================================================

IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 15
VALIDATION_SPLIT = 0.2

# Model save path
MODEL_PATH = r'.\model\skin_cancer_model.h5'

# ============================================================================
# STEP 1: PREPARE HAM10000 DATASET
# ============================================================================

def download_ham10000():
    """
    Download HAM10000 dataset.
    ⚠️ Note: You need to:
    1. Download from: https://www.kaggle.com/datasets/kmader/skin-cancer-mnist-ham10000
    2. Place in: ./data/HAM10000/ folder
    3. Extract: ISIC2018_Task3_Training_Input.zip and ISIC2018_Task3_Training_GroundTruth.zip
    """
    print("=" * 70)
    print("📥 HAM10000 DATASET SETUP")
    print("=" * 70)
    print("\n⚠️  MANUAL SETUP REQUIRED:")
    print("1. Download from Kaggle: https://www.kaggle.com/datasets/kmader/skin-cancer-mnist-ham10000")
    print("2. Create folder: ./data/HAM10000/")
    print("3. Extract all files there")
    print("\nOr download from official source:")
    print("   https://www.kaggle.com/api/v1/datasets/download/kmader/skin-cancer-mnist-ham10000")
    print("\n" + "=" * 70 + "\n")


def create_sample_data():
    """
    Create sample data for demonstration if HAM10000 not available.
    This creates synthetic data for testing the pipeline.
    """
    print("⚠️  Creating sample synthetic data for demonstration...")
    
    data_dir = Path('./data/sample_data')
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Create sample images
    classes = ['benign', 'malignant']
    samples_per_class = 100
    
    for class_name in classes:
        class_dir = data_dir / class_name
        class_dir.mkdir(exist_ok=True)
        
        for i in range(samples_per_class):
            # Create random image
            img = np.random.randint(0, 256, (224, 224, 3), dtype=np.uint8)
            img_path = class_dir / f'image_{i}.jpg'
            cv2.imwrite(str(img_path), cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
    
    print(f"✅ Created {samples_per_class * len(classes)} sample images in ./data/sample_data/")
    return data_dir


def load_data():
    """
    Load HAM10000 dataset or sample data
    """
    print("\n" + "=" * 70)
    print("📂 LOADING DATASET")
    print("=" * 70)
    
    data_dir = Path('./data/HAM10000')
    
    if not data_dir.exists():
        print("\n❌ HAM10000 not found at ./data/HAM10000/")
        print("Using sample synthetic data instead...\n")
        data_dir = create_sample_data()
    
    # Load images and labels
    images = []
    labels = []
    
    for class_name in ['benign', 'malignant']:
        class_dir = data_dir / class_name
        if class_dir.exists():
            for img_file in class_dir.glob('*.jpg'):
                try:
                    img = cv2.imread(str(img_file))
                    if img is not None:
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
                        images.append(img)
                        labels.append(0 if class_name == 'benign' else 1)
                except Exception as e:
                    print(f"Error loading {img_file}: {e}")
    
    print(f"✅ Loaded {len(images)} images")
    print(f"   - Benign: {sum(1 for l in labels if l == 0)}")
    print(f"   - Malignant: {sum(1 for l in labels if l == 1)}")
    
    return np.array(images), np.array(labels)


# ============================================================================
# STEP 2: PREPROCESS DATA
# ============================================================================

def preprocess_data(images, labels):
    """
    Normalize images and split data
    """
    print("\n" + "=" * 70)
    print("🔧 PREPROCESSING DATA")
    print("=" * 70)
    
    # Normalize images to [0, 1]
    images = images.astype('float32') / 255.0
    
    # One-hot encode labels
    labels = keras.utils.to_categorical(labels, 2)
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        images, labels,
        test_size=0.2,
        random_state=42,
        stratify=np.argmax(labels, axis=1)
    )
    
    print(f"✅ Data preprocessed:")
    print(f"   - Training samples: {len(X_train)}")
    print(f"   - Test samples: {len(X_test)}")
    print(f"   - Image size: {IMG_SIZE}x{IMG_SIZE}")
    print(f"   - Normalization: [0, 1]")
    
    return X_train, X_test, y_train, y_test


# ============================================================================
# STEP 3: BUILD MODEL
# ============================================================================

def build_model():
    """
    Build MobileNetV2 transfer learning model
    """
    print("\n" + "=" * 70)
    print("🧠 BUILDING MODEL")
    print("=" * 70)
    
    # Load pre-trained MobileNetV2
    base_model = MobileNetV2(
        input_shape=(IMG_SIZE, IMG_SIZE, 3),
        include_top=False,
        weights='imagenet'
    )
    
    # Freeze base model weights
    base_model.trainable = False
    
    # Build custom head
    model = keras.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(64, activation='relu'),
        layers.Dropout(0.2),
        layers.Dense(2, activation='softmax')
    ])
    
    # Compile model
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    print("✅ Model built successfully")
    model.summary()
    
    return model, base_model


# ============================================================================
# STEP 4: DATA AUGMENTATION
# ============================================================================

def create_data_augmentation():
    """
    Create data augmentation pipeline
    """
    train_datagen = ImageDataGenerator(
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        zoom_range=0.2,
        fill_mode='nearest'
    )
    
    return train_datagen


# ============================================================================
# STEP 5: TRAIN MODEL
# ============================================================================

def train_model(model, base_model, X_train, X_test, y_train, y_test):
    """
    Train model with data augmentation
    """
    print("\n" + "=" * 70)
    print("🚀 TRAINING MODEL (Phase 1: Transfer Learning)")
    print("=" * 70)
    
    datagen = create_data_augmentation()
    
    # Phase 1: Train with frozen base model
    history1 = model.fit(
        datagen.flow(X_train, y_train, batch_size=BATCH_SIZE),
        epochs=EPOCHS // 2,
        validation_data=(X_test, y_test),
        steps_per_epoch=len(X_train) // BATCH_SIZE,
        verbose=1
    )
    
    # Phase 2: Fine-tune (unfreeze last layers)
    print("\n" + "=" * 70)
    print("🚀 TRAINING MODEL (Phase 2: Fine-tuning)")
    print("=" * 70)
    
    base_model.trainable = True
    
    # Freeze all but last 50 layers
    for layer in base_model.layers[:-50]:
        layer.trainable = False
    
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.0001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    history2 = model.fit(
        datagen.flow(X_train, y_train, batch_size=BATCH_SIZE),
        epochs=EPOCHS // 2,
        validation_data=(X_test, y_test),
        steps_per_epoch=len(X_train) // BATCH_SIZE,
        verbose=1
    )
    
    return history1, history2


# ============================================================================
# STEP 6: EVALUATE AND SAVE
# ============================================================================

def evaluate_and_save(model, X_test, y_test):
    """
    Evaluate model performance and save
    """
    print("\n" + "=" * 70)
    print("📊 EVALUATING MODEL")
    print("=" * 70)
    
    # Evaluate
    test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
    print(f"Test Loss: {test_loss:.4f}")
    print(f"Test Accuracy: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")
    
    # Save model
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    model.save(MODEL_PATH)
    print(f"\n✅ Model saved to: {MODEL_PATH}")


# ============================================================================
# MAIN TRAINING PIPELINE
# ============================================================================

if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("🏥 SKIN CANCER DETECTION MODEL - TRAINING PIPELINE")
    print("=" * 70)
    
    # Step 1: Download/Prepare dataset
    download_ham10000()
    
    # Step 2: Load data
    images, labels = load_data()
    
    # Step 3: Preprocess
    X_train, X_test, y_train, y_test = preprocess_data(images, labels)
    
    # Step 4: Build model
    model, base_model = build_model()
    
    # Step 5: Train model
    history1, history2 = train_model(model, base_model, X_train, X_test, y_train, y_test)
    
    # Step 6: Evaluate and save
    evaluate_and_save(model, X_test, y_test)
    
    print("\n" + "=" * 70)
    print("✅ TRAINING COMPLETE!")
    print("=" * 70)
    print(f"\n📦 Model saved at: {MODEL_PATH}")
    print("Next step: Run 'python backend/app.py' to start the Flask server")
    print("\n")

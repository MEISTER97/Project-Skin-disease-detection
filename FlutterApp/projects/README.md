# Skin Lesion Classifier App (Flutter)

This is a Flutter mobile application designed to help users identify whether a skin lesion is **benign** or **malignant**. The app allows users to upload or capture an image of a skin lesion, which is then analyzed by a machine learning model running on a Django backend 

## Features

- 📸 Capture an image with the camera or select from the gallery  
- ☁️ Upload the image to a Django backend  
- 🧠 Receive classification results (Benign or Malignant) 
- 🗂 View previous results 

## Backend

The app connects to a Django backend that handles:

- Image processing and model inference
- Classification using a ResNet-50 model trained on the **HAM10000** dataset

> 💡 The model is trained to distinguish between benign and malignant skin lesions.

## Getting Started

### Prerequisites

- Flutter SDK
- Android Studio / Xcode
- Backend running (Django API)

### Setup

1. Clone the repo:

```bash
git clone https://github.com/your-username/flutter-skin-lesion-app.git
cd flutter-skin-lesion-app

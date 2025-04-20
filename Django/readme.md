# Skin Lesion Classifier Backend (Django + ResNet-50)

This is a Django backend server for classifying skin lesions as **benign** or **malignant** using a trained **ResNet-50** deep learning model.

It serves both:

- 🌐 A web interface for uploading images manually
- 📱 A REST API endpoint to interact with a Flutter mobile app
- 📊 A page to view **all previously uploaded results**, whether submitted via web or mobile

---

## Features

- 🧠 Uses a trained **ResNet-50** model for binary classification
- 📤 Upload images via a web interface
- 🌐 RESTful API to receive image uploads from the Flutter app
- 🔁 Sends back predictions (benign or malignant) in JSON format
- 📂 View and track history of **all uploads and predictions**


## Getting Started

### Prerequisites

- Python 3.8+
- pip / virtualenv (recommended)
- PyTorch, torchvision, Pillow, Django, Django REST framework

### Setup

1. Clone the repo:

```bash
git clone https://github.com/your-username/django-skin-lesion-backend.git
cd django-skin-lesion-backend


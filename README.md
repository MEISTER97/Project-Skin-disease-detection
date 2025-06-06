# Skin Cancer Detection System

A complete full-stack project for **skin lesion classification (benign vs malignant)** using Deep Learning.  

The system consists of:

- 🧠 **Machine Learning** model trained in JupyterLab (ResNet-50, PyTorch)
- 🖥️ **Backend REST API** implemented in Django + Django REST Framework (DRF)
- 📱 **Mobile Frontend App** developed in Flutter
- 🗄️ **PostgreSQL database** to store user data and predictions

The project allows users to upload skin lesion images, receive predictions with Grad-CAM visual explanations, and track their history of uploaded images.

---

## 🚀 Features

- Skin lesion image classification (benign vs malignant)
- Grad-CAM visualization of predictions
- User authentication with JWT (Flutter)
- Secure image upload via API
- History of previous predictions (for authenticated users)
- Edge case handling (non-lesion images trigger "Unknown" result if confidence < threshold)

---

## 🗂️ Project Structure

/backend/ # Django REST API backend
/frontend/ # Flutter mobile app
/model-training/ # JupyterLab notebooks for model training & experiments
README.md # This file


---

## 🛠️ Tools and Technologies

- **Machine Learning:** PyTorch, TorchVision
- **Backend:** Django, Django REST Framework, PostgreSQL
- **Frontend:** Flutter (Dart)
- **Visualization:** Matplotlib, Seaborn, Grad-CAM
- **Experimentation:** JupyterLab

---

## ⚙️ Backend Setup

### 1. Clone the Repository

git clone https://github.com/MEISTER97/Project-Skin-disease-detection.git
cd skin-cancer-detector/backend

### 2. Set up PostgreSQL

CREATE DATABASE django_skin_lesion;
CREATE USER django_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE django_skin_lesion TO django_user;

### 3. Create .env File
DB_NAME=django_skin_lesion
DB_USER=django_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

### 4. Install Dependencies
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt


### 5. Apply Migrations
python manage.py migrate

### 6. Run Development Server
python manage.py runserver

http://localhost:8000/api/

---

##📱 Frontend (Flutter) Setup
cd ../frontend
flutter pub get
flutter run

Main Screens:
Sign_up_screen.dart: User signup

Sign_in_screen.dart: User sign in or guest login

Home.dart: Image capture/upload (available to all users), results history (only for authenticated users)

Result_screen.dart: Displays prediction and Grad-CAM

Previous_results_screen.dart: User's past results

---
## 📒 Model Training (JupyterLab)
Model training notebooks are in /model-training/.
Key notebook: Skin_lesion_classification.ipynb

Training Details:
Dataset: HAM10000 skin lesion dataset

Model: ResNet-50 pretrained + fine-tuned

Loss function: CrossEntropyLoss with class weights to handle imbalance

Optimizer: Adam with learning rate scheduling

Data augmentation: Flipping, rotation, normalization

Train-validation split: 80-20

Grad-CAM used to visualize model predictions

Results:
Accuracy: 88.03%

Precision: 67.47%

Recall: 74.50%

F1 Score: 70.81%
"We achieved an 88.03% prediction accuracy, which is quite decent. The model generalizes well on the validation set and shows good sensitivity (recall), which is important for medical diagnosis."

---
## 🧪 Edge Case Testing
To evaluate the model robustness, we tested it with 20+ out-of-distribution (OOD) images:
cars, animals, nature, and persons.

Testing Approach:
Added random OOD images to /model-training/ISIC-images/OOD_test_images/

Ran inference using a confidence threshold of 0.8

Images classified with confidence < threshold are returned as UNKNOWN

animal_image3.jpg -> UNKNOWN (Confidence: 0.78)
car_image2.jpg    -> UNKNOWN (Confidence: 0.56)
nature_image3.jpg -> UNKNOWN (Confidence: 0.72)
nature_image5.jpg -> UNKNOWN (Confidence: 0.55)

Observations:
CNN models like ResNet-50 do not inherently detect OOD images → threshold tuning is required.

Lowering the threshold to 0.8 improves robustness and helps avoid misclassification of random images.

---
## 🚧 Known Challenges
CNN models can be overconfident on OOD images → mitigated with threshold and future work could include adding explicit OOD training samples.

Dataset imbalance handled via class weights and augmentation.

Deployment complexity handled by converting PyTorch training code to efficient inference pipeline in Django backend.

Flutter-Django interaction handled securely via JWT authentication.

---
## 📬 Contact
Created by Man Tran
Feel free to reach out via: mantran1997@gmail.com
Or open an Issue on this GitHub repo if you have any questions or feedback.

## 📄 License
This project is for educational/research purposes.
Feel free to use it, improve it, and share your feedback!



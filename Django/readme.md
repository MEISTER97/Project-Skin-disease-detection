# Skin Lesion Classifier Backend (Django + ResNet-50)

This is a Django backend server for classifying skin lesions as **benign** or **malignant** using a trained **ResNet-50** deep learning model.

It serves both:

- 🌐 A web interface for uploading images manually  
- 📱 A REST API endpoint to interact with a Flutter mobile app  
- 📊 A page to view **all previously uploaded results**, whether submitted via web or mobile  

---

## 🚀 Features

- 🧠 Uses a trained **ResNet-50** model for binary classification  
- 📤 Upload images via a web interface  
- 🌐 RESTful API to receive image uploads from the Flutter app  
- 🔁 Sends back predictions (`benign` or `malignant`) in JSON format  
- 📂 View and track history of **all uploads and predictions**  
- 🛡️ **JWT Authentication** for mobile users (via Flutter app)  
- 🗄️ Stores user uploads & predictions in a **PostgreSQL** database  

---

## 🌐 Web Interface (Basic)

In addition to the REST API, this project provides a **basic HTML upload form** for manual testing.

### Pages:

- `/api/upload/` → Simple web form to upload an image (available for browser testing)
- `/api/upload/<n>/` → Result web page for the uploaded image (`n` = image ID)
- `/api/previous-results/` → List of all previous predictions by all users and guests 

### Notes:

- There is no full web front-end — the `/api/upload/` form is mainly for testing the API manually via browser.
- Predictions and history are synchronized with the mobile app and stored in the PostgreSQL database.
- Developers can also access the default Django admin panel at `/admin/` to view database records.


This allows both:
✅ Non-technical users to upload and view results via web  
✅ Admins to manage the system via the Django admin panel

---

## 🛠️ Getting Started

### Prerequisites

- Python 3.8+
- pip / virtualenv (recommended)
- PostgreSQL
- PyTorch, torchvision
- Pillow
- Django
- Django REST framework
- python-dotenv (to handle `.env` config)

---

## ⚙️ Setup

### 1️⃣ Clone the repo

```bash
git clone https://github.com/MEISTER97/Project-Skin-disease-detection.git
cd Project-Skin-disease-detection/django-skin-lesion-backend
```
---
2️⃣ Set up PostgreSQL
CREATE DATABASE django_skin_lesion;
CREATE USER django_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE django_skin_lesion TO django_user;

3️⃣ Create .env file
In the project root directory, create a .env file:
DB_NAME=django_skin_lesion
DB_USER=django_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=your_django_secret_key_here
DEBUG=True

4️⃣ Install dependencies
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

5️⃣ Apply migrations
python manage.py migrate

6️⃣ Run the development server
python manage.py runserver
Backend will be available at: http://localhost:8000



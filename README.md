Django Skin Lesion Classifier

A Django-based backend for skin lesion image classification. This project connects to a PostgreSQL database and uses environment variables for sensitive configuration.

🚀 Features

Image upload and classification

PostgreSQL database integration

Environment-based configuration for security

API endpoints for frontend/mobile integration

🛠️ Prerequisites

Before you begin, make sure you have the following installed:

Python 3.8+

pip

PostgreSQL

⚖️ Project Setup

1. Clone the repository

git clone https://github.com/MEISTER97/Project-Skin-disease-detection.git
cd Project-Skin-disease-detection

2. Set up PostgreSQL

Create a PostgreSQL database and user:

CREATE DATABASE django_skin_lesion;
CREATE USER django_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE django_skin_lesion TO django_user;

3. Create a .env file

In the root of the project (same level as manage.py), create a .env file and add:

DB_NAME=django_skin_lesion
DB_USER=django_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

4. Install dependencies

It's best to use a virtual environment:

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt


5. Apply migrations

python manage.py migrate

6. Run the development server

python manage.py runserver

You can now access the project at http://localhost:8000.

📁 Directory Structure

.
├── Django/               # Django project folder
│   ├── Django_api/       # Main app folder
│   ├── api/              # Your custom app
│   ├── manage.py
├── .env                  # Environment variables (DO NOT COMMIT)
├── .gitignore
├── requirements.txt
└── README.md

📬 Contact

Created by Man Tran. Feel free to reach out via mantran1997@gmail.com or GitHub Issues for questions or feedback.


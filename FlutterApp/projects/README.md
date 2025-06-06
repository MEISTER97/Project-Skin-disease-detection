# Skin Lesion Classifier - Flutter Mobile App

A Flutter mobile application for uploading skin lesion images and receiving **malignant / benign** predictions from a Django REST API backend.

The app allows users to:

- 📷 Capture or upload skin lesion images  
- 🔍 View prediction results + Grad-CAM heatmap  
- 🗂️ View history of their previous results (for authenticated users)  
- 🔐 Login / Sign up / Guest access  

---

## 🚀 Features

- 📱 Cross-platform mobile app (Android, iOS)
- 🔐 User authentication (Sign up / Login / Guest mode)
- 📷 Image capture from camera or image picker
- 📤 Upload images to the Django REST API backend
- 🔄 Display prediction result and Grad-CAM image
- 📂 View previous results (requires login)
- 🛡️ Handles **edge case images** → unknown result if model confidence is low

---

## 🛠️ Getting Started

### Prerequisites

- Flutter SDK (>= 3.10 recommended)
- Android Studio / Xcode / VS Code with Flutter plugin
- A running instance of your Django backend (see backend repo)

---

### Setup Instructions

1️⃣ Clone this repo:

```bash
git clone https://github.com/MEISTER97/Project-Skin-disease-detection/blob/main/FlutterApp/projects.git
cd flutter-skin-lesion-classifier
```
2️⃣ Install dependencies:
flutter pub get

3️⃣ Run the app:
flutter run

🔑 Authentication
User can sign up with email + password

User can sign in with email + password or continue as Guest

Only authenticated users can view previous results

Guests can still upload images and receive predictions but cannot save/view history


📡 API Integration
Upload endpoint: POST /api/upload/ → Receives image, returns prediction + Grad-CAM

Results endpoint: GET /api/results/ → Returns authenticated user’s previous results


📱 Main Screens
sign_up_screen.dart → User registration

sign_in_screen.dart → User login or guest access

home_screen.dart → Image upload / capture, displays upload button and navigation

result_screen.dart → Displays prediction result + Grad-CAM heatmap

previous_results_screen.dart → Displays user's past results (only for logged-in users)

🧪 Edge Case Handling
If model confidence < configured threshold (e.g. 0.8), the app will display:

UNKNOWN prediction with confidence %

This helps prevent random non-skin images (car, person, animal, etc.) from being wrongly classified as benign/malignant

🚧 Known Issues / Future Improvements
Currently optimized for Android (iOS works but needs more testing)

UI/UX improvements (dark mode, loading indicators, better Grad-CAM display)

Add password reset flow

Add profile screen for managing user details

📄 License
This project is for educational/research purposes.
Feel free to use it, improve it, and share your feedback!

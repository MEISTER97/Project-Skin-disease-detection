# 🧠 Skin Lesion Classification with ResNet-50

This directory contains a **Jupyter Notebook** implementing a deep learning model using **ResNet-50** for binary classification of skin lesion images — distinguishing between **malignant** and **benign** cases.

---

## 📊 Dataset

- **Name:** [HAM10000](https://api.isic-archive.com/collections/212/)
- **Source:** ISIC Archive  
- The dataset includes dermatoscopic images labeled by medical experts.  
- The data was split into **80% training** and **20% validation**.

---

## 🧪 Model Overview

- **Model:** ResNet-50 pretrained on ImageNet, fine-tuned
- **Framework:** PyTorch
- **Classification Labels:**
  - `0`: Benign
  - `1`: Malignant

---

## 📁 Contents

- `resnet50_skin_lesion_classification.ipynb`: Main notebook with data preprocessing, model building, training, and evaluation
- `resnet50_skin_lesion_classification.html`: Exported HTML version of the notebook for easy viewing
- `ISIC-images/OOD_test_images/`: Additional folder containing out-of-distribution (OOD) test images (cars, animals, nature, persons) for robustness testing

---

## 🧠 Features

- Data preprocessing from CSV metadata
- Data augmentation with torchvision transforms
- Class imbalance handling via `class_weights` in loss function
- Model training with Adam optimizer and learning rate scheduling
- Validation and model checkpoint saving
- Accuracy and loss visualization
- **Grad-CAM** visualization of model predictions for explainability
- **Edge Case Testing** with OOD images to test model robustness

---

## 🚀 How to Run

### 1️⃣ Clone the repo:

```bash
git clone https://github.com/MEISTER97/Project-Skin-disease-detection.git
cd Project-Skin-disease-detection/JupyterLab
```

## 2️⃣ Create and activate Python environment:
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

## 3️⃣ Install required packages:
pip install -r requirements.txt

## 4️⃣ Launch JupyterLab:
jupyter lab
Open the resnet50_skin_lesion_classification.ipynb notebook and run all cells.


## ✅ Results
Accuracy: 88.03%

Precision: 67.47%

Recall: 74.50%

F1 Score: 70.81%

We achieved an 88.03% prediction accuracy, which is quite decent. The model generalizes well on the validation set and shows good sensitivity (recall), which is important for medical diagnosis.

🧪 Edge Case (OOD) Testing
Tested the model with 20+ out-of-distribution (OOD) images (cars, animals, nature, persons).

Applied a confidence threshold of 0.8 to return UNKNOWN for uncertain predictions.

Results show that thresholding helps reduce misclassification of irrelevant images.


Example:
animal_image3.jpg → UNKNOWN (Confidence: 0.78)
car_image2.jpg    → UNKNOWN (Confidence: 0.56)
nature_image3.jpg → UNKNOWN (Confidence: 0.72)

## ⚠️ Known Challenges
CNN models can be overconfident on OOD images → mitigated using a confidence threshold.

Dataset imbalance handled via class weights and data augmentation.

Future improvement: training with explicit OOD class or rejection option.

📄 License
This project is for educational/research purposes.
Feel free to use, improve, and share your feedback!

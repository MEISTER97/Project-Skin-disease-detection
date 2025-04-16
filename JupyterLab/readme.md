# 🧠 Skin Lesion Classification with ResNet-50

This repository contains a **Jupyter Notebook** implementing a deep learning model using **ResNet-50** for binary classification of skin lesion images — distinguishing between **malignant** and **benign** cases.

## 📊 Dataset

- **Name:** [HAM10000](https://api.isic-archive.com/collections/212/)
- **Source:** ISIC Archive 
- The dataset includes dermatoscopic images labeled by medical experts.

## 🧪 Model Overview

- **Model:** ResNet-50 
- **Framework:** PyTorch
- **Classification Labels:**
  - `0`: Benign
  - `1`: Malignant

## 📁 Contents

- `resnet50_skin_lesion_classification.ipynb`: Main notebook with data preprocessing, model building, training, and evaluation
- `resnet50_skin_lesion_classification.html`: Exported HTML version of the notebook for easy viewing

## 🧠 Features

- Data preprocessing from CSV metadata
- Data augmentation with torchvision transforms
- Model training with Adam optimizer and learning rate scheduling
- Validation and best model checkpointing
- Accuracy and loss visualization

## 🚀 How to Run

1. Clone the repo:
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name

import os
import numpy as np
from PIL import Image
import torch.nn.functional as F
from torchvision import transforms
import cv2
import torchvision.models as models
from torchvision.models import ResNet50_Weights
from django.conf import settings


class GradCAM:
    def __init__(self, model):
        self.model = model
        self.features = None
        self.gradients = None

        # Register hook to get the features from the last convolutional layer
        def save_features(module, input, output):
            self.features = output

        # Register hook to get the gradients
        def save_gradients(module, grad_input, grad_output):
            self.gradients = grad_output[0]

        # last convolution layer is 'layer4' for ResNet-50
        self.model.layer4[2].register_forward_hook(save_features)
        self.model.layer4[2].register_full_backward_hook(save_gradients)


    def generate_cam(self, input_tensor, class_idx):
        # Make sure the model is in evaluation mode
        self.model.eval()

        # Perform a forward pass to get the output
        output = self.model(input_tensor)

        # Perform a backward pass to compute gradients w.r.t. the output class
        self.model.zero_grad()
        output[0, class_idx].backward(retain_graph=True)

        # Compute the weights of the feature maps (global average pooling)
        gradients = self.gradients.mean(dim=(2, 3), keepdim=True)
        weights = gradients.view(1, -1)

        # Compute the weighted sum of the feature maps
        weighted_feature_maps = self.features * weights.view(1, -1, 1, 1)
        cam = weighted_feature_maps.sum(dim=1, keepdim=True)

        # Apply ReLU to ensure that negative values are zeroed out
        cam = F.relu(cam)

        # Resize to match the input image size
        cam = cam.squeeze().cpu().detach().numpy()
        cam = cv2.resize(cam, (input_tensor.size(2), input_tensor.size(3)))

        # Normalize the cam between 0 and 1
        cam -= cam.min()
        cam /= cam.max()

        return cam


import torch


def load_model():
    # Use Django's BASE_DIR to correctly locate the model file
    model_path = os.path.join(settings.BASE_DIR, "model", "resnet50_custom_best.pth")

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")

    # Define the model architecture (ResNet-50 in this case)
    model = models.resnet50(weights=ResNet50_Weights.DEFAULT)

    # Modify the final fully connected layer to match the number of output classes (3 classes)
    model.fc = torch.nn.Linear(in_features=2048, out_features=3)

    # Load the model's state dict
    model.load_state_dict(torch.load(model_path, map_location=torch.device("cpu")))

    # Set the model to evaluation mode
    model.eval()

    return model


def process_image(image_file):
    # Load model
    model = load_model()

    # Preprocess the image
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    # Open image
    image = Image.open(image_file)
    input_tensor = transform(image).unsqueeze(0)  # Add batch dimension
    input_tensor.requires_grad_(True)  # Enable gradient computation

    # Forward pass
    output = model(input_tensor)
    probabilities = torch.nn.functional.softmax(output, dim=1)  # Get softmax probabilities
    confidence, predicted = torch.max(probabilities, 1)  # Get max probability and index

    # Confidence and predicted class
    confidence_percentage = confidence.item() * 100
    class_labels = ['nevus', 'melanoma', 'other lesion']
    predicted_class = class_labels[predicted.item()]

    # uncertain prediction lower than 70%
    if confidence_percentage<70:
        predicted_class="Uncertain prediction"

    # Generate Grad-CAM heatmap
    grad_cam = GradCAM(model=model)
    cam = grad_cam.generate_cam(input_tensor, predicted.item())  # Pass the predicted class index

    # Convert image to numpy and normalize Grad-CAM heatmap
    image_np = np.array(image.resize((224, 224)))
    cam = np.squeeze(cam)
    cam = cam - np.min(cam)  # Normalize
    cam = cam / np.max(cam)
    cam = np.uint8(255 * cam)  # Scale to [0, 255]

    # Overlay heatmap on image
    heatmap = cv2.applyColorMap(cam, cv2.COLORMAP_JET)
    superimposed_img = cv2.addWeighted(image_np, 0.6, heatmap, 0.4, 0)

    return predicted_class, confidence_percentage, superimposed_img


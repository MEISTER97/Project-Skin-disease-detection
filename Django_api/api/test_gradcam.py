import matplotlib.pyplot as plt
from Django_api.api.model_processing import process_image  # Import the function you wrote

# Test the Grad-CAM process
def test_gradcam(image_path):
    predicted_class, confidence_percentage, superimposed_img = process_image(image_path)

    # Print results
    print(f"Predicted Class: {predicted_class}")
    print(f"Confidence: {confidence_percentage:.2f}%")

    # Show the Grad-CAM overlayed image
    plt.imshow(superimposed_img)
    plt.axis('off')  # Hide axes for better visualization
    plt.show()

# Test with your image file
image_path = r'E:\afeka\finalProject\JupyterLab\images_ToTest\images\ISIC_2175344.jpg'
test_gradcam(image_path)

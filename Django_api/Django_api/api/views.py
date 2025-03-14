import cv2
from django.shortcuts import render
from django.http import JsonResponse
from .forms import ImageUploadForm
from django.core.files.storage import FileSystemStorage
from .models import ImagePrediction
import os
from django.conf import settings
from django.shortcuts import render, redirect,get_object_or_404
from django.http import JsonResponse
from .forms import ImageUploadForm
from .model_processing import process_image

def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_instance = form.save()  # Save the uploaded image

            # Get the path to the saved image
            image_path = image_instance.image.path

            # Process the image through the model
            predicted_class, confidence_percentage, superimposed_img = process_image(image_path)

            # Store the results in the model
            image_instance.result = predicted_class
            image_instance.confidence = confidence_percentage
            image_instance.save()

            # Save the result image
            result_img_path = os.path.join(settings.MEDIA_ROOT, 'result_images', f"{image_instance.id}_result.jpg")
            os.makedirs(os.path.dirname(result_img_path), exist_ok=True)
            cv2.imwrite(result_img_path, superimposed_img)

            # Redirect to result page
            return redirect("upload_success_view", prediction_id=image_instance.id)

    else:
        form = ImageUploadForm()

    return render(request, 'api/upload_image.html', {'form': form})


def upload_success_view(request, prediction_id):
    prediction = get_object_or_404(ImagePrediction, id=prediction_id)

    result_image_url = f"/media/result_images/{prediction.id}_result.jpg"

    context = {
        "result": prediction.result,
        "confidence": round(prediction.confidence, 2),
        "image_url": prediction.image.url,
        "result_image_url": result_image_url,  # Correctly construct result image path
    }

    return render(request, "api/result.html", context)
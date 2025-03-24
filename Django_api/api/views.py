import cv2
from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings
from django.shortcuts import render, redirect,get_object_or_404
from .forms import ImageUploadForm
from .model_processing import process_image
from .models import PredictionResult

def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the uploaded image
            image_instance = form.save()

            # Get the path to the saved image
            image_path = image_instance.image.path

            # Process the image through the model (you'll define process_image to handle this)
            predicted_class, confidence_percentage, superimposed_img = process_image(image_path)

            # Create a PredictionResult instance and store the results
            prediction_result = PredictionResult(
                image=image_instance.image,
                prediction=predicted_class,
                confidence=confidence_percentage
            )
            prediction_result.save()  # Save the prediction result

            # Save the result image
            result_img_path = os.path.join(settings.MEDIA_ROOT, 'result_images', f"{prediction_result.id}_result.jpg")

            os.makedirs(os.path.dirname(result_img_path), exist_ok=True)
            cv2.imwrite(result_img_path, superimposed_img)

            # Redirect to result page with the correct ID
            return redirect("upload_success_view", prediction_id=prediction_result.id)

    else:
        form = ImageUploadForm()

    return render(request, 'api/upload_image.html', {'form': form})


def upload_success_view(request, prediction_id):
    prediction_result = get_object_or_404(PredictionResult, id=prediction_id)

    # Round confidence to 2 decimal places
    rounded_confidence = round(prediction_result.confidence, 2)

    result_image_url = f"{settings.MEDIA_URL}result_images/{prediction_result.id}_result.jpg"

    context = {
        "result": prediction_result.prediction,
        "confidence": rounded_confidence,
        "image_url": prediction_result.image.url,
        "result_image_url": result_image_url,
    }

    return render(request, "api/result.html", context)


def previous_results(request):
    # Fetch all results ordered by date, most recent first
    results = PredictionResult.objects.all().order_by('-created_at')  # Order by date to show the latest first

    # Pass MEDIA_URL to the template for constructing image URLs
    context = {
        "results": results,
        "MEDIA_URL": settings.MEDIA_URL,  # Pass MEDIA_URL to use it in the template
    }

    return render(request, 'api/previous_results.html', context)
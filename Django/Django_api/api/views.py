import cv2
import os
from django.conf import settings
from django.shortcuts import render, redirect,get_object_or_404
from django.views.decorators.http import require_POST

from .forms import ImageUploadForm
from .model_processing import process_image
from .models import PredictionResult
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .serializers import RegisterSerializer
from rest_framework import status
from rest_framework.response import Response

def get_next_image_number():
    """Find the next available image number in 'images' folder."""
    images_dir = os.path.join(settings.MEDIA_ROOT, 'images')
    os.makedirs(images_dir, exist_ok=True)

    existing_files = [f for f in os.listdir(images_dir) if
                      f.startswith("image_") and f.lower().endswith((".jpg", ".jpeg", ".png"))]
    numbers = [int(f.split('_')[1].split('.')[0]) for f in existing_files if f.split('_')[1].split('.')[0].isdigit()]

    next_number = max(numbers) + 1 if numbers else 1
    return f"image_{next_number}.jpg"

# upload an image from flutter
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def upload_image_api(request):
    if request.method == 'POST' and request.headers.get('X-Request-Source') == 'flutter':
        if request.FILES.get('image'):
            image = request.FILES['image']
            image_name = get_next_image_number()
            image_path = os.path.join(settings.MEDIA_ROOT, 'images', image_name)

            with open(image_path, 'wb') as f:
                f.write(image.read())

            predicted_class, confidence_percentage, superimposed_img = process_image(image_path)

            prediction_result = PredictionResult.objects.create(
                image=f'images/{image_name}',
                prediction=predicted_class,
                confidence=confidence_percentage
            )

            result_image_name = f"result_{prediction_result.id}.jpg"
            result_image_path = os.path.join(settings.MEDIA_ROOT, 'result_images', result_image_name)
            os.makedirs(os.path.dirname(result_image_path), exist_ok=True)
            cv2.imwrite(result_image_path, superimposed_img)

            prediction_result.result_image = f'result_images/{result_image_name}'
            prediction_result.save()

            return JsonResponse({
                "prediction": predicted_class,
                "confidence": round(confidence_percentage, 2),
                "image_url": request.build_absolute_uri(settings.MEDIA_URL + prediction_result.image.name),
                "result_image_url": request.build_absolute_uri(settings.MEDIA_URL + prediction_result.result_image.name),
                "result_image_width": superimposed_img.shape[1],
                "result_image_height": superimposed_img.shape[0]
            }, status=200)

        return JsonResponse({"error": "No image provided"}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)



def upload_image_web(request):
    form = ImageUploadForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        image_instance = form.save()

        new_image_name = get_next_image_number()
        new_image_path = os.path.join(settings.MEDIA_ROOT, 'images', new_image_name)
        os.rename(image_instance.image.path, new_image_path)

        predicted_class, confidence_percentage, superimposed_img = process_image(new_image_path)

        prediction_result = PredictionResult.objects.create(
            image=f'images/{new_image_name}',
            prediction=predicted_class,
            confidence=confidence_percentage
        )

        result_image_name = f"result_{prediction_result.id}.jpg"
        result_img_path = os.path.join(settings.MEDIA_ROOT, 'result_images', result_image_name)
        os.makedirs(os.path.dirname(result_img_path), exist_ok=True)
        cv2.imwrite(result_img_path, superimposed_img)

        prediction_result.result_image = f'result_images/{result_image_name}'
        prediction_result.save()

        return redirect("upload_success_view", prediction_id=prediction_result.id)

    return render(request, 'api/upload_image.html', {'form': form})


def upload_success_view(request, prediction_id):
    prediction_result = get_object_or_404(PredictionResult, id=prediction_id)

    # Round confidence to 2 decimal places
    rounded_confidence = round(prediction_result.confidence, 2)

    result_image_name = f"result_{prediction_result.id}.jpg"
    result_image_url = f"{settings.MEDIA_URL}result_images/{result_image_name}"

    context = {
        "result": prediction_result.prediction,
        "confidence": rounded_confidence,
        "image_url": prediction_result.image.url,
        "result_image_url": result_image_url,
    }
    return render(request, "api/result.html", context)

# return results to flutter
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_previous_results_api(request):
    # Check if the request is from Flutter for previous results
    if request.headers.get('X-Request-Source') == 'flutter_previous_results':
        results = PredictionResult.objects.order_by('-created_at')[:10]  # Get last 10 results
        results_data = []

        for result in results:
            results_data.append({
                "prediction": result.prediction,
                "confidence": result.confidence,
                "image_url": request.build_absolute_uri(result.image.url),
                "result_image_url": request.build_absolute_uri(result.result_image.url) if result.result_image else None
            })

        return JsonResponse({"results": results_data}, status=200)

    return JsonResponse({"error": "Invalid request"}, status=400)


#return results to web
def previous_results(request):
    # Fetch all results ordered by date, most recent first
    results = PredictionResult.objects.all().order_by('-created_at')

    # Add the result image URL for each result
    for result in results:
        result.result_image_url = f"{settings.MEDIA_URL}result_images/{result.id}_result.jpg"

    # Pass MEDIA_URL to the template for constructing image URLs
    context = {
        "results": results,
        "MEDIA_URL": settings.MEDIA_URL,  # Pass MEDIA_URL to use it in the template
    }

    return render(request, 'api/previous_results.html', context)


#register a user from flutter(sign up)
@api_view(['POST'])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({'message': 'User registered successfully'}, status=201)
    return JsonResponse(serializer.errors, status=400)



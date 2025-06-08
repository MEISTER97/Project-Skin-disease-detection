import cv2
import os
from django.conf import settings
from django.shortcuts import render, redirect,get_object_or_404
from rest_framework.permissions import AllowAny

from .forms import ImageUploadForm
from .model_processing import process_image
from .models import PredictionResult
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterSerializer
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa

#determines the next available image filename in the 'images' folder under MEDIA_ROOT.
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
@permission_classes([AllowAny])  # Allow access to any user, authenticated or not
@csrf_exempt
def upload_image_api(request):
    # Check for POST request from Flutter client
    if request.method == 'POST' and request.headers.get('X-Request-Source') == 'flutter':

        # Ensure an image file is provided in the request
        if request.FILES.get('image'):
            image = request.FILES['image']

            # Generate a unique name and path to store the image
            image_name = get_next_image_number()
            image_path = os.path.join(settings.MEDIA_ROOT, 'images', image_name)

            # Save the uploaded image to the local filesystem
            with open(image_path, 'wb') as f:
                f.write(image.read())

            # Run prediction and generate Grad-CAM result
            predicted_class, confidence_percentage, superimposed_img = process_image(image_path)

            # Save prediction result in the database
            prediction_result = PredictionResult.objects.create(
                user=request.user if request.user.is_authenticated else None,
                image=f'images/{image_name}',
                prediction=predicted_class,
                confidence=confidence_percentage
            )

            # Save the result (Grad-CAM) image
            result_image_name = f"result_{prediction_result.id}.jpg"
            result_image_path = os.path.join(settings.MEDIA_ROOT, 'result_images', result_image_name)
            os.makedirs(os.path.dirname(result_image_path), exist_ok=True)
            cv2.imwrite(result_image_path, superimposed_img)

            # Update the database record with result image path
            prediction_result.result_image = f'result_images/{result_image_name}'
            prediction_result.save()

            # Return prediction data and image URLs
            return JsonResponse({
                "prediction": predicted_class,
                "confidence": round(confidence_percentage, 2),
                "image_url": request.build_absolute_uri(settings.MEDIA_URL + prediction_result.image.name),
                "result_image_url": request.build_absolute_uri(
                    settings.MEDIA_URL + prediction_result.result_image.name),
                "result_image_width": superimposed_img.shape[1],
                "result_image_height": superimposed_img.shape[0]
            }, status=200)

        # If no image is found in the request
        return JsonResponse({"error": "No image provided"}, status=400)

    # If the request is not a valid Flutter POST
    return JsonResponse({"error": "Invalid request"}, status=400)


# upload an image from web and check if image valid
def upload_image_web(request):
    # Initialize the image upload form (handles both GET and POST data)
    form = ImageUploadForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if form.is_valid():
            # Save the uploaded image instance
            image_instance = form.save()

            # Generate a unique name and move the uploaded file to 'images/' with the new name
            new_image_name = get_next_image_number()
            new_image_path = os.path.join(settings.MEDIA_ROOT, 'images', new_image_name)
            os.rename(image_instance.image.path, new_image_path)

            # Run prediction and generate Grad-CAM overlay
            predicted_class, confidence_percentage, superimposed_img = process_image(new_image_path)

            # Save prediction result to the database
            prediction_result = PredictionResult.objects.create(
                image=f'images/{new_image_name}',
                prediction=predicted_class,
                confidence=confidence_percentage
            )

            # Save the Grad-CAM result image
            result_image_name = f"result_{prediction_result.id}.jpg"
            result_img_path = os.path.join(settings.MEDIA_ROOT, 'result_images', result_image_name)
            os.makedirs(os.path.dirname(result_img_path), exist_ok=True)
            cv2.imwrite(result_img_path, superimposed_img)

            # Update the database entry with result image path
            prediction_result.result_image = f'result_images/{result_image_name}'
            prediction_result.save()

            # Redirect to a page showing the prediction result
            return redirect("upload_success_view", prediction_id=prediction_result.id)

    # Render the image upload form
    return render(request, 'api/upload_image.html', {'form': form})


# After a successful upload, this view fetches the result associated with the uploaded image
def upload_success_view(request, prediction_id):
    # Retrieve the prediction result or return 404 if not found
    prediction_result = get_object_or_404(PredictionResult, id=prediction_id)

    # Round the confidence score to 2 decimal places for display
    rounded_confidence = round(prediction_result.confidence, 2)

    # Construct the result image filename and URL
    result_image_name = f"result_{prediction_result.id}.jpg"
    result_image_url = f"{settings.MEDIA_URL}result_images/{result_image_name}"

    # Prepare context data for the template
    context = {
        "result": prediction_result.prediction,
        "confidence": rounded_confidence,
        "image_url": prediction_result.image.url,
        "result_image_url": result_image_url,
    }

    # Render the result template with prediction details
    return render(request, "api/result.html", context)

# Return results to `flutter`
@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Require user to be authenticated
def get_previous_results_api(request):
    # Check if the request is coming from the Flutter app (for previous results)
    if request.headers.get('X-Request-Source') == 'flutter_previous_results':
        # Fetch the 10 most recent prediction results for the user
        results = PredictionResult.objects.filter(user=request.user).order_by('-created_at')[:10]

        results_data = []

        for result in results:
            results_data.append({
                "prediction": result.prediction,
                "confidence": result.confidence,
                "image_url": request.build_absolute_uri(result.image.url),
                "result_image_url": request.build_absolute_uri(result.result_image.url) if result.result_image else None
            })

        # Return the results as JSON
        return JsonResponse({"results": results_data}, status=200)

    # Return error if the request is not valid
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


# Register a user from Flutter (sign up)
@api_view(['POST'])
@permission_classes([AllowAny])  # Allow access to unauthenticated users
def register_user(request):
    # Deserialize and validate the incoming registration data
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        # Save the user if data is valid
        serializer.save()
        return JsonResponse({'message': 'User registered successfully'}, status=201)

    # If validation fails, return the errors
    return JsonResponse(serializer.errors, status=400)


def download_result_pdf(request, prediction_id):
    # Retrieve the prediction result or return 404 if not found
    result = get_object_or_404(PredictionResult, id=prediction_id)
    context = {'result': result}

    # Define the path to the HTML template for rendering the PDF
    template_path = 'api/single_result.html'

    # Prepare the HTTP response with PDF content type
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="result_{prediction_id}.pdf"'

    # Render HTML from template with context data
    template = get_template(template_path)
    html = template.render(context)

    # Generate the PDF using WeasyPrint or xhtml2pdf (pisa)
    pisa_status = pisa.CreatePDF(html, dest=response)

    # Return error if PDF generation fails
    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=500)

    # Return the generated PDF as response
    return response


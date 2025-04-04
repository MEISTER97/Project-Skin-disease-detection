from django.db import models

class ImagePrediction(models.Model):
    image = models.ImageField(upload_to='images/')  # Save the uploaded image
    result = models.CharField(max_length=255, blank=True, null=True)  # Store the result from the model
    confidence = models.FloatField(blank=True, null=True)  # Store confidence if needed
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.result} ({self.confidence}%)"


class PredictionResult(models.Model):
    image = models.ImageField(upload_to='images/')
    prediction = models.CharField(max_length=100)
    confidence = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    result_image = models.ImageField(upload_to='result_images/', null=True, blank=True)

    def __str__(self):
        return f"{self.image.name} - {self.prediction} ({self.confidence}%)"

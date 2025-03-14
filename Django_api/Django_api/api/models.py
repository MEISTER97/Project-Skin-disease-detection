from django.db import models

class ImagePrediction(models.Model):
    image = models.ImageField(upload_to='images/')  # Save the uploaded image
    result = models.CharField(max_length=255, blank=True, null=True)  # Store the result from the model
    confidence = models.FloatField(blank=True, null=True)  # Store confidence if needed
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.predicted_class} ({self.confidence}%)"
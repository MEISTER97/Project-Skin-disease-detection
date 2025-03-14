from django import forms
from .models import ImagePrediction

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImagePrediction
        fields = ['image']

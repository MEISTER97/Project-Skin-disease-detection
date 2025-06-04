from django import forms
from .models import ImagePrediction

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImagePrediction
        fields = ['image']

    def clean_image(self):
        image = self.cleaned_data.get('image')
        valid_extensions = ['.jpg', '.jpeg', '.png']
        ext = image.name.lower().split('.')[-1]
        if f'.{ext}' not in valid_extensions:
            raise forms.ValidationError("Only JPG, JPEG, and PNG files are allowed.")
        return image
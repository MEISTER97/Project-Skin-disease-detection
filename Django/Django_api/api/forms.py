from django import forms
from .models import ImagePrediction

from django import forms

class ImageUploadForm(forms.ModelForm):
    """
    Form for uploading an image file linked to the ImagePrediction model.
    Ensures that only images with valid extensions are accepted.
    """

    class Meta:
        model = ImagePrediction
        fields = ['image']

    def clean_image(self):
        """
        Validates the uploaded image file to ensure it has an allowed extension.
        Allowed extensions are: .jpg, .jpeg, .png.
        Raises a ValidationError if the file extension is invalid.
        """
        image = self.cleaned_data.get('image')
        valid_extensions = ['.jpg', '.jpeg', '.png']
        ext = image.name.lower().split('.')[-1]
        if f'.{ext}' not in valid_extensions:
            raise forms.ValidationError("Only JPG, JPEG, and PNG files are allowed.")
        return image

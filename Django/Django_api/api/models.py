from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class ImagePrediction(models.Model):
    image = models.ImageField(upload_to='images/')  # Save the uploaded image
    result = models.CharField(max_length=255, blank=True, null=True)  # Store the result from the model
    confidence = models.FloatField(blank=True, null=True)  # Store confidence if needed
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.result} ({self.confidence}%)"


class PredictionResult(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='predictions',
        null=True,
        blank=True
    )
    image = models.ImageField(upload_to='images/')
    result_image = models.ImageField(upload_to='result_images/', null=True, blank=True)
    prediction = models.CharField(max_length=100)
    confidence = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.image.name} - {self.prediction} ({self.confidence}%)"


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # No username or other required fields

    def __str__(self):
        return self.email
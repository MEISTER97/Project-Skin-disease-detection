from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

#This model stores uploaded images and their associated predictions
class ImagePrediction(models.Model):
    image = models.ImageField(upload_to='images/')  # Save the uploaded image
    result = models.CharField(max_length=255, blank=True, null=True)  # Store the result from the model
    confidence = models.FloatField(blank=True, null=True)  # Store confidence if needed
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.result} ({self.confidence}%)"

# Stores uploaded image, prediction, Grad-CAM result, user reference, and confidence score into the desire folders.
#store them also into the database
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


"""
Custom user manager to handle user creation using email instead of username.
Includes methods for creating both regular users and superusers.
"""
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a regular user with the given email and password.
        """
        if not email:
            raise ValueError("Email is required")

        # Normalize the email address by lowercasing the domain part
        email = self.normalize_email(email)

        # Create user instance without saving to the database yet
        user = self.model(email=email, **extra_fields)

        # Set the user password (handles hashing)
        user.set_password(password)

        # Save the user to the database
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        Automatically sets `is_staff` and `is_superuser` to True.
        """
        # Ensure required superuser flags are set
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)

# Replaces Django’s default user model to support email-only login
class CustomUser(AbstractBaseUser, PermissionsMixin):
    # Unique email address used for authentication
    email = models.EmailField(unique=True)

    # Indicates whether this user account is active
    is_active = models.BooleanField(default=True)

    # Designates whether the user can access the admin site
    is_staff = models.BooleanField(default=False)

    # Link to the custom manager that handles user creation
    objects = CustomUserManager()

    # Use email instead of username for login
    USERNAME_FIELD = 'email'

    # No additional required fields on user creation
    REQUIRED_FIELDS = []

    def __str__(self):
        # Return the email as the string representation of the user
        return self.email

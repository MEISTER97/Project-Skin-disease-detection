from django.urls import path
from .views import upload_image, upload_success_view
from . import views

urlpatterns = [
    path('upload/', views.upload_image, name='upload_image'),
    path("upload/success/<int:prediction_id>/", upload_success_view, name="upload_success_view"),
]

from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('upload/', views.upload_image, name='upload_image'),
    path("upload/success/<int:prediction_id>/", views.upload_success_view, name="upload_success_view"),
    path('previous-results/', views.previous_results, name='previous_results'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

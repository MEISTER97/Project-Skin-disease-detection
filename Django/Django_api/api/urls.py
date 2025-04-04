from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
# Regular views (web-based upload)
    path('upload/', views.upload_image_web, name='upload_image'),
    path("upload/success/<int:prediction_id>/", views.upload_success_view, name="upload_success_view"),
    path('previous-results/', views.previous_results, name='web_previous_results'),
    
# API views (API-based upload and result)
    path('flutter_upload/', views.upload_image_api, name='flutter_upload'),
    path('flutter_results/', views.get_previous_results_api, name='flutter_results'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

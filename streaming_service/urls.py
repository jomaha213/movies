import os  # <-- DODAJ TO
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('movies.urls')),
]

if settings.DEBUG and not os.environ.get('CLOUDINARY_CLOUD_NAME'):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
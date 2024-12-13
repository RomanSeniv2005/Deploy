from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('frontend.urls')),
    path('admin/', admin.site.urls),  # Адмін панель
    path('', include('bookings.urls')),  # Підключення API з додатку bookings
]

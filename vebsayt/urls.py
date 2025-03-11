from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('sayt.urls')),  # APP ichidagi urls.py ni qo'shib olish
]

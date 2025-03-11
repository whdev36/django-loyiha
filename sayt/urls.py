from django.urls import path
from . import views

urlpatterns = [
    path('', views.bosh_sahifa, name='bosh-sahifa'),  # Bosh sahifa uchun yo'l
]
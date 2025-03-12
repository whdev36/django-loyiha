from django.shortcuts import render
from django.contrib import messages
from .models import Mahsulot

# Bosh sahifa uchun funksiya yaratish
def bosh_sahifa(request):
    mahsulotlar = Mahsulot.objects.all()
    return render(request, 'bosh-sahifa.html', {'mahsulotlar': mahsulotlar})

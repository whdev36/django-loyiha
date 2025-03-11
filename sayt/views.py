from django.shortcuts import render

# Bosh sahifa uchun funksiya yaratish
def bosh_sahifa(request):
    return render(request, 'bosh-sahifa.html', {})

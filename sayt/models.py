from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser

# Modellarni yaratish

# Hisob uchun model
class Hisob(AbstractUser):
    class Meta:
        verbose_name = 'Hisob'
        verbose_name_plural = 'Hisoblar'
    
    telefon_raqam = models.CharField(blank=True, max_length=20, null=True)
    profil_rasm = models.ImageField(upload_to='hisoblar/', blank=True, null=True)
    
    def __str__(self):
        return self.username

# Turkum uchun model
class Turkum(models.Model):
    class Meta:
        verbose_name = 'Turkum'
        verbose_name_plural = 'Turkumlar'

    nom = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(blank=True, unique=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom.lower())  # NOM maydonini slug formatiga o'tkazish
        super().save()  # Asosiy save metodini chaqirish

    def __str__(self):
        return self.nom
    
# Mahsulot uchun model
class Mahsulot(models.Model):
    class Meta:
        verbose_name = 'Mahsulot'
        verbose_name_plural = 'Mahsulotlar'

    nom = models.CharField(max_length=255)
    turkum = models.ForeignKey(Turkum, on_delete=models.CASCADE)
    narx = models.DecimalField(max_digits=10, decimal_places=2)
    rasm = models.ImageField(upload_to='mahsulotlar/')
    tavsif = models.TextField(blank=True)

    def __str__(self):
        return self.nom
    
# Buyurtma uchun model
class Buyurtma(models.Model):
    class Meta:
        verbose_name = 'Buyurtma'
        verbose_name_plural = 'Buyurtmalar'
    
    hisob = models.ForeignKey(Hisob, on_delete=models.CASCADE)
    mahsulot = models.ManyToManyField(Mahsulot)
    umumiy_narx = models.DecimalField(max_digits=10, decimal_places=2)
    da_yaratilgan = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Buyurtma {self.id} - {self.hisob.username}'
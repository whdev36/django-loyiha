from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser

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
        super().save(*args, **kwargs)  # Asosiy save metodini chaqirish

    def __str__(self):
        return self.nom

# Mahsulot uchun model
class Mahsulot(models.Model):
    class Meta:
        verbose_name = 'Mahsulot'
        verbose_name_plural = 'Mahsulotlar'

    nom = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, unique=True, null=True)
    turkum = models.ForeignKey(Turkum, on_delete=models.CASCADE)
    narx = models.DecimalField(max_digits=10, decimal_places=2)
    rasm = models.ImageField(upload_to='mahsulotlar/', blank=True, null=True)
    tavsif = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom.lower())  # Mahsulot nomidan slug yaratish
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom

# Buyurtma uchun model
class Buyurtma(models.Model):
    STATUSLAR = (
        ('yangi', 'Yangi'),
        ('tasdiqlangan', 'Tasdiqlangan'),
        ('yetkazilgan', 'Yetkazilgan'),
        ('bekor', 'Bekor qilingan'),
    )

    class Meta:
        verbose_name = 'Buyurtma'
        verbose_name_plural = 'Buyurtmalar'
    
    hisob = models.ForeignKey(Hisob, on_delete=models.CASCADE)
    mahsulot = models.ManyToManyField(Mahsulot)
    umumiy_narx = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    da_yaratilgan = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUSLAR, default='yangi')

    def save(self, *args, **kwargs):
        # Umumiy narxni avtomatik hisoblash
        self.umumiy_narx = sum(mahsulot.narx for mahsulot in self.mahsulot.all())
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Buyurtma {self.id} - {self.hisob.username} ({self.status})'

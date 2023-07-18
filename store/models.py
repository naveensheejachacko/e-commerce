from django.db import models

from categories.models import Product

# Create your models here.
class Banners(models.Model):
    image = models.ImageField(upload_to="banners", blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    alt_text = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.alt_text

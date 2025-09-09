import uuid
from django.db import models

# Create your models here.
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('jersey', 'Jersey'),
        ('jaket', 'Jaket'),
        ('sepatu', 'Sepatu Bola'),
        ('kaus_kaki', 'Kaus Kaki'),
        ('aksesoris', 'Aksesoris'),
        ('celana', 'Celana'),
    ]
    
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    thumbnail = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='jersey')
    is_featured = models.BooleanField(default=False)
    brand = models.CharField(max_length=20, blank=True)
    stock = models.PositiveIntegerField(default=0)
    sales_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
        
    def __str__(self):
        return self.name
    
    @property
    def is_best_seller(self):
        return self.sales_count > 250
    
    def increment_sales_count(self):
        self.sales_count += 1
        self.save()
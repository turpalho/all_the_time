from django.db import models
from django.conf import settings

from .services.model_abstracts import Model


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Store(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Store"
        verbose_name_plural = "Stores"

    def __str__(self):
        return self.name


class Receipt(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   on_delete=models.CASCADE)
    store = models.ForeignKey("Store", related_name='receipts', on_delete=models.CASCADE)
    category = models.ForeignKey("Category", related_name='receipts', on_delete=models.PROTECT)
    total_sum = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Receipt"
        verbose_name_plural = "Receipts"

    def __str__(self):
        return self.pk


class Product(models.Model):
    receipt = models.ForeignKey("Receipt", related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    count = models.BigIntegerField()
    total_sum = models.DecimalField(max_digits=10, decimal_places=2)
    is_weighed_out = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name

from django.db import models
from django.contrib.auth.models import User,Group

class Category(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
# Create your models here.
class InventoryItems(models.Model):
    name = models.CharField(max_length=200)
    quantity = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class StockMovement(models.Model):
    inventory_item = models.ForeignKey(InventoryItems, on_delete=models.CASCADE)
    change = models.IntegerField()  # Positive for add, negative for remove
    date = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=255)  # Reason for the stock change (e.g., "Stock added", "Stock removed")

    def __str__(self):
        return f"{self.inventory_item.name} - {self.change} on {self.date}"


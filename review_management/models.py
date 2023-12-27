from django.db import models
from products.models import ProductVariant
from user_side.models import NewUser

class review(models.Model):
    review = models.TextField(max_length = 1000, blank=True, null=True)
    stars = models.IntegerField(null=True, blank=True)
    product = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='reviews')
    customer = models.ForeignKey(NewUser, on_delete=models.SET_NULL, null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)

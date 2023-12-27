from django.db import models
from order_management.models import OrderItem
from order_management.models import Payment

from user_side.models import NewUser

# Create your models here.
class SeamPay(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, default=0.0)
    updated_at = models.DateTimeField(auto_now_add=True)


class Wallet(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, blank=True, null=True)
    order_id = models.CharField(max_length=250, blank=True, null=True)
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, null=True, blank=True)
    is_debit = models.BooleanField(default=False)
    seampay = models.ForeignKey(SeamPay, on_delete=models.CASCADE, blank=True, null=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True,)  # amount that we get in one transaction
    created_at = models.DateTimeField(auto_now_add=True)



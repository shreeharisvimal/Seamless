from django.db import models
from user_side.models import NewUser
from products.models import ProductVariant

class Coupon(models.Model):
    code = models.CharField(max_length=10, unique=True)
    discount = models.DecimalField(decimal_places=2, max_digits=8)
    valid_from = models.DateTimeField(auto_now_add=True)
    valid_to = models.DateTimeField()
    is_active = models.BooleanField(default= True)

    def __str__(self):
        return f"{self.code}- RS {self.discount}"
    
    def coupon_name (self):
        return f"{self.code}- RS {self.discount}"
    
class Cart(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, null=True,blank=True)
    total = models.DecimalField(decimal_places=2, max_digits=10,default=0, null=True)
    sub_total = models.DecimalField(decimal_places=2, max_digits=10,default=0, null=True)
    shipping = models.DecimalField(decimal_places=2, max_digits=10,default=0, null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}-cart'

    

class Cart_Item(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default= 1)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.cart}-item - {self.product}"
    
    



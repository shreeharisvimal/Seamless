import uuid
from django.db import models
from user_side.models import NewUser
from account.models import Address
from cart.models import Cart,Cart_Item,Coupon
from products.models import ProductVariant

class Payment(models.Model):
    PAYMENT_STATUS = (
        ("PENDING", "Pending"),
        ("FAILED", "Failed"),
        ("SUCCESS", "Success"),
    )
    PAYMENT_METHOD = (
        ('COD', 'Cash On Delivery'),
        ('RazorPay', 'Razor Pay'),
    )
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    payment_method = models.CharField(choices=PAYMENT_METHOD, max_length=100)
    payment_status = models.CharField(choices=PAYMENT_STATUS, max_length=20)
    cod_payment_id = models.UUIDField(default=uuid.uuid4, unique=True, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, null=True, blank=True)
    amount_paid = models.CharField(max_length=30)
    payment_time = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.payment_method == 'COD':
            self.razorpay_payment_id = None
        elif self.payment_method == 'RazorPay':
            self.cod_payment_id = None
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.cod_payment_id) if self.cod_payment_id else str(self.razorpay_payment_id)
    

class Order(models.Model):
    
    user = models.ForeignKey(NewUser, on_delete=models.SET_NULL, null=True)
    payment_details = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True)
    order_number = models.AutoField(primary_key=True)
    shipping_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, related_name='shipping_address')
    billing_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, related_name='billing_address')
    order_total = models.DecimalField(max_digits=12, decimal_places=2)
    order_subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    order_shipping = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    order_coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, null=True, blank=True)
    is_complete = models.BooleanField(default=False)
    order_time = models.DateTimeField(auto_now_add=True)
    order_update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.user} - {self.order_number}"
class OrderItem(models.Model):
    ORDER_STATUS = (
        ("PLACED", "Order Placed"),
        ("PROCESSING", "Order Processing"),
        ("SHIPPED", "Order Shipped"),
        ("OUT FOR DELIVERY", "out for delivery"),
        ("DELIVERED", "Order Delivered"),
        ("CANCELLED", "Order Cancelled"),
    )  
    user = models.ForeignKey(NewUser, on_delete=models.SET_NULL, null=True)
    order_item_id = models.CharField(max_length=120, default='#0000000')
    order_status = models.CharField(choices=ORDER_STATUS, max_length=20, default='PLACED')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True) 
    order_product = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.IntegerField(default= 1)
    payment_details = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True)
    product_price = models.DecimalField(decimal_places=2, max_digits=10,default=0, null=True)
    ordered_time = models.DateTimeField(auto_now_add=True)
    order_updated_time = models.DateTimeField(auto_now=True)
    cancel_reason = models.TextField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"Order {self.user}"
    




    

    

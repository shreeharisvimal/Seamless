# Generated by Django 4.2.7 on 2023-12-02 07:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0003_alter_userprofile_email_alter_userprofile_full_name_and_more'),
        ('cart', '0006_cart_total'),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_method', models.CharField(choices=[('COD', 'Cash On Delivery'), ('razorpay', 'Razor Pay')], max_length=100)),
                ('payment_status', models.CharField(choices=[('PENDING', 'Pending'), ('FAILED', 'Failed'), ('SUCCESS', 'Success')], max_length=20)),
                ('cod_payment_id', models.UUIDField(blank=True, default=uuid.uuid4, null=True, unique=True)),
                ('razorpay_payment_id', models.CharField(blank=True, max_length=100, null=True)),
                ('amount_paid', models.CharField(max_length=30)),
                ('payment_time', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordered_time', models.DateTimeField(auto_now_add=True)),
                ('order_updated_time', models.DateTimeField(auto_now=True)),
                ('order_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.productvariant')),
                ('product_price', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_item_product_price', to='cart.cart_item')),
                ('quantity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_item_quantity', to='cart.cart_item')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_number', models.AutoField(primary_key=True, serialize=False)),
                ('order_total', models.DecimalField(decimal_places=2, max_digits=12)),
                ('order_subtotal', models.DecimalField(decimal_places=2, max_digits=12)),
                ('order_shipping', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('order_status', models.CharField(choices=[('PLACED', 'Order Placed'), ('PROCESSING', 'Order Processing'), ('SHIPPED', 'Order Shipped'), ('DELIVERED', 'Order Delivered'), ('CANCELLED', 'Order Cancelled')], default='New', max_length=20)),
                ('is_complete', models.BooleanField(default=False)),
                ('order_time', models.DateTimeField(auto_now_add=True)),
                ('order_update_time', models.DateTimeField(auto_now=True)),
                ('billing_address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='billing_address', to='account.address')),
                ('order_coupon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cart.coupon')),
                ('order_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order_management.orderitem')),
                ('payment_details', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='order_management.payment')),
                ('shipping_address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shipping_address', to='account.address')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

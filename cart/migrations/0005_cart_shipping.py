# Generated by Django 4.2.7 on 2023-11-30 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_alter_cart_coupon'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='shipping',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True),
        ),
    ]

# Generated by Django 4.2.5 on 2023-11-18 13:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
        ('user_side', '0002_wishlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishlist',
            name='my_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='wishlist',
            name='wish_item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='products.productvariant'),
        ),
    ]

# Generated by Django 4.2.7 on 2023-12-04 15:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_productvariant_product_varient_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productvariant',
            name='thumbnail_img',
        ),
        migrations.CreateModel(
            name='VariantImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.ImageField(upload_to='varient_img/')),
                ('variant', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='products.productvariant')),
            ],
        ),
    ]

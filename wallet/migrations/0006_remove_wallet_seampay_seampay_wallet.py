# Generated by Django 4.2.7 on 2023-12-13 07:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0005_wallet_seampay'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wallet',
            name='seampay',
        ),
        migrations.AddField(
            model_name='seampay',
            name='wallet',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='wallet.wallet'),
        ),
    ]

# Generated by Django 5.1.1 on 2024-11-02 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodies', '0017_weekly_special_alter_cart_itemimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]

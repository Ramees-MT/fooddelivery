# Generated by Django 5.1.1 on 2024-11-01 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodies', '0016_alter_special_offer_itemimage_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Weekly_special',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('specialname', models.CharField(max_length=50)),
                ('specialimage', models.URLField()),
            ],
        ),
        migrations.AlterField(
            model_name='cart',
            name='itemimage',
            field=models.URLField(),
        ),
    ]

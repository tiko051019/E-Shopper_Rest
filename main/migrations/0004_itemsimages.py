# Generated by Django 5.1.6 on 2025-04-06 19:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_itemsdetails'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemsImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='Images', verbose_name='Carousel Images')),
                ('key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items_images_rn', to='main.items')),
            ],
        ),
    ]

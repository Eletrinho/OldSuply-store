# Generated by Django 4.2.1 on 2023-05-27 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0004_rename_img_product_imagens"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="description",
            field=models.TextField(blank=True),
        ),
    ]

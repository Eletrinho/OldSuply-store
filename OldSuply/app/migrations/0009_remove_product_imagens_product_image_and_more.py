# Generated by Django 4.2.1 on 2023-06-05 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0008_remove_product_imagens_product_image_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="imagens",
        ),
        migrations.AddField(
            model_name="product",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="products/"),
        ),
        migrations.AlterField(
            model_name="product",
            name="slug",
            field=models.SlugField(blank=True, default="slug_padrao", unique=True),
        ),
    ]

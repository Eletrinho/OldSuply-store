# Generated by Django 4.2.4 on 2023-11-09 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0010_remove_product_size_delete_size"),
    ]

    operations = [
        migrations.AddField(
            model_name="address",
            name="bairro",
            field=models.CharField(default="Zona Industrial (Guará)", max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="address",
            name="number",
            field=models.CharField(default=24, max_length=8),
            preserve_default=False,
        ),
    ]

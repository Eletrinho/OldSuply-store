# Generated by Django 4.2.1 on 2023-07-27 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0006_product_size"),
    ]

    operations = [
        migrations.CreateModel(
            name="Size",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "clothes_size",
                    models.CharField(
                        choices=[("P", "P"), ("M", "M"), ("G", "G")], max_length=1
                    ),
                ),
            ],
        ),
        migrations.RemoveField(
            model_name="product",
            name="size",
        ),
        migrations.AddField(
            model_name="product",
            name="size",
            field=models.ManyToManyField(to="app.size"),
        ),
    ]
# Generated by Django 4.2.1 on 2023-07-28 15:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0009_remove_size_name"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="size",
        ),
        migrations.DeleteModel(
            name="Size",
        ),
    ]

# Generated by Django 3.1.7 on 2021-07-20 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authenticate", "0003_auto_20210713_1243"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="phonenumber",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
# Generated by Django 3.1.7 on 2021-07-13 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authenticate", "0002_alerts"),
    ]

    operations = [
        migrations.AddField(
            model_name="alerts",
            name="monthly",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="alerts",
            name="weekly",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="alerts",
            name="yearly",
            field=models.BooleanField(default=False),
        ),
    ]

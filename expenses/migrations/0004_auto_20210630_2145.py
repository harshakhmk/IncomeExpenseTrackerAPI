# Generated by Django 3.1.7 on 2021-06-30 16:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("expenses", "0003_auto_20210630_1124"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="expense",
            options={"ordering": ["-transaction_date"]},
        ),
    ]

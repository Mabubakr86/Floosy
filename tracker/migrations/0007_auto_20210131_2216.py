# Generated by Django 3.1.5 on 2021-01-31 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0006_auto_20210126_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
# Generated by Django 3.1.5 on 2021-01-25 11:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0002_wallet_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='wallet',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='tracker.wallet'),
            preserve_default=False,
        ),
    ]

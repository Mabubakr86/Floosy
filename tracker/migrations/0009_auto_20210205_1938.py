# Generated by Django 3.1.5 on 2021-02-05 17:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0008_auto_20210201_2047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='wallet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='tickets', to='tracker.wallet'),
        ),
    ]
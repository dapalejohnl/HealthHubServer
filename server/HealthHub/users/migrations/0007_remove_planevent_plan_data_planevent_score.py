# Generated by Django 4.1.3 on 2023-06-05 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_planevent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='planevent',
            name='plan_data',
        ),
        migrations.AddField(
            model_name='planevent',
            name='score',
            field=models.FloatField(default=0, verbose_name='plan score'),
            preserve_default=False,
        ),
    ]

# Generated by Django 5.1.5 on 2025-02-02 14:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0008_stats_delete_streak'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='stats',
            name='best_streak',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='stats',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, unique=True),
        ),
    ]

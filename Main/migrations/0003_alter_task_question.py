# Generated by Django 5.1.5 on 2025-02-02 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0002_test_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='question',
            field=models.CharField(max_length=255),
        ),
    ]

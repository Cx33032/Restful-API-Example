# Generated by Django 5.0.4 on 2024-04-21 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_newsagency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='author',
            field=models.CharField(max_length=32),
        ),
    ]

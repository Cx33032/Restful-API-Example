# Generated by Django 5.0.4 on 2024-04-21 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0007_userinformation_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='author_username',
            field=models.CharField(default=' ', max_length=32),
            preserve_default=False,
        ),
    ]

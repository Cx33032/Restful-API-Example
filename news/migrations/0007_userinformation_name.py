# Generated by Django 5.0.4 on 2024-04-21 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0006_alter_story_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinformation',
            name='name',
            field=models.CharField(default='John Smith', max_length=48),
        ),
    ]

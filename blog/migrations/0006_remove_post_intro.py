# Generated by Django 4.2.3 on 2023-07-25 08:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_post_content5_post_title5'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='intro',
        ),
    ]

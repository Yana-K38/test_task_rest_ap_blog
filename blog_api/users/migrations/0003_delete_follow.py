# Generated by Django 4.2 on 2023-08-06 13:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_blog_name_follow_follow_unique_name_follow'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Follow',
        ),
    ]
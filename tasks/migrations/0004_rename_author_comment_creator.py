# Generated by Django 4.2.1 on 2024-05-12 20:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='author',
            new_name='creator',
        ),
    ]

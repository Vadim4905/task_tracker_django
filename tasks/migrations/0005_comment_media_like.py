# Generated by Django 4.2.1 on 2024-05-19 10:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0004_rename_author_comment_creator'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='media',
            field=models.FileField(blank=True, null=True, upload_to='comments_media/'),
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='tasks.comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liked_comments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('comment', 'user')},
            },
        ),
    ]

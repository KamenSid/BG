# Generated by Django 4.2.1 on 2023-05-21 12:35

from django.db import migrations
import django.utils.timezone
import embed_video.fields


class Migration(migrations.Migration):

    dependencies = [
        ('testdb', '0002_replay'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='replay',
            name='video_resource',
        ),
        migrations.AddField(
            model_name='replay',
            name='video',
            field=embed_video.fields.EmbedVideoField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
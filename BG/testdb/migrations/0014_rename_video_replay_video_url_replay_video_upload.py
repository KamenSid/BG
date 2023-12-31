# Generated by Django 4.2.1 on 2023-07-16 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testdb', '0013_alter_comment_options_alter_replay_likes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='replay',
            old_name='video',
            new_name='video_url',
        ),
        migrations.AddField(
            model_name='replay',
            name='video_upload',
            field=models.FileField(blank=True, null=True, upload_to='replays/'),
        ),
    ]

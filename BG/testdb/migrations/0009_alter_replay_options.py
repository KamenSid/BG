# Generated by Django 4.2.1 on 2023-07-01 06:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testdb', '0008_comment_delete_teacher_remove_replay_likes_count_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='replay',
            options={'ordering': ['title']},
        ),
    ]

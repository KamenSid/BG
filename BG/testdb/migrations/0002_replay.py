# Generated by Django 4.2.1 on 2023-05-21 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testdb', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Replay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('author', models.CharField(max_length=20)),
                ('video_resource', models.CharField(max_length=150)),
                ('description', models.CharField(max_length=300)),
            ],
        ),
    ]

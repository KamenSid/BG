# Generated by Django 4.2.1 on 2023-07-22 08:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0011_remove_appuserprofile_guild_alter_guild_members'),
    ]

    operations = [
        migrations.AddField(
            model_name='appuserprofile',
            name='guild',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='members.guild'),
        ),
    ]

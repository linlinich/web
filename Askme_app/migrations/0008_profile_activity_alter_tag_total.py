# Generated by Django 4.1.3 on 2022-11-16 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Askme_app', '0007_answer_is_correct_alter_profile_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='activity',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='tag',
            name='total',
            field=models.IntegerField(default=0),
        ),
    ]

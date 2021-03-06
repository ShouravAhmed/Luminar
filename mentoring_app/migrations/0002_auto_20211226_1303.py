# Generated by Django 3.2.7 on 2021-12-26 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentoring_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mentoringprogram',
            name='cover_picture',
            field=models.ImageField(blank=True, default='default_cover.jpg', null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='userresponse',
            name='exp_level',
            field=models.PositiveIntegerField(default=0),
        ),
    ]

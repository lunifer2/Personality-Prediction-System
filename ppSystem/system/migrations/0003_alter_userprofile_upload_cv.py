# Generated by Django 4.0.5 on 2022-07-27 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0002_alter_userprofile_agreeableness_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='upload_cv',
            field=models.FileField(blank=True, null=True, upload_to='CV'),
        ),
    ]
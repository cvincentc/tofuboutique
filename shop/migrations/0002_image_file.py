# Generated by Django 4.1.4 on 2022-12-14 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='images/'),
        ),
    ]

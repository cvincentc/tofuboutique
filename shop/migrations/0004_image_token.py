# Generated by Django 4.1.4 on 2022-12-15 02:41

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_alter_image_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='token',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]

# Generated by Django 3.1.4 on 2021-01-04 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20210104_2010'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Signings',
            new_name='Signing',
        ),
        migrations.AddField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]

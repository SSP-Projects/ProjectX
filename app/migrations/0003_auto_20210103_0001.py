# Generated by Django 3.1.4 on 2021-01-02 23:01

from django.db import migrations
import phone_field.models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20210103_0000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='centers',
            name='phone_number',
            field=phone_field.models.PhoneField(blank=True, max_length=31),
        ),
    ]
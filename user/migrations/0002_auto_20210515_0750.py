# Generated by Django 3.2.2 on 2021-05-15 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='contact_number',
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='location',
            field=models.CharField(max_length=255, null=True),
        ),
    ]

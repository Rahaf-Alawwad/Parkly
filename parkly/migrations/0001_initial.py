# Generated by Django 3.2 on 2021-05-06 09:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Lot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('available_parking', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Parking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('park_ID', models.CharField(max_length=4, null=True, unique=True)),
                ('location', models.CharField(max_length=255, null=True)),
                ('available', models.BooleanField(default=True)),
                ('is_reentry_allowed', models.BooleanField(null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('lot', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lot', to='parkly.lot')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
                ('location', models.CharField(max_length=255, null=True)),
                ('user_type', models.CharField(choices=[('owner', 'owner'), ('user', 'user')], max_length=255, null=True)),
                ('registration_date', models.DateTimeField(auto_now_add=True)),
                ('contact_number', models.CharField(max_length=12)),
                ('activated', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateTime', models.DateTimeField(auto_now_add=True)),
                ('code', models.CharField(max_length=10, unique=True)),
                ('duration', models.PositiveIntegerField(default=1)),
                ('cost', models.PositiveIntegerField()),
                ('is_paid', models.BooleanField(default=False)),
                ('parking', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parking', to='parkly.parking')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='parkly.profile')),
            ],
        ),
        migrations.AddField(
            model_name='lot',
            name='owner',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owner', to='parkly.profile'),
        ),
    ]
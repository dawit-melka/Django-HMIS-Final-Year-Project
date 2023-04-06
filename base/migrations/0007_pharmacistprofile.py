# Generated by Django 4.1.7 on 2023-03-23 10:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0006_alter_prescribedmedicine_dosage_medicalhistory_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PharmacistProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20, null=True)),
                ('last_name', models.CharField(max_length=20, null=True)),
                ('phone', models.CharField(max_length=20, unique=True)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('pharmacist', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
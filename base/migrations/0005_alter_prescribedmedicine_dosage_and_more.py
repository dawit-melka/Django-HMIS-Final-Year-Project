# Generated by Django 4.1.7 on 2023-03-09 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_remove_patient_profile_picture_prescribedmedicine'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prescribedmedicine',
            name='dosage',
            field=models.TextField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='prescribedmedicine',
            name='medicine',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
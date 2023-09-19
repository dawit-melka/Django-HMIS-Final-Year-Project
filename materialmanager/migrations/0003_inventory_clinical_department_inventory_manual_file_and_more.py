# Generated by Django 4.2 on 2023-06-25 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materialmanager', '0002_alter_inventory_serial_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='clinical_department',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='inventory',
            name='manual_file',
            field=models.FileField(blank=True, null=True, upload_to='manuals/'),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='manuals_available',
            field=models.ManyToManyField(blank=True, null=True, to='materialmanager.manuals'),
        ),
    ]
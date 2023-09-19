# Generated by Django 4.2 on 2023-06-24 13:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('doctor', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cashier', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReceptionProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20, null=True)),
                ('last_name', models.CharField(max_length=20, null=True)),
                ('phone', models.CharField(max_length=20, unique=True)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('active', models.BooleanField(default=False)),
                ('recepetion', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20, null=True)),
                ('middle_name', models.CharField(max_length=20, null=True)),
                ('last_name', models.CharField(max_length=20, null=True)),
                ('gender', models.CharField(choices=[('Male', 'M'), ('Female', 'F')], max_length=10, null=True)),
                ('marital_status', models.CharField(blank=True, choices=[('maried', 'Maried'), ('single', 'Single'), ('divorced', 'Divorced'), ('widowed', 'Widowed')], max_length=10, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone', models.CharField(max_length=20, unique=True)),
                ('dateofbirth', models.DateField(blank=True, null=True)),
                ('bloodtype', models.CharField(blank=True, choices=[('A', 'A'), ('B', 'B'), ('AB', 'AB'), ('O', 'O')], max_length=10, null=True)),
                ('RH', models.CharField(blank=True, choices=[('+', '+'), ('-', '-')], max_length=10, null=True)),
                ('address', models.CharField(max_length=20, null=True)),
                ('region', models.CharField(blank=True, choices=[('Tigray', 'Tigray'), ('Afar', 'Afar'), ('Amhara', 'Amhara'), ('Oromia', 'Oromia'), ('Somali', 'Somali'), ('Benishangul-Gumuz', 'Benishangul-Gumuz'), ('Gambella', 'Gambella'), ('Harari', 'Harari'), ('', '')], max_length=20, null=True)),
                ('city', models.CharField(blank=True, max_length=20, null=True)),
                ('emergency_contact_name', models.CharField(blank=True, max_length=40, null=True)),
                ('relationship', models.CharField(blank=True, max_length=20, null=True)),
                ('contact_phone', models.CharField(blank=True, max_length=20, null=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('reception', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date', models.DateField(blank=True, null=True)),
                ('time', models.TimeField(blank=True, null=True)),
                ('reason', models.CharField(max_length=200, null=True)),
                ('status', models.BooleanField(default=True)),
                ('payment', models.BooleanField(default=False)),
                ('payment_date', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('Cashier', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cashier.cashierprofile')),
                ('Doctor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='doctor.doctorprofile')),
                ('Patient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='reception.patient')),
                ('Specalization', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='doctor.doctorspecalization')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]

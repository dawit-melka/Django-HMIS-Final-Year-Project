# Generated by Django 4.2 on 2023-06-24 22:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nurse', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='registerbirth',
            options={'ordering': ['-created']},
        ),
        migrations.AlterModelOptions(
            name='vitalsigns',
            options={'ordering': ['-created']},
        ),
    ]

# Generated by Django 3.2.5 on 2021-07-22 14:36

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Firmware',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(max_length=13, unique=True)),
                ('data', models.FileField(upload_to='firmwares/')),
                ('is_active', models.BooleanField(default=False)),
            ],
        ),
    ]

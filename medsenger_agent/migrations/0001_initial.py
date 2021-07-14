# Generated by Django 3.2.5 on 2021-07-14 17:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('contract_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('speaker_active', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='MeasurementTaskGeneric',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(max_length=255)),
                ('category', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255, null=True)),
                ('max_value', models.FloatField(null=True)),
                ('min_value', models.FloatField(null=True)),
                ('text', models.CharField(max_length=255)),
                ('value_type', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Speaker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField(unique=True)),
                ('token', models.CharField(max_length=255, unique=True)),
                ('contract', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='medsenger_agent.contract')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_id', models.IntegerField()),
                ('text', models.TextField()),
                ('is_red', models.BooleanField(default=False)),
                ('is_notified', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('contract', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='medsenger_agent.contract')),
            ],
        ),
        migrations.CreateModel(
            name='MedicineTaskGeneric',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medsenger_id', models.IntegerField()),
                ('title', models.CharField(max_length=255)),
                ('rules', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('is_sent', models.BooleanField(default=False)),
                ('is_done', models.BooleanField(default=False)),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medsenger_agent.contract')),
            ],
        ),
        migrations.CreateModel(
            name='MeasurementTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('doctor_description', models.TextField(default=None, null=True)),
                ('patient_description', models.TextField(default=None, null=True)),
                ('thanks_text', models.TextField(default=None, null=True)),
                ('is_sent', models.BooleanField(default=False)),
                ('is_done', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medsenger_agent.contract')),
                ('fields', models.ManyToManyField(to='medsenger_agent.MeasurementTaskGeneric')),
            ],
        ),
    ]

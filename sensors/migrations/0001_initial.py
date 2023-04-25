# Generated by Django 4.2 on 2023-04-07 23:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sensor_Configuration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_interval', models.IntegerField()),
                ('UART_address', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Sensor_Data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('volts', models.PositiveSmallIntegerField()),
                ('amps', models.PositiveSmallIntegerField()),
                ('frequency', models.PositiveSmallIntegerField()),
                ('watts', models.PositiveSmallIntegerField()),
                ('power_factor', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Sensor_Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.CharField(max_length=255)),
                ('brand', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sensors.sensor_type')),
            ],
        ),
    ]

# Generated by Django 4.2 on 2023-04-24 02:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sensors', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('data', models.JSONField()),
            ],
        ),
        migrations.DeleteModel(
            name='Sensor_Data',
        ),
        migrations.RenameField(
            model_name='sensor',
            old_name='reference',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='sensor_configuration',
            name='UART_address',
        ),
        migrations.AddField(
            model_name='sensor',
            name='sensor_configuration',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='sensors.sensor_configuration'),
        ),
        migrations.AddField(
            model_name='sensor_configuration',
            name='params',
            field=models.JSONField(null=True),
        ),
        migrations.AddField(
            model_name='data',
            name='sensor_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sensors.sensor'),
        ),
    ]

# Generated by Django 3.0.8 on 2020-07-14 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Radar_05',
            fields=[
                ('dictionay_id', models.AutoField(primary_key=True, serialize=False)),
                ('dir_name', models.TextField()),
                ('space', models.BigIntegerField()),
                ('scan_date', models.DateTimeField()),
            ],
        ),
    ]

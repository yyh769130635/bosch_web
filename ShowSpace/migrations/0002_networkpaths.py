# Generated by Django 3.0.8 on 2020-07-14 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ShowSpace', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='networkPaths',
            fields=[
                ('path_id', models.AutoField(primary_key=True, serialize=False)),
                ('path', models.TextField()),
            ],
        ),
    ]
# Generated by Django 3.2.3 on 2021-05-20 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ordenador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fabricante', models.CharField(max_length=100)),
                ('modelo', models.CharField(max_length=100)),
                ('ram', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=100)),
                ('precio', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'ordenador',
            },
        ),
    ]

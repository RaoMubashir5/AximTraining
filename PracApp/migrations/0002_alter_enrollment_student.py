# Generated by Django 5.1 on 2024-08-14 21:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PracApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrollment',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PracApp.student', verbose_name='Enrolled Students'),
        ),
    ]

# Generated by Django 5.1 on 2024-08-12 17:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PracApp', '0004_alter_student_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='student',
            options={'ordering': ['first_name']},
        ),
    ]

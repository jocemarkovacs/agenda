# Generated by Django 4.0.4 on 2022-05-21 20:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_evento_local'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evento',
            name='local',
        ),
    ]
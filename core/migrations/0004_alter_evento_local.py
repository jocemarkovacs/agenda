# Generated by Django 4.0.4 on 2022-05-20 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_evento_local'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evento',
            name='local',
            field=models.CharField(max_length=100),
        ),
    ]
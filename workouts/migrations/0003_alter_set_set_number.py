# Generated by Django 5.1.1 on 2024-10-07 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workouts', '0002_workout_exercises'),
    ]

    operations = [
        migrations.AlterField(
            model_name='set',
            name='set_number',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]

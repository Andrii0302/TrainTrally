# Generated by Django 5.1.1 on 2024-10-09 12:36

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workouts', '0004_workout_sets_workout_volume'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='exercisehistory',
            options={'verbose_name': 'Exercise history', 'verbose_name_plural': 'Exercise history'},
        ),
        migrations.CreateModel(
            name='ExerciseHistorySet',
            fields=[
                ('set_number', models.PositiveIntegerField()),
                ('reps', models.IntegerField(default=0)),
                ('weight', models.FloatField(default=0.0)),
                ('set_type', models.CharField(choices=[('W', 'Warmup'), ('R', 'Rest Set'), ('D', 'Drop Set'), ('N', 'Normal Set'), ('F', 'Failure Set')], max_length=200)),
                ('done', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('history', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sets', to='workouts.exercisehistory')),
            ],
        ),
    ]

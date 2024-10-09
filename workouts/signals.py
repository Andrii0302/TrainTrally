from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Workout,Exercise,Set,ExerciseHistory,ExerciseHistorySet
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import m2m_changed
from workouts import models

@receiver(m2m_changed, sender=Workout.exercises.through)
def createExerciseHistory(sender, instance, action, **kwargs):
    if action == 'post_add': 
        total_volume = 0
        workouts_sets_count = 0
        if instance.done:
            for exercise in instance.exercises.all():
                total_sets = exercise.sets.filter(done=True).count()
                total_reps = sum(reps for (reps,) in exercise.sets.filter(done=True).values_list('reps'))
                total_weight = sum(weight * reps for (weight, reps) in exercise.sets.filter(done=True).values_list('weight', 'reps'))
                
                total_volume += total_weight
                workouts_sets_count += total_sets

                # Create ExerciseHistory instance
                exercise_history = ExerciseHistory.objects.create(
                    workout=instance,
                    exercise=exercise,
                    total_sets=total_sets,
                    total_reps=total_reps,
                    total_weight=total_weight
                )

                # Loop through each set and save its details to ExerciseHistorySet
                for set_instance in exercise.sets.filter(done=True):
                    ExerciseHistorySet.objects.create(
                        history=exercise_history,
                        set_number=set_instance.set_number,
                        reps=set_instance.reps,
                        weight=set_instance.weight,
                        set_type=set_instance.set_type,
                        done=set_instance.done
                    )

                instance.sets = workouts_sets_count
                instance.volume = total_volume
                instance.save()

                # Delete the sets from the Set table after saving them to ExerciseHistorySet
                exercise.sets.all().delete()

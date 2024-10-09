from django.db import models
from users.models import Profile
import uuid

class Exercise(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    primary = models.ManyToManyField('MuscleGroupTag', related_name="primary_muscles", blank=True)
    secondary = models.ManyToManyField('MuscleGroupTag', related_name="secondary_muscles", blank=True)
    description = models.TextField(null=True, blank=True)
    user_note = models.CharField(max_length=500, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name


class Set(models.Model):
    SETS_TYPES = (
        ('W', 'Warmup'),
        ('R', 'Rest Set'),
        ('D', 'Drop Set'),
        ('N','Normal Set'),
        ('F', 'Failure Set'),
    )
    exercise = models.ForeignKey(Exercise, related_name="sets", on_delete=models.CASCADE)
    set_number = models.PositiveIntegerField(null=True, blank=True)
    reps = models.IntegerField(null=True, blank=True, default=0)
    weight = models.FloatField(null=True, blank=True, default=0.0)
    set_type = models.CharField(max_length=200, choices=SETS_TYPES, null=True, blank=True)
    done = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return f'Set {self.set_number} of {self.exercise.name}'
    @property
    def increment_sets(self):
        self.set_number += 1
        self.save()

class Workout(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=200, null=True, blank=True)
    featured_img= models.ImageField(null=True, blank=True, default="default.jpg")
    description = models.TextField(null=True, blank=True)
    exercises = models.ManyToManyField(Exercise,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    duration = models.DurationField()
    volume = models.FloatField(default=0.0)
    sets = models.IntegerField(default=0)
    done = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}'


class ExerciseHistory(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    total_sets = models.IntegerField(default=0)
    total_reps = models.IntegerField(default=0)
    total_weight = models.FloatField(default=0.0)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    class Meta:
        verbose_name = 'Exercise history'
        verbose_name_plural = 'Exercise history'
    def __str__(self):
        return f'{self.exercise.name} in {self.workout.name}'
class ExerciseHistorySet(models.Model):
    history = models.ForeignKey(ExerciseHistory, related_name="sets", on_delete=models.CASCADE)
    set_number = models.PositiveIntegerField()
    reps = models.IntegerField(default=0)
    weight = models.FloatField(default=0.0)
    set_type = models.CharField(max_length=200, choices=Set.SETS_TYPES)
    done = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return f'Set {self.set_number} of {self.history.exercise.name} in workout {self.history.workout.name}'

class MuscleGroupTag(models.Model):
    name=models.CharField(max_length=200)
    created=models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)
    def __str__(self):
        return self.name
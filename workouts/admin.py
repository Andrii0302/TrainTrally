from django.contrib import admin

from .models import Workout,Exercise,Set,ExerciseHistory,ExerciseHistorySet

admin.site.register(Workout)
admin.site.register(Exercise)
admin.site.register(Set)
admin.site.register(ExerciseHistory)
admin.site.register(ExerciseHistorySet)

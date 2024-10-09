from django.urls import path
from .views import HomeView,WorkoutsView,CreateWorkoutView,UpdateWorkoutView,WorkoutView,DeleteWorkoutView,\
ExercisesView,CreateCustomExerciseView,DeleteCustomExerciseView, SingleExerciseView,SubmitWorkoutView

urlpatterns = [
    path('',HomeView.as_view(),name='home'),
    path('workouts/',WorkoutsView.as_view(),name='workouts'),
    path('workout/<uuid:pk>/',WorkoutView.as_view(),name='workout'),
    path('create-workout/',CreateWorkoutView.as_view(),name='create-workout'),
    path('update-workout/<uuid:pk>/',UpdateWorkoutView.as_view(),name='update-workout'),
    path('delete-workout/<uuid:pk>/',DeleteWorkoutView.as_view(),name='delete-workout'),
    path('exercises/',ExercisesView.as_view(),name='exercises'),
    path('create-exercise/',CreateCustomExerciseView.as_view(),name='create-exercise'),
    path('delete-exercise/<uuid:pk>/',DeleteCustomExerciseView.as_view(),name='delete-exercise'),
    path('exercise/<uuid:pk>/',SingleExerciseView.as_view(),name='exercise'),
    path('submit-workout/<uuid:pk>/',SubmitWorkoutView.as_view(),name='submit-workout'),
]
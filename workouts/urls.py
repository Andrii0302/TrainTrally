from django.urls import path
from .views import HomeView,WorkoutsView,CreateWorkoutView,UpdateFormView,WorkoutView

urlpatterns = [
    path('',HomeView.as_view(),name='home'),
    path('workouts/',WorkoutsView.as_view(),name='workouts'),
    path('workout/<uuid:pk>/',WorkoutView.as_view(),name='workout'),
    path('create-workout/',CreateWorkoutView.as_view(),name='create-workout'),
    path('update-workout/<uuid:pk>/',UpdateFormView.as_view(),name='update-workout'),
]
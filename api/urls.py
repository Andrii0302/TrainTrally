from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('', views.getRoutes),
    path('workouts/', views.getWorkouts),
    path('workouts/<uuid:pk>/', views.getWorkout),
    path('workouts/<uuid:pk>/exercises/', views.getExercises),
    path('workouts/<uuid:pk>/sets/', views.getSets),
    path('workouts/create-set/', views.createSet, name='create-set'),
    path('workouts/create-exercise/', views.createExercise, name='create-exercise'),
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/',views.getUsers, name='users'),
    path('users/<uuid:pk>/',views.getUser, name='user'),
]

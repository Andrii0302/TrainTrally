from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import WorkoutSerializer,ExerciseSerializer,SetSerializer,ExerciseHistorySetSerializer,ProfileSerializer
from workouts.models import Workout,ExerciseHistorySet,ExerciseHistory
from users.models import Profile
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status

@api_view(['GET'])
def getRoutes(request):
    routes = [
        {'GET': '/api/workouts'},
        {'GET': '/api/workouts/id'},
        {'POST': '/api/workouts/id/vote'},]
    return Response(routes)

@api_view(['GET'])
def getWorkouts(request):
    workouts = Workout.objects.all()
    serializer = WorkoutSerializer(workouts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getWorkout(request,pk):
    workout = Workout.objects.get(id=pk)
    serializer = WorkoutSerializer(workout, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def getExercises(request,pk):
    workout = Workout.objects.get(id=pk)
    exercises = workout.exercises.all()
    serializer = ExerciseSerializer(exercises, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getSets(request,pk):
    exercise_history_entries = ExerciseHistory.objects.filter(workout__id=pk)
    sets = ExerciseHistorySet.objects.filter(history__in=exercise_history_entries)
    serializer = ExerciseHistorySetSerializer(sets, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createSet(request):
    serializer = SetSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated,IsAdminUser])
def createExercise(request):
    serializer = ExerciseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getUsers(request):
    users= Profile.objects.all()
    serializer = ProfileSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getUser(request,pk):
    user = Profile.objects.get(id=pk)
    serializer = ProfileSerializer(user, many=False)
    return Response(serializer.data)

from rest_framework import serializers
from workouts.models import Workout,Set,Exercise,ExerciseHistorySet,ExerciseHistory
from users.models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ['owner','name','description','primary','secondary','user_note']

class WorkoutSerializer(serializers.ModelSerializer):
    owner= ProfileSerializer(many=False)
    exercises= serializers.SerializerMethodField()
    class Meta:
        model = Workout
        fields = '__all__'
    def get_exercises(self,object):
        exercises = object.exercises.all()
        serializer = ExerciseSerializer(exercises,many=True)
        return serializer.data
class SetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Set
        fields = ['exercise', 'set_number', 'reps', 'weight', 'set_type', 'done']

class ExerciseHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseHistory
        fields = '__all__'

class ExerciseHistorySetSerializer(serializers.ModelSerializer):
    history = ExerciseHistorySerializer(read_only=True)
    class Meta:
        model = ExerciseHistorySet
        fields = '__all__'

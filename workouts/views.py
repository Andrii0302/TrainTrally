from datetime import timedelta
from typing import Any
from django.db.models.query import QuerySet
from django.forms import formset_factory
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.views import View
from .models import Workout,Exercise,Set,ExerciseHistory,ExerciseHistorySet
from .forms import WorkoutForm,ExerciseForm
from django.views.generic import ListView,DetailView
from django.views.generic.edit import FormView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SetForm,ExerciseHistorySetForm
from django.db.models.signals import m2m_changed
"""
Workouts
"""
class HomeView(View):
    def get(self,request):
        return HttpResponse('TrainTrally')

class WorkoutsView(ListView):
    model = Workout
    template_name = 'workouts/workouts.html'
    context_object_name = 'workouts'
    def get_queryset(self) -> QuerySet[Any]:
        return Workout.objects.all()



class CreateWorkoutView(LoginRequiredMixin, View):
    def get(self, request):
        
        exercises = Exercise.objects.all()
        context = {'exercises': exercises}
        return render(request, 'workouts/workout-form.html', context)

    def post(self, request):
        workout_form = WorkoutForm(request.POST)
        exercise_ids = request.POST.getlist('exercise_id')
        reps_list = request.POST.getlist('reps')
        weight_list = request.POST.getlist('weight')
        set_type_list = request.POST.getlist('set_type')
        done_list = request.POST.getlist('done')

        if not all(len(lst) == len(exercise_ids) for lst in [reps_list, weight_list, set_type_list, done_list]):
            return render(request, 'workouts/workout-form.html', {
                'error': 'Mismatched data lengths. Please check your input.',
                'exercises': Exercise.objects.all(),
            
            })
        set_count = {}
        sets = []  

        for i in range(len(exercise_ids)):
            exercise_id = exercise_ids[i]

            if exercise_id not in set_count:
                set_count[exercise_id] = 1  
            else:
                set_count[exercise_id] += 1 

            exercise = Exercise.objects.get(id=exercise_id)

            set_instance = Set(
                exercise=exercise,
                set_number=set_count[exercise_id],  
                reps=int(reps_list[i]) if reps_list[i] else 0,
                weight=float(weight_list[i]) if weight_list[i] else 0.0,
                set_type=set_type_list[i], 
                done=done_list[i] == 'true', 
            )
            set_instance.save() 
            sets.append(set_instance) 
        
        workout = Workout.objects.create(
            owner=request.user.profile,  
            duration=timedelta(hours=1),
            done=False, 
        )

        for set_instance in sets:
            workout.exercises.add(set_instance.exercise) 
        workout.done = True
        workout.save() 
        m2m_changed.send(sender=Workout.exercises.through, instance=workout, action='post_add')
        return redirect('submit-workout',pk=workout.id) 

class SubmitWorkoutView(View):
    def get(self,request,pk):
        workout = get_object_or_404(Workout, id=pk, owner=self.request.user.profile)
        form=WorkoutForm()
        context={'form':form,'workout':workout}
        return render(request, 'workouts/submit-workout.html',context)
    def post(self,request,pk):
        workout = get_object_or_404(Workout, id=pk, owner=self.request.user.profile)
        form=WorkoutForm(request.POST,request.FILES,instance=workout)
        if form.is_valid():
            form.save()
            return redirect('workouts')
        context={'form':form,'workout':workout}
        return render(request, 'workouts/submit-workout.html',context)

class UpdateWorkoutView(LoginRequiredMixin, View):
    def get(self, request, pk):
        workout = get_object_or_404(Workout, id=pk, owner=self.request.user.profile)
        
        # Get all exercise histories for the workout
        exercise_histories = ExerciseHistory.objects.filter(workout=workout)

        # Create forms for each ExerciseHistorySet related to the workout
        exercise_history_set_forms = []
        for exercise_history in exercise_histories:
            sets = ExerciseHistorySet.objects.filter(history=exercise_history)
            for set_instance in sets:
                form = ExerciseHistorySetForm(instance=set_instance)
                exercise_history_set_forms.append((exercise_history, form))

        workout_form = WorkoutForm(instance=workout)

        context = {
            'workout_form': workout_form,
            'exercise_history_set_forms': exercise_history_set_forms,
            'exercise_histories': exercise_histories  # Pass to template if needed
        }
        return render(request, 'workouts/update-workout.html', context)

    def post(self, request, pk):
        workout = get_object_or_404(Workout, id=pk, owner=self.request.user.profile)

        # Get all exercise histories for the workout
        exercise_histories = ExerciseHistory.objects.filter(workout=workout)
        workout_form = WorkoutForm(request.POST, request.FILES, instance=workout)

        # Initialize a dictionary to hold totals for each exercise
        exercise_totals = {}

        # Collect forms for each set
        exercise_history_set_forms = []
        for exercise_history in exercise_histories:
            sets = ExerciseHistorySet.objects.filter(history=exercise_history)
            for set_instance in sets:
                form = ExerciseHistorySetForm(request.POST, instance=set_instance)
                exercise_history_set_forms.append((exercise_history, form))
                if form.is_valid():
                    # Initialize totals for this exercise if not already done
                    if exercise_history.id not in exercise_totals:
                        exercise_totals[exercise_history.id] = {
                            'total_sets': 0,
                            'total_reps': 0,
                            'total_weight': 0
                        }

                    # Increment totals for this exercise
                    exercise_totals[exercise_history.id]['total_sets'] += 1  # Increment total sets
                    exercise_totals[exercise_history.id]['total_reps'] += form.cleaned_data['reps']
                    exercise_totals[exercise_history.id]['total_weight'] += form.cleaned_data['weight']

        # Check if workout form is valid and all set forms are valid
        if workout_form.is_valid() and all(form.is_valid() for _, form in exercise_history_set_forms):
            # Calculate total volume for the workout
            total_volume = 0

            # Update each ExerciseHistory with its respective totals
            for exercise_history in exercise_histories:
                totals = exercise_totals.get(exercise_history.id, {'total_sets': 0, 'total_reps': 0, 'total_weight': 0})
                
                # Update the ExerciseHistory instance
                exercise_history.total_sets = totals['total_sets']
                exercise_history.total_reps = totals['total_reps']
                exercise_history.total_weight = totals['total_weight']
                exercise_history.save()

                # Update the total volume for the workout
                total_volume += totals['total_reps'] * totals['total_weight']

            # Update the workout volume
            workout.volume = total_volume
            workout.save()

            # Save each form in the formset
            for exercise_history, form in exercise_history_set_forms:
                form.save()

            return redirect('workouts') 

        context = {
            'workout_form': workout_form,
            'exercise_history_set_forms': exercise_history_set_forms,
            'exercise_histories': exercise_histories
        }
        return render(request, 'workouts/update-workout.html', context)




class WorkoutView(DetailView):
    model = Workout
    template_name = 'workouts/single-workout.html'
    context_object_name = 'workout'
    def get_queryset(self) -> QuerySet[Any]:
        return Workout.objects.all()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        workout = self.object
        exercise_histories = ExerciseHistory.objects.filter(workout=workout)
        histories_with_sets = []
        
        for history in exercise_histories:
            # Fetch sets related to the current exercise history
            sets = ExerciseHistorySet.objects.filter(history=history)
            histories_with_sets.append({
                'history': history,
                'sets': sets
            })
        context['exercise_histories'] = histories_with_sets
        return context
class DeleteWorkoutView(LoginRequiredMixin,View):
    def get(self, request, pk):
        workout = get_object_or_404(Workout, id=pk,owner=self.request.user.profile)
        context = {'workout': workout}
        return render(request, 'workouts/delete-workout.html', context)
    def post(self,request,pk):
        workout = get_object_or_404(Workout, id=pk,owner=self.request.user.profile)
        workout.delete()
        return redirect('workouts')
    
class ExercisesView(ListView):
    model = Exercise
    template_name = 'workouts/exercises.html'
    context_object_name = 'exercises'

class CreateCustomExerciseView(LoginRequiredMixin,View):
    def get(self, request):
        form = ExerciseForm()
        context = {'form': form}
        return render(request, 'workouts/exercise-form.html', context)
    def post(self, request):
        form = ExerciseForm(request.POST, request.FILES)
        if form.is_valid():
            exercise = form.save(commit=False)
            exercise.owner = request.user.profile
            exercise.save()
            return redirect('exercises')
        context = {'form': form}
        return render(request, 'workouts/exercise-form.html', context)
class DeleteCustomExerciseView(LoginRequiredMixin,View):
    def get(self, request, pk):
        exercise = get_object_or_404(Exercise, id=pk, owner=self.request.user.profile)
        context = {'exercise': exercise}
        return render(request, 'workouts/delete-exercise.html', context)
    def post(self,request,pk):
        exercise = get_object_or_404(Exercise, id=pk,owner=self.request.user.profile)
        exercise.delete()
        return redirect('exercises')
    
class SingleExerciseView(LoginRequiredMixin,DetailView):
    model = Exercise
    template_name = 'workouts/single-exercise.html'
    context_object_name = 'exercise'
    def get_queryset(self) -> QuerySet[Any]:
        return Exercise.objects.all()

# no update exercise view












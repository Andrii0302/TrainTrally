from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.views import View
from .models import Workout
from .forms import WorkoutForm
from django.views.generic import ListView
from django.views.generic.edit import FormView,UpdateView
from django.urls import reverse_lazy
class HomeView(View):
    def get(self,request):
        return HttpResponse('TrainTrally')

class WorkoutsView(ListView):
    model = Workout
    template_name = 'workouts/workouts.html'
    context_object_name = 'workouts'

class CreateWorkoutView(FormView):
    # def get(self, request):
    #     form = WorkoutForm() 
    #     context = {'form': form}
    #     return render(request, 'workouts/create-workout.html', context)

    # def post(self, request):
    #     form = WorkoutForm(request.POST, request.FILES)  
    #     if form.is_valid():
    #         form.save()
    #         return redirect('workouts')
    #     context = {'form': form}
        
    #     return render(request, 'workouts/create-workout.html', context)
    template_name = 'workouts/create-workout.html'
    form_class = WorkoutForm
    success_url = '/workouts/'
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class UpdateFormView(View):
    def get(self, request, pk):
        workout = get_object_or_404(Workout, id=pk)  
        form = WorkoutForm(instance=workout)
        context = {'form': form, 'workout': workout}
        return render(request, 'workouts/workout-form.html', context)

    def post(self, request, pk):
        workout = get_object_or_404(Workout, id=pk)  
        form = WorkoutForm(request.POST, request.FILES, instance=workout)
        if form.is_valid():
            form.save()
            return redirect('workouts')  
        context = {'form': form, 'workout': workout}
        return render(request, 'workouts/workout-form.html', context)

class WorkoutView(View):
    def get(self,request,pk):
        workout = get_object_or_404(Workout, id=pk)
        context = {'workout': workout}
        return render(request, 'workouts/single-workout.html', context)
    
# class DeleteWorkoutView(View):
#     def get(self, request, pk):
#         workout = get_object_or_404(Workout, id=pk)
#         context = {'workout': workout}
#         return render(request, 'workouts/delete-workout.html', context)



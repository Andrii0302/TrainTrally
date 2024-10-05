from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.views import View
from .models import Workout
from .forms import WorkoutForm
from django.views.generic import ListView,DetailView
from django.views.generic.edit import FormView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

class HomeView(View):
    def get(self,request):
        return HttpResponse('TrainTrally')

class WorkoutsView(ListView):
    model = Workout
    template_name = 'workouts/workouts.html'
    context_object_name = 'workouts'
    def get_queryset(self) -> QuerySet[Any]:
        return Workout.objects.all()

class CreateWorkoutView(LoginRequiredMixin, FormView):
    template_name = 'workouts/workout-form.html'
    form_class = WorkoutForm
    success_url = '/training/workouts/'
    def form_valid(self, form):
        form.instance.owner = self.request.user.profile
        form.save()
        return super().form_valid(form)

class UpdateWorkoutView(LoginRequiredMixin,View):
    def get(self, request, pk):
        workout = get_object_or_404(Workout, id=pk, owner=self.request.user.profile)
        form = WorkoutForm(instance=workout)
        context = {'form': form, 'workout': workout}
        return render(request, 'workouts/workout-form.html', context)

    def post(self, request, pk):
        workout = get_object_or_404(Workout, id=pk, owner=self.request.user.profile)
        form = WorkoutForm(request.POST, request.FILES, instance=workout)
        if form.is_valid():
            form.save()
            return redirect('workouts')  
        context = {'form': form, 'workout': workout}
        return render(request, 'workouts/workout-form.html', context)

class WorkoutView(DetailView):
    model = Workout
    template_name = 'workouts/single-workout.html'
    context_object_name = 'workout'
    def get_queryset(self) -> QuerySet[Any]:
        return Workout.objects.all()
    
class DeleteWorkoutView(LoginRequiredMixin,View):
    def get(self, request, pk):
        workout = get_object_or_404(Workout, id=pk,owner=self.request.user.profile)
        context = {'workout': workout}
        return render(request, 'workouts/delete-workout.html', context)
    def post(self,request,pk):
        workout = get_object_or_404(Workout, id=pk,owner=self.request.user.profile)
        workout.delete()
        return redirect('workouts')




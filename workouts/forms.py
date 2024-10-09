from django import forms
from .models import Workout,Exercise,Set
from django.forms import modelformset_factory

class WorkoutForm(forms.ModelForm):
    class Meta:
        model=Workout
        fields='__all__'
        exclude=['owner','sets','volume','exercises','done']
        widgets={
            'exercises': forms.CheckboxSelectMultiple(),
        }
class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['name', 'primary', 'secondary', 'description', 'user_note']
        widgets = {
            'primary': forms.CheckboxSelectMultiple(),
            'secondary': forms.CheckboxSelectMultiple(),
        }
        

class SetForm(forms.ModelForm):
    class Meta:
        model = Set
        fields = ['exercise', 'set_number', 'reps', 'weight', 'set_type', 'done']

class ExerciseHistorySetForm(forms.ModelForm):
    class Meta:
        model = Set
        fields = ['reps','weight','set_type']
#SetFormSet = modelformset_factory(Set, form=SetForm, extra=3)


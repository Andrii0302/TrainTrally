from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile,Message

class CustomCreationForm(UserCreationForm):
    class Meta:
        model=User
        fields=['first_name','email','username','password1','password2']
        labels = {
            'first_name':'Name',
        }

class ProfileForm(ModelForm):
    class Meta:
        model=Profile
        fields='__all__'
        exclude=['user','created','id']
class MessageForm(ModelForm):
    class Meta:
        model=Message
        fields=['name','email','subject','body']
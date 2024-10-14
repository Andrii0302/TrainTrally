from django.forms import ModelForm
from django import forms
from .models import ChatGroup,ChatMessage


class ChatmessageCreateForm(ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['body']
        widgets = {
            'body' : forms.TextInput(attrs={'placeholder': 'Add message ...', 'class': 'p-4 text-black', 'maxlength' : '300', 'autofocus': True }),
        }
    def __init__(self,*args,**kwargs):
        super(ChatmessageCreateForm,self).__init__(*args,**kwargs)
        for k,v in self.fields.items():
            v.widget.attrs.update({'class':'w-full bg-gray-800 text-white px-3 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500','maxlength':"150"})
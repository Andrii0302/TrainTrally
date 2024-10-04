from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login,authenticate,logout 
from django.contrib import messages
from .forms import CustomCreationForm

class LoginUserView(View):
    page='login'
    def get(self,request):
        if request.user.is_authenticated:
            return redirect('workouts')
        return render(request,'users/login_register.html',{'page':self.page})
    def post(self,request):
        username=request.POST['username']
        password=request.POST['password']
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,'Username does not exist')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('workouts')
        else:
            messages.error(request,'Username or password is incorrect')
            return render(request,'users/login_register.html',{'page':self.page})

class LogoutUserView(View):
    def get(self,request):
        logout(request)
        messages.info(request,'User was logged out')
        return redirect('login')

class RegisterUserView(View):
    page = 'register'

    def get(self, request):
        form = CustomCreationForm()
        return render(request, 'users/login_register.html', {'page': self.page, 'form': form})

    def post(self, request):
        form = CustomCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  
            messages.success(request, 'User account was created!')
            login(request, user)  
            return redirect('workouts') 
        else:
            messages.error(request, 'An error has occurred during registration')
            return render(request, 'users/login_register.html', {'page': self.page, 'form': form})
    
        



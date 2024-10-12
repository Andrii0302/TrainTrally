from django.shortcuts import get_object_or_404, render,redirect
from django.views import View
from django.contrib.auth.models import User
from django.http import Http404, HttpResponse
from django.contrib.auth import login,authenticate,logout 
from django.contrib import messages
from .forms import CustomCreationForm, MessageForm,ProfileForm
from django.views.generic import ListView,DetailView
from .models import Profile,Message
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
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

class ProfilesView(ListView):
    model = Profile
    template_name = 'users/profiles.html'
    context_object_name = 'users'
    # paginate_by = 6
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('-created')

class UserProfileView(DetailView):
    model = Profile
    template_name = 'users/user-profile.html'
    context_object_name = 'profile'

class UserAccountView(LoginRequiredMixin,View):
    def get(self, request):
        user = request.user
        profile = user.profile
        context = {
            'profile': profile,
            'user':user,
        }
        return render(request, 'users/account.html', context)
    

class UserEditAccountView(LoginRequiredMixin,View):
    def get(self,request):
        profile = request.user.profile
        form = ProfileForm(instance=profile)
        return render(request,'users/profile_form.html',{'form':form})
    def post(self,request):
        profile = request.user.profile
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')
        return render(request,'users/profile_form.html',{'form:form'})

class InboxView(LoginRequiredMixin,View):
    def get(self,request):
        profile = request.user.profile
        messageRequest = profile.messages.all()
        unreadCount = messageRequest.filter(is_read=False).count()
        context={'messageRequest':messageRequest,'unreadCount':unreadCount}
        return render(request,'users/inbox.html',context)

class InboxMessageView(LoginRequiredMixin,View):
    def get(self,request,pk):
        profile = request.user.profile
        message = profile.messages.get(id=pk)
        if message.is_read == False:
            message.is_read=True
            message.save()
        context={'message':message}
        return render(request,'users/message.html',context)

class CreateMessageView(LoginRequiredMixin,View):
    def get(self,request,pk):
        recipcipient=Profile.objects.get(id=pk)
        form=MessageForm()
        sender = request.user.profile
        context={'recipient':recipcipient,'form':form}
        return render(request,'users/message_form.html',context)
    
    def post(self,request,pk):
        recipient=Profile.objects.get(id=pk)
        form=MessageForm(request.POST)
        sender = request.user.profile
        if form.is_valid():
            message=form.save(commit=False)
            message.sender = sender
            message.recipient = recipient
            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()
            messages.success(request, 'Your message was successfully sent!')
            return redirect('profile-detail',pk=recipient.id)
        return render(request,'users/message_form.html',{'recipient':recipient,'form':form})


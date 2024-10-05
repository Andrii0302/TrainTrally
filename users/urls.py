from django.urls import path
from . import views
urlpatterns = [
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', views.LogoutUserView.as_view(), name='logout'),
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('profiles/', views.ProfilesView.as_view(), name='profiles'),
    path('profile/<uuid:pk>/', views.UserProfileView.as_view(), name='profile-detail'),
    path('account/', views.UserAccountView.as_view(), name='account'),
    path('edit-account/', views.UserEditAccountView.as_view(), name='edit-account'),
]

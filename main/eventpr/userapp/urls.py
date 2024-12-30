from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),  # Replacing the earlier 'register' with 'signup'
    path('logout/', views.logout, name='logout'),  # Adding logout for user management
]

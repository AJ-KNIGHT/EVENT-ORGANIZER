from django.urls import path
from . import views

app_name = 'userapp'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),  # Replacing the earlier 'register' with 'signup'
    path('logout/', views.logout, name='logout'),  # Adding logout for user management
    path('dashboard/', views.booking_dashboard, name='booking_dashboard'),
    path('submit-change-request/<int:booking_id>/', views.submit_change_request, name='submit_change_request'),
    path('change-requests-dashboard/', views.change_requests_dashboard, name='change_requests_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
]


from django.urls import path
from . import views


app_name = 'userapp'  # Make sure this matches the namespace used in the template

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('change_password/', views.change_password, name='change_password'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('dashboard/', views.booking_dashboard, name='booking_dashboard'),
    path('submit-change-request/<int:booking_id>/', views.submit_change_request, name='submit_change_request'),
    path('change-requests-dashboard/', views.change_requests_dashboard, name='change_requests_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('approve-change-request/<int:request_id>/', views.approve_change_request, name='approve_change_request'),
    path('reject-change-request/<int:request_id>/', views.reject_change_request, name='reject_change_request'),
]

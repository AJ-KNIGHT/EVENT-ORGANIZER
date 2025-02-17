from django.contrib.auth import views as auth_views  # Add this import
from django.urls import path
from . import views
from .views import user_login 
from userapp.views import user_list, delete_user
from django.urls import path
from .views import delete_user
from .views import user_details

app_name = 'userapp'  # Make sure this matches the namespace used in the template

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path("login/", user_login, name="login"),  # ✅ Updated view name
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

    # Password reset paths
    path('password_reset/', views.password_reset, name='password_reset'),
    path('password_reset/done/', views.password_reset_done, name='password_reset_done'),
    path('password_reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('reset/done/', views.password_reset_complete, name='password_reset_complete'),

    # Optionally, handle invalid token
    path('password_reset/invalid/', views.password_reset_invalid, name='password_reset_invalid'),
    path('delete-user/<int:user_id>/', delete_user, name='delete_user'),



    path("delete/<int:user_id>/", delete_user, name="delete_user"),
    


    path('user-list/', user_list, name='user_list'),
    path("user/<int:user_id>/", user_details, name="user_details"),
]

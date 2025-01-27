
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError

from .models import CustomUser, ChangeRequest
from eventapp.models import Booking
from eventapp.forms import ChangeRequestForm
from django.db.models import Sum
from eventpr.utils import send_html_email
from django.contrib.admin.views.decorators import staff_member_required
from .forms import CustomPasswordChangeForm, CustomUserUpdateForm

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomPasswordChangeForm

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import CustomUserUpdateForm  # You need to create this form for updating user data
from django.shortcuts import render

# User registration
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')

        # Check if username and password are provided
        if not username or not password or not confirmpassword:
            messages.error(request, "Username and password are required.")
            return redirect('signup')

        # Check if the passwords match
        if password != confirmpassword:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        # Check if username already exists
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return redirect('signup')

        # Check if email is already taken
        elif CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered.')
            return redirect('signup')

        # Validate password strength (minimum length of 8 characters)
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return redirect('signup')

        try:
            # Create the user
            user_reg = CustomUser.objects.create_user(username=username, email=email, password=password)
            user_reg.save()
            messages.success(request, 'User successfully created! You can now log in.')
            return redirect('login')  # Redirect to login after successful registration

        except ValidationError as e:
            messages.error(request, f"Error: {e}")
            return redirect('signup')

    return render(request, 'signup.html')


# User login
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, "Username and password are required.")
            return redirect('userapp:login')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                auth_login(request, user)
                messages.success(request, 'Login successful!')

                # Redirect to next page or homepage
                next_url = request.GET.get('next', '/')
                return redirect(next_url)
            else:
                messages.error(request, 'Your account is inactive. Please contact support.')
        else:
            messages.error(request, 'Invalid username or password.')

        return redirect('userapp:login')

    return render(request, 'login.html')


# User logout
def logout(request):
    auth_logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('/')  # Redirect to homepage after logout


@login_required
def booking_dashboard(request):
    """
    Display all bookings for the logged-in user.
    """
    user = request.user
    user_bookings = Booking.objects.filter(user=user)

    return render(request, 'booking_dashboard.html', {'user_bookings': user_bookings})


@login_required
def submit_change_request(request, booking_id):
    """
    Handle the submission of a change request for a specific booking.
    """
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == 'POST':
        form = ChangeRequestForm(request.POST)
        if form.is_valid():
            change_request = form.save(commit=False)
            change_request.booking = booking
            change_request.user = request.user
            change_request.save()

            # Notify admin via email
            context = {
                'booking_id': booking.id,
                'request_type': change_request.get_request_type_display(),
                'new_value': change_request.new_value,
                'user': request.user,
            }
            send_html_email(
                subject="Change Request Submitted",
                recipient_list=['amal183626@gmail.com'],
                template_name='emails/change_request_notification.html',
                context=context,
            )

            messages.success(request, "Your change request has been submitted successfully.")
            return redirect('userapp:change_requests_dashboard')  # Adjust the redirect as needed
    else:
        form = ChangeRequestForm()

    return render(request, 'submit_change_request.html', {'booking': booking, 'form': form})


@login_required
def change_requests_dashboard(request):
    """
    Display all change requests submitted by the logged-in user.
    """
    change_requests = ChangeRequest.objects.filter(user=request.user)

    return render(request, 'change_request_dashboard.html', {'change_requests': change_requests})


@staff_member_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('userapp:booking_dashboard')

    # Statistics
    total_bookings = Booking.objects.count()
    total_revenue = Booking.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    pending_requests_count = ChangeRequest.objects.filter(status='Pending').count()

    # Pending Change Requests
    pending_requests = ChangeRequest.objects.filter(status='Pending')

    context = {
        'total_bookings': total_bookings,
        'total_revenue': total_revenue,
        'pending_requests_count': pending_requests_count,
        'pending_requests': pending_requests,
    }

    return render(request, 'admin_dashboard.html', context)


@login_required
def approve_change_request(request, request_id):
    if not request.user.is_staff:
        return redirect('userapp:booking_dashboard')

    change_request = get_object_or_404(ChangeRequest, id=request_id, status='Pending')
    change_request.status = 'Approved'
    change_request.save()

    # Send email notification
    context = {'change_request': change_request}
    send_html_email(
        subject="Change Request Approved",
        recipient_list=[change_request.user.email],
        template_name='emails/change_request_approved.html',
        context=context,
    )

    messages.success(request, f"Change request #{change_request.id} has been approved.")
    return redirect('userapp:admin_dashboard')


@login_required
def reject_change_request(request, request_id):
    if not request.user.is_staff:
        return redirect('userapp:booking_dashboard')

    change_request = get_object_or_404(ChangeRequest, id=request_id, status='Pending')
    change_request.status = 'Rejected'
    change_request.save()

    # Send email notification
    context = {'change_request': change_request}
    send_html_email(
        subject="Change Request Rejected",
        recipient_list=[change_request.user.email],
        template_name='emails/change_request_rejected.html',
        context=context,
    )

    messages.error(request, f"Change request #{change_request.id} has been rejected.")
    return redirect('userapp:admin_dashboard')




def profile(request):
    return render(request, 'profile.html')


@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()  # This will change the password
            messages.success(request, 'Your password has been changed successfully!')
            return redirect('userapp:profile')  # Redirect to the profile page after successful password change
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomPasswordChangeForm(user=request.user)
    
    return render(request, 'password_change_form.html', {'form': form})



@login_required
def update_profile(request):
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, request.FILES, instance=request.user)  # Include request.FILES
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('userapp:profile')  # Assuming the profile page is named 'profile'
    else:
        form = CustomUserUpdateForm(instance=request.user)

    return render(request, 'update_profile.html', {'form': form})



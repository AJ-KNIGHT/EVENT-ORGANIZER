from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.mail import send_mail

from .models import CustomUser , ChangeRequest
from eventapp.models import Booking
from eventapp.forms import ChangeRequestForm


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

        # Check if username and password are provided
        if not username or not password:
            messages.error(request, "Username and password are required.")
            return redirect('login')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('/')  # Redirect to homepage after login
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')

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
    print(f"Logged-in user: {user}")
    user_bookings = Booking.objects.filter(user=user)
    print(f"User bookings: {user_bookings}")  # Debugging output to check if bookings are fetched

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
            change_request = form.save(commit=False)  # Create a ChangeRequest instance but don't save it yet
            change_request.booking = booking  # Associate the booking
            change_request.user = request.user  # Associate the user
            change_request.save()  # Save the instance to the database

            # Notify admin via email
            send_mail(
                subject="Change Request Submitted",
                message=f"A change request has been submitted for booking {booking.id}.\n"
                        f"Request Type: {change_request.get_request_type_display()}\n"
                        f"New Value/Details: {change_request.new_value}",
                from_email='eventpro49@gmail.com',
                recipient_list=['amal183626@gmail.com']
            )

            messages.success(request, "Your change request has been submitted successfully.")
            return redirect('userapp:change_request_dashboard')  # Adjust the redirect as needed
    else:
        form = ChangeRequestForm()

    return render(request, 'submit_change_request.html', {'booking': booking, 'form': form})


@login_required
def change_requests_dashboard(request):
    """
    Display all change requests submitted by the logged-in user.
    """
    change_requests = ChangeRequest.objects.filter(user=request.user)
    print(change_requests)

    return render(request, 'change_request_dashboard.html', {'change_requests': change_requests})

@login_required
def admin_dashboard(request):
    """
    Display all bookings for admin review.
    Only accessible by staff users.
    """
    if not request.user.is_staff:
        return redirect('userapp:booking_dashboard')

    bookings = Booking.objects.all()
    return render(request, 'admin_dashboard.html', {'bookings': bookings})



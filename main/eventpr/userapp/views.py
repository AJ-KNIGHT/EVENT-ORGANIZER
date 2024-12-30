from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .models import CustomUser
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator

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

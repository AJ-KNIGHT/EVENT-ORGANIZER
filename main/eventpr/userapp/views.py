
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.utils.timezone import now
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
            request.toast_type = 'warning'
            request.toast_message = 'Username and password are required!'
            messages.error(request, "Username and password are required.")
            return redirect('userapp:signup')

        # Check if the passwords match
        if password != confirmpassword:
            request.toast_type = 'error'
            request.toast_message = 'Passwords do not match!'
            messages.error(request, "Passwords do not match.")
            return redirect('userapp:signup')

        # Check if username already exists
        if CustomUser.objects.filter(username=username).exists():
            request.toast_type = 'error'
            request.toast_message = 'Username is already taken!'
            messages.error(request, 'Username is already taken.')
            return redirect('userapp:signup')

        # Check if email is already taken
        elif CustomUser.objects.filter(email=email).exists():
            request.toast_type = 'error'
            request.toast_message = 'Email is already registered!'
            messages.error(request, 'Email is already registered.')
            return redirect('userapp:signup')

        # Validate password strength (minimum length of 8 characters)
        if len(password) < 8:
            request.toast_type = 'error'
            request.toast_message = 'Password must be at least 8 characters long.'
            messages.error(request, "Password must be at least 8 characters long.")
            return redirect('userapp:signup')

        try:
            # Create the user
            user_reg = CustomUser.objects.create_user(username=username, email=email, password=password)
            user_reg.save()
            request.toast_type = 'success'
            request.toast_message = 'User successfully created! You can now log in..'
            messages.success(request, 'User successfully created! You can now log in.')
            return redirect('userapp:login')  # Redirect to login after successful registration

        except ValidationError as e:
            messages.error(request, f"Error: {e}")
            return redirect('userapp:signup')

    return render(request, 'userapp/signup.html',)


# User login
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect

def user_login(request):
    

    if request.method == "POST":
        username = request.POST.get("username")  # Avoid KeyError
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        

        if user is not None:
            login(request, user)  # ✅ Correct usage
            request.toast_type = 'warninh'
            request.toast_message = 'Login successful'
            messages.success(request, "Login successful!")
            return redirect("index")  # ✅ Redirect to the home page
        else:
            request.toast_type = 'warning'
            request.toast_message = '"Invalid username or password. Forgot password?'
            messages.error(request, "Invalid username or password. Forgot password?")
            return render(request, "userapp/login.html", {"show_forgot_password": True})  # ✅ Pass variable

    return render(request, "userapp/login.html",)





# User logout
def logout(request):
    auth_logout(request)
    request.toast_type = 'success'
    request.toast_message = 'Logged out successfully'
    messages.success(request, 'Logged out successfully!')
    

    return redirect('/')  # Redirect to homepage after logout


@login_required
def booking_dashboard(request):
    """
    Display all bookings for the logged-in user.
    """
    user = request.user
    user_bookings = Booking.objects.filter(user=user)

    return render(request, 'eventapp/booking_dashboard.html', {'user_bookings': user_bookings})


@login_required
def submit_change_request(request, booking_id):
    """
    Handle the submission of a change request for a specific booking or booking cancellation.
    """
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == 'POST':
        if 'cancel_booking' in request.POST:
            # Handle booking cancellation
            booking.delete()

            # Notify admin about cancellation
            send_html_email(
                subject="Booking Cancellation",
                recipient_list=['amal183626@gmail.com'],
                template_name='email/booking_cancellation_notification.html',
                context={'booking_id': booking_id, 'user': request.user},
            )

            messages.success(request, "Your booking has been canceled successfully.")
            return redirect('userapp:change_requests_dashboard')

        # Handle change request
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
                template_name='email/change_request_notification.html',
                context=context,
            )

            messages.success(request, "Your change request has been submitted successfully.")
            return redirect('userapp:change_requests_dashboard')
    else:
        form = ChangeRequestForm()

    return render(request, 'eventapp/submit_change_request.html', {'booking': booking, 'form': form})



@login_required
def change_requests_dashboard(request):
    """
    Display all change requests submitted by the logged-in user.
    """
    change_requests = ChangeRequest.objects.filter(user=request.user)

    return render(request, 'eventapp/change_request_dashboard.html', {'change_requests': change_requests})


@staff_member_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('userapp:booking_dashboard')

    # Statistics
    total_bookings = Booking.objects.count()
    total_revenue = Booking.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    pending_requests_count = ChangeRequest.objects.filter(status='Pending').count()

    # Pending Change Requests
    pending_requests = ChangeRequest.objects.filter(status='Pending').order_by('-created_at')

    # User List
    users = CustomUser.objects.all().order_by('-date_joined')

    context = {
        'total_bookings': total_bookings,
        'total_revenue': total_revenue,
        'pending_requests_count': pending_requests_count,
        'pending_requests': pending_requests,
        'users': users,  # Pass users to the template
    }

    return render(request, 'userapp/admin_dashboard.html', context)




@login_required
def approve_change_request(request, request_id):
    if not request.user.is_staff:
        return redirect('userapp:booking_dashboard')

    change_request = get_object_or_404(ChangeRequest, id=request_id, status='Pending')
    change_request.status = 'Approved'
    change_request.save()

    # Send   notification
    context = {'change_request': change_request}
    send_html_email(
        subject="Change Request Approved",
        recipient_list=[change_request.user.email],
        template_name='email/change_request_approved.html',
        context=context,
    )
    request.toast_type = 'success'
    request.toast_message = f"Change request #{change_request.id} has been approved."
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
        template_name='email/change_request_rejected.html',
        context=context,
    )
    request.toast_type = 'error'
    request.toast_message = f"Change request #{change_request.id} has been rejected."
    messages.error(request, f"Change request #{change_request.id} has been rejected.")
    return redirect('userapp:admin_dashboard',)



@login_required
def profile(request):
    return render(request, 'userapp/profile.html', {'timestamp': now().timestamp()})


from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib import messages
from userapp.forms import CustomPasswordChangeForm  # Ensure you have this form imported

@login_required
def change_password(request):

    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep the user logged in after password change
            request.toast_type = 'success'
            request.toast_message = '✅ Your password has been changed successfully!'
            #messages.success(request, '✅ Your password has been changed successfully!')
            return redirect('userapp:profile')  # Redirect to the profile page
        else:
            request.toast_type = 'error'
            request.toast_message = '✅ ⚠️ Please correct the error below'
            messages.error(request, '⚠️ Please correct the error below.')
    else:
        form = CustomPasswordChangeForm(user=request.user)
    
    return render(request, 'userapp/password_change_form.html', {'form': form,})

from django.shortcuts import render, get_object_or_404
from userapp.models import CustomUser



from django.shortcuts import render, get_object_or_404
from userapp.models import CustomUser
from eventapp.models import Booking
from django.utils.timezone import now
from django.utils import timezone

from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import CustomUser, Booking

def user_details(request, user_id):
    # Fetch the user or return a 404 if not found
    user = get_object_or_404(CustomUser, id=user_id)

    # Get the total number of bookings for this user
    total_bookings = Booking.objects.filter(user=user).count()

    # Initialize the upcoming_event as None
    upcoming_event = None

    try:
        # Fetch the user's upcoming event (if any)
        upcoming_event = Booking.objects.filter(user=user, event_date__gte=timezone.now()).order_by('event_date').first()
    except Booking.DoesNotExist:
        upcoming_event = None

    # Initialize the event_slug variable
    event_slug = None

    # Check if there's an upcoming event and if it has a valid slug
    if upcoming_event and upcoming_event.event_name and upcoming_event.event_name.slug:
        event_slug = upcoming_event.event_name.slug

    print(upcoming_event)  # Debugging: Print the upcoming_event

    # Return the rendered page with the necessary context
    return render(
        request,
        "userapp/user_details.html",
        {
            "user": user,
            "total_bookings": total_bookings,
            "upcoming_event": upcoming_event,
            "event_slug": event_slug,  # Pass the event slug to the template
        },
    )



from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from userapp.forms import CustomUserUpdateForm

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, request.FILES, instance=request.user)  
        if form.is_valid():
            form.save()
            request.toast_type = 'success'
            request.toast_message = '✅ YYour profile has been updated successfully!'
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('userapp:profile')  # Ensure 'profile' URL exists in your urls.py
        else:
            request.toast_type = 'error'
            request.toast_message = ' Please correct the errors below.!'
            messages.error(request, "Please correct the errors below.")  # Show validation errors
    else:
        form = CustomUserUpdateForm(instance=request.user)
     

    return render(request, 'userapp/update_profile.html', {'form': form,})


from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

User = get_user_model()

@login_required
@csrf_exempt
def delete_user(request, user_id):
    if request.method == "POST":
        user = get_object_or_404(User, id=user_id)
        
        if user.is_superuser:  # Prevent accidental deletion of superusers
            return JsonResponse({"success": False, "error": "Superusers cannot be deleted!"})

        user.delete()
        return JsonResponse({"success": True})
    
    return JsonResponse({"success": False, "error": "Invalid request"})




@login_required
def user_list(request):
    users = CustomUser.objects.all()  # Adjust this based on your user model
    return render(request, 'userapp/user_list.html', {'users': users})


from django.shortcuts import render, redirect
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import update_session_auth_hash
from userapp.models import CustomUser  # Ensure you are importing your custom user model

# Password Reset Form (Step 1)
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site

# Password Reset Form (Step 1)
def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            users = CustomUser.objects.filter(email=email)
            print(f"Found {len(users)} users with email: {email}")  # Debug print
            for user in users:
                print(f"Generating token for user: {user.username}")  # Debug print
                # Create the reset token and encode the user ID
                uid = urlsafe_base64_encode(str(user.pk).encode())
                token = default_token_generator.make_token(user)

                # Generate the reset URL
                reset_url = f"http://{get_current_site(request).domain}/user/password_reset/{uid}/{token}/"
                
                # Create the HTML message using the template
                message = render_to_string(
                    'registration/password_reset_email.html',  # Make sure the template is correct
                    {'reset_url': reset_url, 'user': user}
                )

                # Send the email with the HTML content
                send_mail(
                    'Password Reset Request',
                    'If you are seeing this, your email client does not support HTML.',  # Plain-text fallback
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                    html_message=message  # The HTML version of the message
                )
                print(f"Sent email to: {email}")  # Debug print
            return redirect('userapp:password_reset_done')  # Redirect to done view
        else:
            print("Form is not valid.")  # Debug print
    else:
        form = PasswordResetForm()

    return render(request, 'registration/password_reset_form.html', {'form': form})


# Password Reset Done (Step 2)
def password_reset_done(request):
    return render(request, 'registration/password_reset_done.html')

# Password Reset Confirm (Step 3)
def password_reset_confirm(request, uidb64, token):
    try:
        # Decode the user ID from the URL
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
    except (CustomUser.DoesNotExist, ValueError):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)  # Keep the user logged in after changing the password
                return redirect('userapp:password_reset_complete')  # Redirect to password reset complete view
        else:
            form = SetPasswordForm(user)
        return render(request, 'registration/password_reset_confirm.html', {'form': form})

    return redirect('userapp:password_reset_invalid')

# Password Reset Complete (Step 4)
def password_reset_complete(request):
    return render(request, 'registration/password_reset_complete.html')

# Optional Invalid Token View (Step 5)
def password_reset_invalid(request):
    return render(request, 'registration/password_reset_invalid.html')


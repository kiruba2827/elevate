from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .models import UserProfile
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

# View to approve a user
@login_required(login_url="my-login")
def admin_approve_user(request, user_id):
    if request.user.is_superuser:
        user_profile = UserProfile.objects.get(user__id=user_id)
        
        # Approve the user and send an email
        user_profile.is_approved = True
        user_profile.save()

        # Send an email notification to the user
        send_mail(
            'Your Account has been Approved',
            'Dear {},\n\nYour account has been approved. You can now log in and use the system.'.format(user_profile.user.username),
            settings.DEFAULT_FROM_EMAIL,
            [user_profile.user.email],
            fail_silently=False,
        )

        return redirect('dashboard')
    else:
        return redirect('final')

# View to reject a user
def reject_user(request, user_id):
    if request.user.is_authenticated:
        user_profile = get_object_or_404(UserProfile, user_id=user_id)

        # Reject the user and update their status
        user_profile.is_approved = False
        user_profile.is_rejected = True
        user_profile.save()  # Make sure the save() is called

        # Optionally, delete the actual User object from the User model
        user_profile.user.delete()

        return redirect('dashboard')
    else:
        return redirect('login')

import json
from django.shortcuts import render
from .models import ImportantEvent

def homepage(request):
    events = ImportantEvent.objects.all()

    events_data = [
        {
            'id': event.id,  # Ensure ID is included
            'title': event.title,
            'date': event.date.strftime('%Y-%m-%d') if event.date else "No Date",  # Change 'start' to 'date'
            'description': event.description or "No description available",
        }
        for event in events
    ]

    

    return render(request, 'crm/index.html', {'events_data': json.dumps(events_data)})





from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ImportantEvent
from datetime import datetime
import json

# View to add events
@csrf_exempt
def add_event(request):
    if request.method == "POST":
        # Load the data from the request body
        data = json.loads(request.body)
        title = data.get("title")
        date_str = data.get("date")  # This is the string date
        description = data.get("description", "")

        # Convert the string date to a datetime object
        try:
            event_date = datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            return JsonResponse({"error": "Invalid date format"}, status=400)

        # Create the event in the database
        event = ImportantEvent.objects.create(title=title, date=event_date, description=description)

        return JsonResponse({
            "message": "Event added successfully!",
            "event": {
                "id": event.id,  # Including event ID for possible deletion later
                "title": event.title,
                "date": event.date.strftime('%Y-%m-%d'),
                "description": event.description,
            },
        })
    return JsonResponse({"error": "Invalid request"}, status=400)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ImportantEvent
import json

# View to delete an event based on title and date
@csrf_exempt
def delete_event(request):
    if request.method == "POST":
        # Load the data from the request body
        data = json.loads(request.body)
        title = data.get("title")
        date_str = data.get("date")

        if not title or not date_str:
            return JsonResponse({"error": "Event title and date are required"}, status=400)

        # Convert the string date to a datetime object
        try:
            event_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({"error": "Invalid date format"}, status=400)

        # Try to find the event based on title and date
        try:
            event = ImportantEvent.objects.get(title=title, date=event_date)
            event.delete()
            return JsonResponse({"message": "Event deleted successfully!"})
        except ImportantEvent.DoesNotExist:
            return JsonResponse({"error": "Event not found"}, status=404)

    return JsonResponse({"error": "Invalid request"}, status=400)



# View for user registration
def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(
                user=user,
                age=form.cleaned_data.get('age'),
                gender=form.cleaned_data.get('gender'),
                date_of_birth=form.cleaned_data.get('date_of_birth')
            )
            return redirect("my-login")
    context = {'registerform': form}
    return render(request, 'crm/register.html', context)

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm

def my_login(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return JsonResponse({'redirect_url': '/dashboard/'})  # Redirect after login

        # If form is invalid, return form HTML with errors
        return JsonResponse({'form_html': render(request, 'crm/my-login.html', {'loginform': form}).content.decode()})

    return render(request, 'crm/my-login.html', {'loginform': form})




# View for logout
def user_logout(request):
    logout(request)
    return redirect('final')

# View for final page
def final_view(request):
    return render(request, 'crm/final.html')

from django.shortcuts import render, redirect
from django.db.models import Count, Q
from .models import UserProfile
from django.contrib.auth.decorators import login_required


from django.db.models import Count, Q
from django.db import connection

@login_required(login_url="my-login")
def dashboard(request):
    if request.user.is_superuser:
        # Fetch total users
        total_users = UserProfile.objects.count()

        # Fetch approved users
        approved_users = UserProfile.objects.filter(is_approved=True).count()

        # Fetch pending users (users who are neither approved nor rejected)
        pending_users = UserProfile.objects.filter(is_approved=False, is_rejected=False).count()

        # Fetch rejected users
        rejected_users = UserProfile.objects.filter(is_rejected=True).count()

        # Weekly data aggregation based on 'created_at'
        weekly_data = UserProfile.objects.extra(
            select={'week': "strftime('%Y-%W', created_at)"}  # This groups by year and week
        ).values('week').annotate(
            approved_count=Count('id', filter=Q(is_approved=True)),
            rejected_count=Count('id', filter=Q(is_rejected=True)),
            pending_count=Count('id', filter=Q(is_approved=False, is_rejected=False))
        ).order_by('week')

        labels = [f"Week {entry['week']}" for entry in weekly_data]
        approved_users_weekly = [entry['approved_count'] for entry in weekly_data]
        rejected_users_weekly = [entry['rejected_count'] for entry in weekly_data]
        pending_users_weekly = [entry['pending_count'] for entry in weekly_data]

        # Fetch all users for the table
        users = UserProfile.objects.all()

        context = {
            'total_users': total_users,
            'approved_users': approved_users,
            'pending_users': pending_users,
            'rejected_users': rejected_users,
            'users': users,
            'labels': labels,
            'approved_users_weekly': approved_users_weekly,
            'rejected_users_weekly': rejected_users_weekly,
            'pending_users_weekly': pending_users_weekly,
        }

        return render(request, 'crm/dashboard.html', context)
    else:
        return redirect('final')


from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile


@login_required(login_url="my-login")
def update_users(request):
    if request.method == "POST":
        for key, value in request.POST.items():
            # Handle email updates
            if key.startswith("email_"):
                user_id = key.split("_")[1]
                user = User.objects.get(id=user_id)
                user.email = value
                user.save()
            
            # Handle gender updates
            elif key.startswith("gender_"):
                user_id = key.split("_")[1]
                user_profile = UserProfile.objects.get(user_id=user_id)
                user_profile.gender = value
                user_profile.save()
            
            # Handle date of birth updates
            elif key.startswith("dob_"):
                user_id = key.split("_")[1]
                user_profile = UserProfile.objects.get(user_id=user_id)
                user_profile.date_of_birth = value
                user_profile.save()

            # Handle approve action
            elif key.startswith("approve_"):
                user_id = key.split("_")[1]
                user_profile = UserProfile.objects.get(user_id=user_id)
                user_profile.is_approved = True
                user_profile.is_rejected = False
                user_profile.save()
            
            # Handle reject action
            elif key.startswith("reject_"):
                user_id = key.split("_")[1]
                user_profile = UserProfile.objects.get(user_id=user_id)
                user_profile.is_approved = False
                user_profile.is_rejected = True
                user_profile.save()

        # Add a success message
        messages.success(request, "User details updated successfully!")

        # Redirect back to the dashboard after processing all updates
        return redirect("dashboard")
from django.shortcuts import render
from django.http import HttpResponse

def home1(request):
    return render(request, 'crm/home1.html')

def home2(request):
    return render(request, 'crm/home2.html')

def home3(request):
    return render(request, 'crm/home3.html')

def about_us(request):
    return render(request, 'crm/about_us.html')

def our_mission(request):
    return render(request, 'crm/our_mission.html')

def our_team(request):
    return render(request, 'crm/our_team.html')

def email_us(request):
    return render(request, 'crm/email_us.html')

def call_us(request):
    return render(request, 'crm/call_us.html')

def visit_us(request):
    return render(request, 'crm/visit_us.html')


# Services Views
def service1(request):
    return render(request, 'crm/service1.html')

def service2(request):
    return render(request, 'crm/service2.html')

def service3(request):
    return render(request, 'crm/service3.html')

from django.shortcuts import render

def service4(request):
    return render(request, 'crm/service4.html')  # Ensure path is correct


# Downloads Views
def download1(request):
    return HttpResponse("Download 1 Page")  # Replace with actual file download logic

def download2(request):
    return HttpResponse("Download 2 Page")  # Replace with actual file download logic

def download3(request):
    return HttpResponse("Download 3 Page")  

from django.http import JsonResponse

def check_authentication(request):
    if request.user.is_authenticated:
        user_data = {
            'username': request.user.username,
            'email': request.user.email,
            'is_staff': 'Yes' if request.user.is_staff else 'No',
            'profile_picture': request.user.profile.picture.url if hasattr(request.user, 'profile') else None
        }
        return JsonResponse({'is_authenticated': True, 'user_data': user_data})
    else:
        return JsonResponse({'is_authenticated': False})

from django.shortcuts import render

def request_internet_access(request):
    return render(request, 'crm/request_internet_access.html')

from django.shortcuts import render

def whitelist_ip(request):
    return render(request, 'crm/whitelist_ip.html')


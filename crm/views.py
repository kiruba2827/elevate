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
# View for the homepage
def homepage(request):
    return render(request, 'crm/index.html')

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

# View for login
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
                return redirect("dashboard")

    context = {'loginform': form}
    return render(request, 'crm/my-login.html', context=context)

# View for logout
def user_logout(request):
    logout(request)
    return redirect('final')

# View for final page
def final_view(request):
    return render(request, 'crm/final.html')

# View for dashboard (ensure only one definition of this view)
@login_required(login_url="my-login")
def dashboard(request):
    # Ensure the user is an admin
    if request.user.is_superuser:
        # Fetch total users
        total_users = UserProfile.objects.count()

        # Fetch approved users
        approved_users = UserProfile.objects.filter(is_approved=True).count()

        # Fetch pending users (users who are neither approved nor rejected)
        pending_users = UserProfile.objects.filter(is_approved=False, is_rejected=False).count()

        # Fetch rejected users
        rejected_users = UserProfile.objects.filter(is_rejected=True).count()

        # Fetch all users (you can further filter this if needed)
        users = UserProfile.objects.all()

        # Add statistics to the context
        context = {
            'total_users': total_users,
            'approved_users': approved_users,
            'pending_users': pending_users,
            'rejected_users': rejected_users,
            'users': users,
        }

        return render(request, 'crm/dashboard.html', context)
    else:
        return redirect('final')

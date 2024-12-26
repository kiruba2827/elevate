from django.shortcuts import render,redirect

from . forms import CreateUserForm, LoginForm

from django.contrib.auth.models import auth

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required


from django.contrib.auth import logout



from .models import UserProfile

def homepage(request):
    
    return render(request, 'crm/index.html')

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

def my_login(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(data=request.POST)  # Pass only `data=request.POST`

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("dashboard")

    context = {'loginform': form}
    return render(request, 'crm/my-login.html', context=context)

    
    
    
    return render(request, 'crm/my-login.html', context=context)


def user_logout(request):
    # Log out and clear the session
    logout(request)
    request.session.flush()

    # Redirect to the final page
    return redirect('final')



def final_view(request):
    return render(request, 'crm/final.html')






@login_required(login_url="my-login")
def dashboard(request):
    
    return render(request, 'crm/dashboard.html')




from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth

# Create your views here.

def register(request):
    # POST not GET
    if request.method == "POST":
        # Password match
        if request.POST['password1'] == request.POST['password2']:
            try:
                # Does the user already exist
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'accounts/register.html', {'error': "Username has already been taken"})
                # Does not already exist
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                auth.login(request, user)
                return redirect('home')
        # Passwords didn't match
        else:
            return render(request, 'accounts/register.html', {'error': "Passwords must match"})
    # GET ie registration request
    else:
        return render(request, "accounts/register.html")

def login(request):
    # POST or GET request
    message=''
    context = {'message': message,}
    if request.method == 'POST':
       user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
       if user is not None:
           auth.login(request, user)
           message = 'Login successful'
           return redirect('home')
       else:
           message = 'Username and or Password incorrect'
           return render(request,'accounts/login.html', {'message': message})         
    else:
        return render(request,'accounts/login.html')

def logout(request):
        if request.method == 'POST':
            auth.logout(request)


        # TO DO --> send to home page and logout
        return redirect('home')




    


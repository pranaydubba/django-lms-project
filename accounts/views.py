from django.shortcuts import render,redirect
from .models import MyUser
from .forms import MyUserForm,LoginForm
from django.contrib.auth import authenticate,login as auth_login, logout as auth_logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
# Create your views here.

def redirect_authenticated_user(user):
    if user.role == 'instructor':
        return redirect('instructor_dashboard')
    elif user.role == 'student':
        return redirect('student_dashboard')

def home(request):
    return render(request,'home.html')

def register(request):
    if request.user.is_authenticated:
        return redirect_authenticated_user(request.user)
    userform = MyUserForm()
    if request.method == 'POST':
        userform = MyUserForm(request.POST,request.FILES)
        if userform.is_valid():
            name = userform.cleaned_data['username']
            email = userform.cleaned_data['email']
            ph_no = userform.cleaned_data['ph_no']
            password = userform.cleaned_data['password']
            role = userform.cleaned_data['role']
            bio = userform.cleaned_data.get('bio')
            profile_pic = userform.cleaned_data.get('profile_pic')
            if role == 'student':
                MyUser.manager.create_student(email,username=name,ph_no=ph_no,password=password,role=role,bio=bio,profile_pic=profile_pic)
                return redirect('login')
            elif role == 'instructor':
                MyUser.manager.create_instructor(email,username=name,ph_no=ph_no,password=password,role=role,bio=bio,profile_pic=profile_pic)
                return redirect('login')
            return render(request,'register.html')
        return render(request,'register.html',{'userform':userform})

    userform = MyUserForm()
    return render(request,'register.html',{'userform':userform})

def login(request):
    if request.user.is_authenticated:
        return redirect_authenticated_user(request.user)
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(email = login_form.cleaned_data['email'],
                                password = login_form.cleaned_data['password'])
            if user is not None:
                if user.is_instructor and not user.is_approved:
                    return HttpResponse('Your account is not approved by admin yet')
                auth_login(request,user)
                if request.user.is_authenticated:
                    return redirect_authenticated_user(request.user)
            else:
                return HttpResponse('Invalid credentials')
    login_form = LoginForm()
    return render(request,'login.html',{'login_form':login_form})

@login_required
def logout(request):
    auth_logout(request)
    return redirect('login')

@login_required
def profile(request):
    user = request.user
    if request.method == 'POST':
        form = MyUserForm(request.POST, request.FILES, instance=user)
        form.fields.pop('password')
        form.fields.pop('role')
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = MyUserForm(instance=user)
        form.fields.pop('password')
        form.fields.pop('role')
    return render(request, 'profile.html', {'user_obj': user,'form': form})

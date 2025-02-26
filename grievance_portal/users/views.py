from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import StudentRegistrationForm, CustomLoginForm
from .models import User
from grievances.models import Grievance  

def register_view(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(request, email=form.cleaned_data.get('email'), password=raw_password)  # ✅ FIX: Use `email`
            login(request, user)
            return redirect('student_dashboard')
    else:
        form = StudentRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if user.user_type == 'student':
                return redirect('student_dashboard')
            else:  # Admin user
                return redirect('admin_dashboard')
    else:
        form = CustomLoginForm()
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out. Please log in to continue.")
    return redirect('login')


@login_required
def student_dashboard(request):
    if request.user.user_type != 'student':
        return redirect('admin_dashboard')
    
    grievances = request.user.grievances.all()
    return render(request, 'users/student_dashboard.html', {'grievances': grievances})

@login_required
def admin_dashboard(request):
    if request.user.user_type != 'admin':
        return redirect('student_dashboard')
    
    # Filter grievances based on admin role
    admin_role = request.user.admin_role
    category_map = {
        'hostel': 'Hostel',
        'infra': 'Infrastructure',
        'exam': 'Examination'
    }

    grievances = None
    if admin_role in category_map:
        grievances = Grievance.objects.filter(category__name=category_map[admin_role])  # ✅ FIX: Use ForeignKey relationship

    return render(request, 'users/admin_dashboard.html', {'grievances': grievances})

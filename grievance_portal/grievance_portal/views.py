from django.shortcuts import render



def login(request):
    return render(request, 'users/login.html')

def submit_grievance(request):
    return render(request, 'grievances/submit_grievance.html')

def student_dashboard(request):
    return render(request, 'grievances/student/dashboard.html')

def logout(request):
    return render(request,'users/login.html')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Grievance, GrievanceResponse
from .forms import GrievanceForm, GrievanceResponseForm
from django.contrib import messages

@login_required
def create_grievance(request):
    if request.user.user_type != 'student':
        messages.error(request, "Only students can submit grievances.")
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        form = GrievanceForm(request.POST)
        if form.is_valid():
            grievance = form.save(commit=False)
            grievance.student = request.user
            grievance.save()
            messages.success(request, "Grievance submitted successfully!")
            return redirect('student_dashboard')
    else:
        form = GrievanceForm()
    
    return render(request, 'grievances/create_grievance.html', {'form': form})

@login_required
def grievance_detail(request, pk):
    grievance = get_object_or_404(Grievance, pk=pk)
    
    # Check permissions
    if request.user.user_type == 'student' and grievance.student != request.user:
        messages.error(request, "You don't have permission to view this grievance.")
        return redirect('student_dashboard')
    elif request.user.user_type == 'admin' and request.user.admin_role != grievance.category:
        messages.error(request, "This grievance doesn't belong to your department.")
        return redirect('admin_dashboard')
    
    responses = grievance.responses.all().order_by('created_at')
    
    # Admin can add responses
    form = None
    if request.user.user_type == 'admin':
        if request.method == 'POST':
            form = GrievanceResponseForm(request.POST)
            if form.is_valid():
                response = form.save(commit=False)
                response.grievance = grievance
                response.admin = request.user
                response.save()
                
                # Update grievance status to in_progress if it was pending
                if grievance.status == 'pending':
                    grievance.status = 'in_progress'
                    grievance.save()
                
                messages.success(request, "Response added successfully!")
                return redirect('grievance_detail', pk=pk)
        else:
            form = GrievanceResponseForm()
    
    return render(request, 'grievances/grievance_detail.html', {
        'grievance': grievance,
        'responses': responses,
        'form': form
    })

@login_required
def mark_resolved(request, pk):
    grievance = get_object_or_404(Grievance, pk=pk)
    
    # Only the admin of the respective category can mark as resolved
    if request.user.user_type == 'admin' and request.user.admin_role == grievance.category:
        grievance.status = 'resolved'
        grievance.save()
        messages.success(request, "Grievance marked as resolved!")
    else:
        messages.error(request, "You don't have permission to perform this action.")
    
    return redirect('grievance_detail', pk=pk)
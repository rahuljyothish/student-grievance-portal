from django.db import models
from users.models import User

class GrievanceCategory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Grievance(models.Model):
    CATEGORY_CHOICES = [
        ('hostel', 'Hostel'),
        ('infra', 'Infrastructure'),
        ('exam', 'Examination'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='grievances')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.get_category_display()} ({self.get_status_display()})"
    
    class Meta:
        ordering = ['-created_at']

class GrievanceResponse(models.Model):
    grievance = models.ForeignKey(Grievance, on_delete=models.CASCADE, related_name='responses')
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_responses')
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Response to {self.grievance.title} by {self.admin.email}"
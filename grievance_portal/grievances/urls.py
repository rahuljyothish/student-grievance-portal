from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_grievance, name='create_grievance'),
    path('<int:pk>/', views.grievance_detail, name='grievance_detail'),
    path('<int:pk>/resolve/', views.mark_resolved, name='mark_resolved'),
]
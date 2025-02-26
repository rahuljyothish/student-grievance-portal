from django.contrib import admin

# Register your models here.
from django.contrib import admin
from grievances.models import Grievance, GrievanceCategory, GrievanceResponse
admin.site.register(Grievance)
admin.site.register(GrievanceCategory)
admin.site.register(GrievanceResponse)
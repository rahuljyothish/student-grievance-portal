from django import forms
from .models import Grievance, GrievanceResponse

class GrievanceForm(forms.ModelForm):
    class Meta:
        model = Grievance
        fields = ['category', 'title', 'description']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Grievance Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Detailed description of your grievance'}),
        }

class GrievanceResponseForm(forms.ModelForm):
    class Meta:
        model = GrievanceResponse
        fields = ['response']
        widgets = {
            'response': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your response to this grievance'}),
        }
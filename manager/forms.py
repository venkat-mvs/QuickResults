from django import forms
from .models import StudentsList

class StudentAddForm(forms.ModelForm):
    class Meta:
        model = StudentsList
        fields = ['studentid','name','branch','email_address']
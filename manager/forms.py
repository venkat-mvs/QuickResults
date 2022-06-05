from django import forms
from .models import StudentsList


class StudentEditForm(forms.ModelForm):
    class Meta:
        model = StudentsList
        fields = ['name','branch','email_address', 'mail_sent']

class StudentAddForm(forms.ModelForm):
    class Meta:
        model = StudentsList
        fields = ['studentid','name','branch','email_address']
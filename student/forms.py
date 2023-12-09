from django import forms
from django.contrib.auth.models import User
from . import models
from exam import models as QMODEL

class StudentUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }

class StudentForm(forms.ModelForm):
    tenth_marks = forms.DecimalField(max_digits=5, decimal_places=2, required=False)
    twelfth_marks = forms.DecimalField(max_digits=5, decimal_places=2, required=False)

    class Meta:
        model = models.Student
        fields = ['address', 'mobile', 'profile_pic', 'tenth_marks', 'twelfth_marks', 'graduation_marks', 'graduation_branch']

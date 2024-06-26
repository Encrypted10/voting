from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Nominee

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'election_id']

class AdminUserAddForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'election_id']

class NomineeForm(forms.ModelForm):
    class Meta:
        model = Nominee
        fields = ['name', 'election_id', 'description', 'image_url']

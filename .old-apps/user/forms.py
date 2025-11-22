from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    join_code = forms.CharField(max_length=6, label="FlexPass Join Code")
    email = forms.EmailField(initial="@pchsstudent.org")
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = [
            "join_code",
            "username",
            "email",
            "first_name",
            "last_name",
        ]
        widgets = {
            "password": forms.PasswordInput(),
        }

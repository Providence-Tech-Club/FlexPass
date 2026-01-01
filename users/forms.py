from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser
from rooms.models import Room
from students.models import Student


class RegistrationForm(UserCreationForm):
    join_code = forms.CharField(max_length=6, label="FlexPass Join Code")
    email = forms.EmailField(initial="@pchsstudent.org")
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = [
            "join_code",
            "email",
            "first_name",
            "last_name",
        ]

    def save(self, commit=True) -> None | CustomUser:
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        try:
            join_room = Room.objects.get(join_code=self.cleaned_data["join_code"])
        except Room.DoesNotExist:
            return None
        else:
            if not commit:
                return user

            user.save()

            student = Student.objects.create(
                user=user,
                flex_room=join_room,
            )

            student.set_room(join_room)

        return user


class AuthenticationForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError("Invalid email or password")

        return self.cleaned_data

    def get_user(self):
        return self.user_cache

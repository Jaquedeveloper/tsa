from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class NewUserForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'square'
            }
        )
    )

    username = forms.CharField(
        required=True, max_length=30,
        widget=forms.TextInput(
            attrs={
                'class': 'square'
            }
        )
    )

    password1 = forms.CharField(
        required=True, max_length=100,
        widget=forms.PasswordInput(
            attrs={
                'class': 'square'
            }
        ),
        label="Password"
    )

    password2 = forms.CharField(
        required=True, max_length=100,
        widget=forms.PasswordInput(
            attrs={
                'class': 'square'
            }
        ),
        label="Repeat password"
    )

    class Meta:
        model = User
        fields = ('username', "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.username = self.cleaned_data['username']
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=30, required=True, label="Username:",
        widget=forms.TextInput(
            attrs={
                'class': 'square'
            }
        )
    )
    password = forms.CharField(
        required=True, label="Password:",
        widget=forms.PasswordInput(
            attrs={
                'class': 'square'
            }
        )
    )
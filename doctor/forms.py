from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile
from .models import Doctor

class DoctorRegistrationForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = [
            'medical_id', 'firstname', 'lastname', 'email',
            'number', 'specialization', 'profile_picture', 'attachments'
        ]

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    phone = forms.CharField(max_length=15)
    country = forms.ChoiceField(choices=Profile.COUNTRY_CHOICES)

    class Meta:
        model = User  # Keep this if you are using the default User model
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Create Profile after saving the User
            profile = Profile.objects.create(
                user=user,
                first_name=self.cleaned_data["first_name"],
                last_name=self.cleaned_data["last_name"],
                phone=self.cleaned_data["phone"],
                country=self.cleaned_data["country"],
            )
            # If Profile is required to have any other fields, you can add them here.
        return user

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class OTPVerificationForm(forms.Form):
    email = forms.EmailField()
    otp = forms.IntegerField()

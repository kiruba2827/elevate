
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.contrib.auth.models import User

from django import forms

from django.forms.widgets import PasswordInput, TextInput

from django.core.exceptions import ValidationError
from datetime import date


from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

from django.core.exceptions import ValidationError
from datetime import date

class CreateUserForm(forms.ModelForm):
    age = forms.IntegerField(required=True)
    gender = forms.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    date_of_birth = forms.DateField(required=True, widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    def clean_date_of_birth(self):
        dob = self.cleaned_data['date_of_birth']
        today = date.today()

        # Ensure the date of birth is not in the future
        if dob > today:
            raise ValidationError("The date of birth cannot be in the future.")

        # Optionally: You can validate the age based on the current date and user's age
        age = self.cleaned_data.get('age')
        if age:
            # Calculate the age based on the birthdate
            calculated_age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            if calculated_age != age:
                raise ValidationError(f"Age does not match the date of birth. Based on the date, the age should be {calculated_age}.")

        return dob

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput())

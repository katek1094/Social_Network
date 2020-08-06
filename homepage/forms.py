from django import forms
from .models import MyUser
from django.contrib.auth.forms import UserCreationForm


class MyUserCreationForm(UserCreationForm):
    date_of_birth = forms.DateField(label="date of birth", widget=forms.SelectDateWidget(years=range(1940, 2020)))

    class Meta(UserCreationForm.Meta):
        model = MyUser
        fields = ("email", 'first_name', 'last_name', 'date_of_birth', 'sex')
        widgets = {
            'sex': forms.RadioSelect()
        }






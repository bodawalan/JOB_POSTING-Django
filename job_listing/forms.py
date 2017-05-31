from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.core import validators
from django.forms import ModelForm
from .models import JobPosting,Filter,User

# If you don't do this you cannot use Bootstrap CSS
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'password'}))

def not_orgs(value):
    value=value.lower()
    if value.endswith('.org'):
        raise forms.ValidationError("Not organization email")


class SuggestionForm(forms.Form):
    name=forms.CharField()
    email=forms.EmailField(validators=[not_orgs])
    verify_Email=forms.EmailField()
    suggestion= forms.CharField(widget=forms.Textarea)
    honeypot=forms.CharField(required=False,
                             widget=forms.HiddenInput ,
                             validators=[validators.MaxLengthValidator(0)])

    def clean_honeypot(self):
        honeypot=self.cleaned_data['honeypot']
        if len(honeypot):
            raise forms.ValidationError(" honey post should be empty")

        return honeypot

    def clean(self):
        cleaned_data=super().clean()
        email=cleaned_data.get('email')
        verify=cleaned_data.get('verify_Email')

        if email != verify:
            raise forms.ValidationError("you need give same email")


class JobPostingForm(forms.ModelForm):
    class Meta:
        model=JobPosting
        fields=['title',
                'number_of_position',
                'level',
                'posting_date',
                'desciption',

        ]

class FilterForm(forms.ModelForm):
    class Meta:
        model=Filter
        fields=[
                'level',
            ]

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ['email', 'password', 'name', 'first_name',  'is_organization']

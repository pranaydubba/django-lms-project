from django.forms import Form,ModelForm
from django import forms
from accounts.models import MyUser

class MyUserForm(forms.ModelForm):
    role = forms.ChoiceField(choices=[
        ('student', 'STUDENT'),
        ('instructor', 'INSTRUCTOR')
    ])
    class Meta:
        model = MyUser  
        fields = ['username', 'password', 'email', 'ph_no','role','bio','profile_pic']
        widgets = {
            'username' : forms.TextInput(attrs={'placeholder' : 'Enter your name ', 'id': 'username'}),
            'password' : forms.TextInput(attrs={'type':'password','placeholder':'enter your password '}),
            'email' : forms.TextInput(attrs={'placeholder' : 'Enter your email ', 'id': 'email'}),
            'ph_no' : forms.TextInput(attrs={'type':'tel','placeholder':'enter your phone no '}),
            'bio' : forms.Textarea(attrs={'placeholder':'About You'}),
        }

        def clean(self):
            cleaned_data = super().clean()
            role = cleaned_data.get('role')
            bio = cleaned_data.get('bio')
            profile_pic = cleaned_data.get('profile_pic')

            if role == 'instructor':
                if not bio:
                    self.add_error('bio', 'Bio is required for instructors.')
                if not profile_pic:
                    self.add_error('profile_pic', 'Profile picture is required for instructors.')

            return cleaned_data


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=150,widget=forms.EmailInput(attrs={'placeholder':'enter your email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'enter password'}))
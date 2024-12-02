from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Bookmark, User, Profile

class BookmarkForm(forms.ModelForm):
    class Meta:
        model = Bookmark
        fields = ['user', 'title', 'url', 'description', 'category', 'tags']
        
        
class UsernameChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']


class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_image']


class EmailChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already in use.')
        return email


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

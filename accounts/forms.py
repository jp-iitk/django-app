from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import UserProfile


class SignUpForm(UserCreationForm):
    email = forms.CharField(
        widget=forms.EmailInput(attrs={'placeholder':'xyz@gmail.com'}),
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Jyoti Prakash'})
        self.fields['password1'].widget.attrs.update({'placeholder': '**********'})
        self.fields['password2'].widget.attrs.update({'placeholder': '**********'})

    class Meta:
        model = User
        fields = ('username','email','password1','password2')


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('profile_pic',)


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email',)


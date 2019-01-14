from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm, UserUpdateForm,ProfileUpdateForm
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy,reverse
from django.contrib import messages


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request,'signup.html',{'form':form})


class UserUpdateView(UpdateView):
    model = User
    fields = ('first_name','last_name','email')
    template_name = 'update_account.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user


def user_profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST,instance=request.user)
        profile_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.userprofile)
        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()
            messages.success(request,f'Profile successfully updated for user {request.user.username}')
            return redirect('user_profile')
    else:
        form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
    return render(request, 'user_profile.html', {'form': form, 'profile_form': profile_form})





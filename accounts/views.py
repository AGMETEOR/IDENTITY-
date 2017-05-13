from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, ExtraDataEditForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib import messages


def user_login(request):
    if request.method=="POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("Account is authenticated")
                else:
                    return HttpResponse("Disabled")
        else:
            return HttpResponse("Invalid")
    else:
        form= LoginForm()
    return render(request, 'accounts/login.html',{'form':form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            profile = Profile.objects.create(user=new_user)
            return render(request, 'accounts/register_done.html',{'new_user':new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'accounts/register.html',{'user_form':user_form})


@login_required
def edit(request):
    
    if request.method == 'POST':
        extra_data_form = ExtraDataEditForm(instance=request.user.profile,data=request.POST)
        if extra_data_form.is_valid():
            extra_data_form.save()
            
            messages.success(request, 'Your Contact Details were successfully updated!')
        else:
            messages.error(request, 'Opps! Failed to update...')
    else:
        extra_data_form = ExtraDataEditForm(instance=request.user.profile)
    return render(request,'accounts/edit.html', {'extra_data_form':extra_data_form})

































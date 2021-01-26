from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from  django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .forms import AccountForm

def signup(request):
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request,'Your account has been successfully created..')
            return redirect('accounts:login')
    return render(request,'accounts/signup.html',{'form':form})


@login_required()
def edit_profile(request):
    if request.method == 'POST':
        form = AccountForm(request.POST,request.FILES,instance=request.user.account)
        if form.is_valid():
            my_form = form.save(commit=False)
            my_form.user = request.user
            my_form.save()
            messages.success(request, 'You account has been modified')
            return redirect('accounts:profile')

    else:
        form = AccountForm(instance=request.user.account)
    print(AccountForm(instance=request.user.account))
    return render(request,'accounts/edit_profile.html',{'form':form})
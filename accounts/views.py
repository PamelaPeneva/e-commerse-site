from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from accounts.forms import CustomUserCreationForm
from django.contrib.auth import login,logout,authenticate


def register(request):
    form = CustomUserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        # print(form.cleaned_data)
        form.save()
        messages.success(request, 'Account created successfully')
        return redirect('login')

    context = {
        'form': form,
    }
    return render(request, 'register.html', context=context)

@login_required(login_url='login')
def loginn(request):
    email = request.GET.get('email')
    password = request.GET.get('password')
    user = authenticate(request, email=email, password=password)
    if user is not None:
        login(request,user)
        return redirect('home')

    return render(request, 'signin.html')

"""
eunjae@abv.bg
123user123

JohnDoe@example.com

admin@abv.bg
"""

def logoutt(request):
    logout(request)
    return redirect('login')
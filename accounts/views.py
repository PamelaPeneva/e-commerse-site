from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login,logout,authenticate
from accounts.forms import CustomUserCreationForm
from accounts.models import CustomUser

from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated.')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid.')
        return redirect('register')


def register(request):
    form = CustomUserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)   # create user object
        user.is_active = False           # deactivate account until email confirmation
        form.save()

        # ACTIVATION
        current_site = get_current_site(request)
        mail_subject = 'Please activate your account'
        message = render_to_string('account_verification_email.html', {
            'user': user,
            'domain': current_site,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),  # A base64 encoded version of the user’s primary key (ID).
            'token': default_token_generator.make_token(user),   # ensures the link is valid only once and expires after some time.
        })
        to_email = user.email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()

        # messages.success(request, 'Account created successfully. Check your email to verify your account')
        return redirect('/accounts/login/?command=verification&email=' + user.email)

    context = {
        'form': form,
    }
    return render(request, 'register.html', context=context)

def loginn(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        print(user)
        if user is not None:
            login(request,user)
            messages.success(request, 'You are now logged in.')
            return redirect('dashboard')

    return render(request, 'signin.html')

@login_required(login_url='login')
def logoutt(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def dashboard(request):
    return render(request, 'dashboard.html')

def forgotPassword(request):
    if request.method == 'POST':
        user_email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email__iexact=user_email)
            current_site = get_current_site(request)
            mail_subject = 'Please reset your password'
            message = render_to_string('password_reset_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            email = EmailMessage(mail_subject, message, to=[user.email])
            email.send()
            messages.success(request, 'Password reset link was sent to your email.')
            return redirect('login')
        except CustomUser.DoesNotExist:
            messages.error(request, "Account doesn't exist.")
            return redirect('forgotPassword')

    return render(request, 'forgotPassword.html')

def resetPassword(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            if (new_password and confirm_password) and (new_password == confirm_password):
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Your password has been reset successfully.')
                return redirect('login')
            else:
                messages.error(request, 'Passwords do not match.')

        return render(request, 'reset_password.html')

    else:
        messages.error(request, 'The reset link is invalid or has expired. Get another one')
        return redirect('forgotPassword')


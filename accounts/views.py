from django.shortcuts import  redirect, reverse
from django.core.mail import send_mail
from django.contrib import messages, auth
from accounts.models import Token

def send_email_view(request):
    email = request.POST['email']
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri(
        reverse('account_login') + '?token=' + str(token.uid)
    )
    message = f'Use this link to log in:\n\n{url}'
    send_mail(
        'Your login link for Superlists',
        message,
        'laurattdd@gmail.com',
        [email]
    )
    messages.success(
        request,
        "Check your email, we've sent you a link you can use to log in."
    )
    return redirect('/')


def login_view(request):
    user = auth.authenticate(uid=request.GET.get('token'))
    if user:
        auth.login(request, user)
    return redirect('/')

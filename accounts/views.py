from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from accounts.models import Account, User
from forms import NewUserForm, LoginForm
from queries.forms import QueryForm
from tsa.utils import json_response


def registration(request):
    if request.user.is_authenticated():
        return redirect(to='profile', permanent=True)

    context = dict(active_tab='registration')
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.account = Account()
            user.account.save()
            request.session['registration_completed'] = True
            return redirect(to='login', permanent=True)
        else:
            context['form'] = form
    else:
        context['form'] = NewUserForm()
    return render(request, 'accounts/registration.html', context)


def _login(request):
    if request.user.is_authenticated():
        return redirect(to='profile', permanent=True)

    context = dict(active_tab='login')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            context['form'] = form
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect(to='profile', permanent=True)
                else:
                    context['notice'] = 'Your account is disabled. Please, contact the administrator'
                    context['type'] = 'warning'

            else:
                context['notice'] = 'Invalid credentials'
                context['type'] = 'error'
        else:
            context['notice'] = 'Invalid credentials'
            context['type'] = 'error'
    else:
        if request.session.get('registration_completed'):
            del request.session['registration_completed']
            context['notice'] = 'You have successfully registered'
            context['type'] = 'success'

        context['form'] = LoginForm()
    return render(request, 'accounts/login.html', context)


@login_required
def profile(request):
    context = dict(active_tab='profile', query_form=QueryForm())
    return render(request, 'accounts/profile.html', context)


@login_required
def _logout(request):
    logout(request)
    return redirect(to='home', permanent=True)


@login_required
def remove_from_group(request):
    if not request.user.account.is_group_admin:
        return json_response({'status': 'error'})

    try:
        user_id = int(request.POST.get('user_id', ''))
    except ValueError:
        return json_response({'status': 'error'})

    user = User.objects.filter(pk=user_id, account__group=request.user.account.group)
    if user.exists():
        user.account.group = None
        return json_response({'status': 'success'})

    return json_response({'status': 'error'})
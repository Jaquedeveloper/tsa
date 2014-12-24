from django.shortcuts import render, redirect

from forms import NewUserForm


def new_user(request):
    context = dict()
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            redirect('login')
        else:
            context['form'] = form
    else:
        context['form'] = NewUserForm()
    return render(request, 'accounts/registration.html', context)


def process_login(request):
    pass
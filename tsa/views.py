from django.shortcuts import render


def index(request):
    context = dict(active_tab='home')
    return render(request, 'index.html', context)
from django.shortcuts import render, redirect
from .forms import AddCigarettesForm, AddPullUpsForm
from .models import *


def index(request):
    return render(request, 'summary_of_the_day/index.html')


def cigarettes(request):
    title = 'Cigarettes'
    log = ''
    if request.method == "POST":
        form = AddCigarettesForm(request.POST)
        if form.is_valid():
            try:
                Cigarettes.objects.create(**form.cleaned_data)
                return redirect("summary_of_the_day:summary_of_the_day_cigarettes_stat")
            except:
                form.add_error(None, """Ошибка добавления в БД. 
                Возможно есть запись за эту дату""")
                title = 'Error'
                log = Cigarettes.objects.all()[:5]
    else:
        form = AddCigarettesForm()
    content = {
        'title': title,
        'form': form,
        'log': log,
    }
    return render(request, 'summary_of_the_day/cigarettes.html', content)


def pullups(request):
    title = "Подтягивания"
    if request.method == "POST":
        form = AddPullUpsForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = AddPullUpsForm()
    content = {
        'title': title,
        'form': form,
        'log': PullUpsModel.objects.all()[:10],
    }
    return render(request, 'summary_of_the_day/pull-ups.html', content)


def cigarettes_stat(request):
    stat = Cigarettes.objects.all()
    url_redirect = 'summary_of_the_day/cigarettes-stat.html'
    return render(request, url_redirect, {'stat': stat})

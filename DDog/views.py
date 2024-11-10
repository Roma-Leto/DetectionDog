from django.shortcuts import render
from django.urls import reverse_lazy


def base_index(request):
    content = {
        'title': 'Главная страница',
    }
    return render(request, 'inventory_items/base.html', content)

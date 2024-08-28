from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

from .models import *
from .forms import *


def index(request):
    smarts = SmartphoneModel.objects.all()
    content = {
        'smarts': smarts
    }
    return render(request, "sandbox1/index.html", content)


def show_category(request, cat_slug):
    # Из заданной модели выбираем объекты по критерию. В данном случае slug'у.
    # либо ошибку 404
    category = get_object_or_404(CategorySmartModel, slug=cat_slug)
    smart = SmartphoneModel.objects.filter(category_id=category.pk)
    context = {
        'title': "Категории",
        'smart': smart
    }
    return render(request, "sandbox1/smart_category.html", context)


class AddSmartphone(CreateView):
    form_class = AddSmartForm
    template_name = 'sandbox1/index.html'
    success_url = reverse_lazy("sandbox1_index")
    extra_context = {
        'title': "Добавление записи"
    }


def smart_details(request, smart_slug):
    smart = SmartphoneModel.objects.get(slug=smart_slug)
    context = {
        'title': "Детали",
        'smart': smart
    }
    return render(request, "sandbox1/smart-details.html", context)

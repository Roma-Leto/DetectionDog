"""
Этот модуль содержит представления для управления предметами инвентаря.
Он включает в себя создание, обновление, удаление и отображение информации о предметах,
категориях, материалах и коробках.
"""
import datetime

from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, DetailView, \
    ListView, DeleteView, UpdateView
from django.views.generic.base import ContextMixin

from .models import ItemModel, CategoryModel, BoxModel, LocationModel, \
    MaterialBoxModel

PAGINATION_VAR = 10


# region Create & Details
class IndexView(TemplateView):
    """Главная страница, отображающая количество предметов."""
    template_name = 'inventory_items/index.html'

    def get_context_data(self, **kwargs):
        """Добавляет количество предметов в контекст."""
        context = super().get_context_data(**kwargs)
        context['count_obl'] = ItemModel.objects.count()
        return context


class CategoryCreateView(CreateView):
    """Представление для создания категории."""
    model = CategoryModel
    fields = ["name"]
    template_name = 'inventory_items/any_create.html'


class CategoryDetailView(DetailView):
    """Представление для отображения деталей категории."""
    model = CategoryModel

    def get_context_data(self, **kwargs):
        """Добавляет список предметов, относящихся к категории."""
        context = super().get_context_data(**kwargs)
        context['items'] = ItemModel.objects.filter(
            categories_id=context['object'].id)
        return context


class LocationCreateView(CreateView):
    """Представление для создания локации."""
    model = LocationModel
    fields = '__all__'
    template_name = 'inventory_items/any_create.html'


class LocationDetailView(DetailView):
    """Представление для отображения деталей локации."""
    model = LocationModel

    def get_context_data(self, **kwargs):
        """Добавляет список предметов и боксов, относящихся к локации."""
        context = super().get_context_data(**kwargs)
        context['items'] = ItemModel.objects.filter(
            location_id=context['object'].id)
        context['box'] = BoxModel.objects.filter(
            location_id=context['object'].id)
        return context


class BoxCreateView(CreateView):
    """Представление для создания бокса."""
    model = BoxModel
    fields = '__all__'
    template_name = 'inventory_items/any_create.html'


class BoxDetailView(DetailView, ContextMixin):
    """Представление для отображения деталей бокса."""
    model = BoxModel

    def get_context_data(self, **kwargs):
        """Добавляет список предметов, относящихся к боксу."""
        context = super().get_context_data(**kwargs)
        context['items'] = ItemModel.objects.filter(
            box_id=context['object'].id)
        return context


class MaterialCreateView(CreateView):
    """Представление для создания материала упаковки."""
    model = MaterialBoxModel
    fields = '__all__'
    template_name = 'inventory_items/any_create.html'


class MaterialDetailView(DetailView):
    """Представление для отображения деталей материала упаковки."""
    model = MaterialBoxModel


class ItemCreateView(CreateView):
    """Представление для создания предмета."""
    model = ItemModel
    fields = '__all__'
    template_name = 'inventory_items/any_create.html'


class ItemDetailView(DetailView):
    """Представление для отображения деталей предмета."""
    model = ItemModel


# endregion

# region Lists
class CategoryListView(ListView):
    """Представление для отображения списка категорий."""
    model = CategoryModel
    template_name = 'inventory_items/category_list.html'
    paginate_by = PAGINATION_VAR


class LocationListView(ListView):
    """Представление для отображения списка локаций."""
    model = LocationModel
    template_name = 'inventory_items/location_list.html'
    paginate_by = PAGINATION_VAR


class BoxListView(ListView):
    """Представление для отображения списка боксов."""
    model = BoxModel
    template_name = 'inventory_items/box_list.html'
    paginate_by = PAGINATION_VAR


class MaterialListView(ListView):
    """Представление для отображения списка материалов упаковки."""
    model = MaterialBoxModel
    template_name = 'inventory_items/material_list.html'
    paginate_by = PAGINATION_VAR


class ItemListView(ListView):
    """Представление для отображения списка предметов."""
    model = ItemModel
    template_name = 'inventory_items/item_list.html'
    paginate_by = PAGINATION_VAR

    def get_context_data(self, object_list=None, **kwargs):
        """Добавляет количество предметов в контекст."""
        context = super().get_context_data(**kwargs)
        context['count_objects'] = ItemModel.objects.count()
        return context


# endregion

# region Delete
class CategoryDeleteView(DeleteView):
    """Представление для удаления категории."""
    model = CategoryModel
    template_name = "inventory_items/category_confirm_delete.html"
    success_url = reverse_lazy("inventory:category-list")


class ItemDeleteView(DeleteView):
    """Представление для удаления предмета."""
    model = ItemModel
    template_name = "inventory_items/item_confirm_delete.html"
    success_url = reverse_lazy("inventory:item-list")


class BoxDeleteView(DeleteView):
    """Представление для удаления бокса."""
    model = BoxModel
    template_name = "inventory_items/box_confirm_delete.html"
    success_url = reverse_lazy("inventory:box-list")


# endregion Delete

# region Update
class CategoryUpdateView(UpdateView):
    """Представление для обновления категории."""
    model = CategoryModel
    fields = ["name"]
    template_name_suffix = "_update_form"


class ItemUpdateView(UpdateView):
    """Представление для обновления предмета."""
    model = ItemModel
    fields = '__all__'
    template_name_suffix = "_update_form"


class BoxUpdateView(UpdateView):
    """Представление для обновления бокса."""
    model = BoxModel
    fields = '__all__'
    template_name_suffix = "_update_form"


# endregion

# region Search
class SearchResultsView(ListView):
    """Представление для отображения результатов поиска предметов."""
    model = ItemModel
    template_name = 'inventory_items/search_results.html'

    def get_queryset(self):
        """Фильтрует предметы по запросу пользователя."""
        query = self.request.GET.get('item')
        object_list = ItemModel.objects.filter(
            Q(details__iregex=query) | Q(name__iregex=query)
        )
        return object_list


# endregion

def dynamic_database_filling(request):
    """Заполняет статистику по предметам из базы данных."""

    # Инициализация словаря для хранения количества предметов за каждый день
    count_first_day = {}
    # Получение последнего добавленного предмета
    first_item = ItemModel.objects.all().last()
    # Получение первого добавленного предмета
    last_item = ItemModel.objects.all().first()
    # Получение даты создания первого предмета
    atime = first_item.date_create.date()
    stat = {}  # Инициализация словаря для хранения статистики по датам
    while atime < (last_item.date_create.date() + datetime.timedelta(
            days=1)):  # Цикл по всем датам между первым и последним предметом
        # Подсчет количества предметов, добавленных в текущий день
        count_first_day = ItemModel.objects.filter(
            date_create__day=atime.day).count()
        # Сохранение количества предметов за текущую дату в словарь
        stat[str(atime)] = count_first_day
        atime += datetime.timedelta(days=1)  # Переход к следующему дню

    context = {  # Формирование контекста для передачи в шаблон
        'count': count_first_day,
        # Добавление количества предметов за последний день в контекст
        'all_count': ItemModel.objects.all().count(),
        # Добавление общего количества предметов в контекст
        'stat': stat,  # Добавление статистики по предметам в контекст
    }
    # Возвращение рендеринга шаблона с переданным контекстом
    return render(request, 'inventory_items/statistic.html', context=context)

    # first_item = ItemModel.objects.all().last()
    # last_item = ItemModel.objects.all().first()
    # count_first_day = ItemModel.objects.filter(
    #     date_create__day=first_item.date_create.day)
    # # print(first_item.date_create.day, '-', count_first_day)
    # # today = datetime.datetime.today().date() + datetime.timedelta(days=3)
    # # print(today, first_item.date_create.date())
    # atime = first_item.date_create.date()
    # stat = {}
    # while atime < (last_item.date_create.date() + datetime.timedelta(days=1)):
    #     count_first_day = ItemModel.objects.filter(
    #         date_create__day=atime.day)
    #     print(atime, count_first_day.count())
    #     stat[str(atime)] = count_first_day.count()
    #     # data_for_template.append(stat)
    #     # stat = {}
    #     atime += datetime.timedelta(days=1)
    #
    # print(stat)
    #
    # context = {
    #     'fi': first_item,
    #     'count': count_first_day,
    #     'all_count': ItemModel.objects.all().count(),
    #     'stat': stat,
    # }
    # return render(request, 'inventory_items/statistic.html', context=context)

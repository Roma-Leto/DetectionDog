from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, DetailView, \
    ListView, DeleteView, UpdateView
from django.views.generic.base import ContextMixin

from inventory_items.models import *

pagination_var = 9


# region Create & Details
class IndexView(TemplateView):
    template_name = 'inventory_items/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['count_obl'] = ItemModel.objects.count()
        return context


class CategoryCreateView(CreateView):
    model = CategoryModel
    fields = ["name"]
    template_name = 'inventory_items/any_create.html'


class CategoryDetailView(DetailView):
    model = CategoryModel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = ItemModel.objects.filter(
            categories_id=context['object'].id
        )
        return context


class LocationCreateView(CreateView):
    model = LocationModel
    fields = '__all__'
    template_name = 'inventory_items/any_create.html'


class LocationDetailView(DetailView):
    model = LocationModel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = ItemModel.objects.filter(
            location_id=context['object'].id
        )
        context['box'] = BoxModel.objects.filter(
            location_id=context['object'].id
        )
        return context


class BoxCreateView(CreateView):
    model = BoxModel
    fields = '__all__'
    template_name = 'inventory_items/any_create.html'


class BoxDetailView(DetailView, ContextMixin):
    model = BoxModel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = ItemModel.objects.filter(
            box_id=context['object'].id
        )
        return context


class MaterialCreateView(CreateView):
    model = MaterialBoxModel
    fields = '__all__'
    template_name = 'inventory_items/any_create.html'


class MaterialDetailView(DetailView):
    model = MaterialBoxModel


class ItemCreateView(CreateView):
    model = ItemModel
    fields = '__all__'
    template_name = 'inventory_items/any_create.html'


class ItemDetailView(DetailView):
    model = ItemModel


# endregion
# region Lists
class CategoryListView(ListView):
    model = CategoryModel
    template_name = 'inventory_items/category_list.html'
    paginate_by = pagination_var


class LocationListView(ListView):
    model = LocationModel
    template_name = 'inventory_items/location_list.html'
    paginate_by = pagination_var


class BoxListView(ListView):
    model = BoxModel
    template_name = 'inventory_items/box_list.html'
    paginate_by = pagination_var


class MaterialListView(ListView):
    model = MaterialBoxModel
    template_name = 'inventory_items/material_list.html'
    paginate_by = pagination_var


class ItemListView(ListView):
    model = ItemModel
    template_name = 'inventory_items/item_list.html'
    paginate_by = pagination_var

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count_objects'] = ItemModel.objects.count()
        return context


# endregion
# region Delete
class CategoryDeleteView(DeleteView):
    model = CategoryModel
    template_name = "inventory_items/category_confirm_delete.html"
    success_url = reverse_lazy("inventory:category-list")


class ItemDeleteView(DeleteView):
    model = ItemModel
    template_name = "inventory_items/item_confirm_delete.html"
    success_url = reverse_lazy("inventory:item-list")


class BoxDeleteView(DeleteView):
    model = BoxModel
    template_name = "inventory_items/box_confirm_delete.html"
    success_url = reverse_lazy("inventory:box-list")


# endregion Delete
# region Update
class CategoryUpdateView(UpdateView):
    model = CategoryModel
    fields = ["name"]
    template_name_suffix = "_update_form"


class ItemUpdateView(UpdateView):
    model = ItemModel
    fields = '__all__'
    template_name_suffix = "_update_form"


class BoxUpdateView(UpdateView):
    model = BoxModel
    fields = '__all__'
    template_name_suffix = "_update_form"


# endregion Delete
# region Search

class SearchResultsView(ListView):
    model = ItemModel
    template_name = 'inventory_items/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('item')
        object_list = ItemModel.objects.filter(
            Q(details__iregex=query)
            | Q(name__iregex=query)
        )
        print(object_list.values()[0]['photo'])
        return object_list

# endregion

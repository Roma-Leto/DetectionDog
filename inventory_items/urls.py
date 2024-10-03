from django.urls import path

from .views import *

app_name = 'inventory'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),

    # region category
    path('category-create/',
         CategoryCreateView.as_view(),
         name='category-create'),
    path('category-detail/<int:pk>/',
         CategoryDetailView.as_view(),
         name='category-details'),
    path('category-list/',
         CategoryListView.as_view(),
         name='category-list'),
    path('category_confirm_delete/<int:pk>/',
         CategoryDeleteView.as_view(),
         name='category_confirm_delete'),
    path('category_update_form/<int:pk>/',
         CategoryUpdateView.as_view(),
         name='category_update_form'),
    # endregion
    # region location
    path('location-create/',
         LocationCreateView.as_view(),
         name='location-create'),
    path('location-list/',
         LocationListView.as_view(),
         name='location-list'),
    path('location-detail/<int:pk>/',
         LocationDetailView.as_view(),
         name='location-details'),
    # endregion
    # region box
    path('box-create/',
         BoxCreateView.as_view(),
         name='box-create'),
    path('box-list/',
         BoxListView.as_view(),
         name='box-list'),
    path('box-update-form/<int:pk>/',
         BoxUpdateView.as_view(),
         name='box-update-form'),
    path('box-detail/<int:pk>/',
         BoxDetailView.as_view(),
         name='box-details'),
    # endregion
    # region material
    path('material-create/',
         MaterialCreateView.as_view(),
         name='material-create'),
    path('material-list/',
         MaterialListView.as_view(),
         name='material-list'),
    path('material-detail/<int:pk>/',
         MaterialDetailView.as_view(),
         name='material-details'),
    # endregion
    # region item
    path('item-create/',
         ItemCreateView.as_view(),
         name='item-create'),
    path('item-list/',
         ItemListView.as_view(),
         name='item-list'),
    path('item-detail/<int:pk>/',
         ItemDetailView.as_view(),
         name='item-details'),
    path('item_update_form/<int:pk>/',
         ItemUpdateView.as_view(),
         name='itemmodel-update-form'),
    path('item_confirm_delete/<int:pk>/',
         ItemDeleteView.as_view(),
         name='item-confirm-delete'),
    # endregion

    path('search_results/',
         SearchResultsView.as_view(),
         name='search_results'),
]
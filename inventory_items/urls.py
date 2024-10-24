from django.urls import path

from .views import *

app_name = 'inventory'  # Имя пространства имен для URL-адресов приложения "inventory"

urlpatterns = [
    path('', IndexView.as_view(), name='index'),  # Главная страница приложения

    # region category
    path('category-create/',
         CategoryCreateView.as_view(),
         name='category-create'),  # Страница создания новой категории
    path('category-detail/<int:pk>/',
         CategoryDetailView.as_view(),
         name='category-details'),  # Страница с деталями категории
    path('category-list/',
         CategoryListView.as_view(),
         name='category-list'),  # Страница со списком категорий
    path('category_confirm_delete/<int:pk>/',
         CategoryDeleteView.as_view(),
         name='category_confirm_delete'),  # Подтверждение удаления категории
    path('category_update_form/<int:pk>/',
         CategoryUpdateView.as_view(),
         name='category_update_form'),  # Форма обновления категории
    # endregion

    # region location
    path('location-create/',
         LocationCreateView.as_view(),
         name='location-create'),  # Страница создания новой локации
    path('location-list/',
         LocationListView.as_view(),
         name='location-list'),  # Страница со списком локаций
    path('location-detail/<int:pk>/',
         LocationDetailView.as_view(),
         name='location-details'),  # Страница с деталями локации
    # endregion

    # region box
    path('box-create/',
         BoxCreateView.as_view(),
         name='box-create'),  # Страница создания нового бокса
    path('box-list/',
         BoxListView.as_view(),
         name='box-list'),  # Страница со списком боксов
    path('box-update-form/<int:pk>/',
         BoxUpdateView.as_view(),
         name='box-update-form'),  # Форма обновления бокса
    path('box-detail/<int:pk>/',
         BoxDetailView.as_view(),
         name='box-details'),  # Страница с деталями бокса
    path('box_confirm_delete/<int:pk>/',
         BoxDeleteView.as_view(),
         name='box-confirm-delete'),  # Подтверждение удаления бокса
    # endregion

    # region material
    path('material-create/',
         MaterialCreateView.as_view(),
         name='material-create'),  # Страница создания нового материала упаковки
    path('material-list/',
         MaterialListView.as_view(),
         name='material-list'),  # Страница со списком материалов упаковки
    path('material-detail/<int:pk>/',
         MaterialDetailView.as_view(),
         name='material-details'),  # Страница с деталями материала упаковки
    # endregion

    # region item
    path('item-create/',
         ItemCreateView.as_view(),
         name='item-create'),  # Страница создания нового предмета
    path('item-list/',
         ItemListView.as_view(),
         name='item-list'),  # Страница со списком предметов
    path('item-detail/<int:pk>/',
         ItemDetailView.as_view(),
         name='item-details'),  # Страница с деталями предмета
    path('item_update_form/<int:pk>/',
         ItemUpdateView.as_view(),
         name='itemmodel-update-form'),  # Форма обновления предмета
    path('item_confirm_delete/<int:pk>/',
         ItemDeleteView.as_view(),
         name='item-confirm-delete'),  # Подтверждение удаления предмета
    # endregion

    path('search_results/',
         SearchResultsView.as_view(),
         name='search_results'),  # Страница с результатами поиска
    path('statistic/',
         dynamic_database_filling,
         name='stat'),  # Страница с динамической статистикой
]

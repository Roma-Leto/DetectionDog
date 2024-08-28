from django.urls import path
from .views import index, show_category, smart_details

app_name = 'smart_app'

urlpatterns = [
    path('', index, name='sandbox_index'),
    path('smart-details/<slug:smart_slug>', smart_details, name='smart_details'),
    path('categories-smart/<slug:cat_slug>/', show_category, name='category'),
]

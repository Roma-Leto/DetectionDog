from django.contrib import admin
from django.urls import path, include

from .views import base_index

urlpatterns = [
    path('', base_index, name='base'),
    path('smartphons/', include('sandbox1.urls', namespace='smart_app')),
    path('admin/', admin.site.urls),
]

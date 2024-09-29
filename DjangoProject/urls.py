from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings

from .views import base_index

urlpatterns = [
    path('', base_index, name='base'),
    path('smartphons/', include('sandbox1.urls', namespace='smart_app')),
    path('summary-of-the-day/',
         include('summary_of_the_day.urls',
                 namespace='summary_of_the_day')
         ),
    path('admin/', admin.site.urls),
    path('inventory/', include('inventory_items.urls', namespace='inventory'))
] \
              + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)\
              + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

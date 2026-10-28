from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.views.static import serve

from mainApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('comprar/<int:id>', views.comprar, name='comprar'),
    path('ticket/<int:id>', views.ticket, name='ticket'),
]

# En desarrollo, sirve las imágenes subidas (carpeta media)
if settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]

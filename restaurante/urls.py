from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main_index, name='main_index'),
    path('accounts/', include('apps.accounts.urls')),
    path('platillos/', include('apps.platillos.urls')),
]

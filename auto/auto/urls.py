from django.contrib import admin
from django.urls import path, include
from autocrud import views

urlpatterns = [
    path('', views.home, name='home'),
    path('crud/', include('autocrud.urls')),
    path('admin/', admin.site.urls),
]

from django.urls import path
from . import views

app_name = 'autocrud' #Nas templates deve colocar o app_name nos links {% url 'app_name:name'%} -> autocrud:autos
urlpatterns = [
    path('login/', views.login, name='login'),
    path('cadastro/', views.cadastro, name='cadastro'),

    path('autos/', views.autos, name='autos'),
    path('auto/create/', views.auto_create, name='auto_create'),
    path('auto/<int:autoid>/update/', views.auto_update, name='auto_update'),
    path('auto/<int:autoid>/delete/', views.auto_delete, name='auto_delete'),

    path('makes/', views.makes, name='makes'),
    path('make/create/', views.make_create, name='make_create'),
    path('make/<int:makeid>/update/', views.make_update, name='make_update'),
    path('make/<int:makeid>/delete/', views.make_delete, name='make_delete'),
]

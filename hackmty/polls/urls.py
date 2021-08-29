from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('generic.html/', views.generic, name = 'generic'),
    path('<int:number>/', views.results, name = 'results')
]

urlpatterns += staticfiles_urlpatterns()
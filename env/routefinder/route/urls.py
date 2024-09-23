from django.urls import path
from . import views

urlpatterns = [
    path('route/', views.getRoute, name='route' ),
    path('inputs/', views.inputs, name='inputs')
]
# application/urls.py
from django.urls import path
from .views import display_data
from .views import dash

from . import views  #-------------------------------aymen-------------------------


urlpatterns = [
    path('', display_data, name='display_data'),
    path('dash/', dash, name='dash'),



    
    path('dashboard/', views.dashboard, name='app-dashboard'),  # Définissez l'URL pour dashboard
    path('datatables/',views.datatables,name='app-datatables'),
    path('classement/',views.classement,name='app-classement'),
    path('prediction/',views.prediction,name='app-prediction'),

]


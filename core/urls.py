from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),        
    path('core/not_authorized', views.not_authorized, name='url_not_authorized'),
    path('core/rel', views.rel, name='rel'),    
]

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'provider'

urlpatterns = [
    #Provider    
    path('provider-create/', views.provider_create, name = 'url_provider_create'),
    path('', views.providers_list, name='url_providers_list'),
    path('<slug:slug>/detail', views.provider_detail, name='url_provider_detail'),
    path('<slug:slug>/edit', views.provider_edit, name='url_provider_edit'),
    path('<slug:slug>/delete', views.provider_delete, name='url_provider_delete'),
    path('delete_all/', views.provider_delete_all, name='url_provider_delete_all'),

    # URL PARA TRADUZIR O DATATABLES. USO GERAL
    path('provider/translate-js/', views.translate_datables_js, name='url_translate_datables_js'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

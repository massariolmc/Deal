from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'service_type'

urlpatterns = [
    #service_type    
    path('service_type-create/', views.service_type_create, name = 'url_service_type_create'),
    path('', views.service_types_list, name='url_service_types_list'),
    path('service_type/<slug:slug>/detail', views.service_type_detail, name='url_service_type_detail'),
    path('service_type/<slug:slug>/edit', views.service_type_edit, name='url_service_type_edit'),
    path('service_type/<slug:slug>/delete', views.service_type_delete, name='url_service_type_delete'),
    path('service_type/delete_all/', views.service_type_delete_all, name='url_service_type_delete_all'),

    # URL PARA TRADUZIR O DATATABLES. USO GERAL
    path('service_type/translate-js/', views.translate_datables_js, name='url_translate_datables_js'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
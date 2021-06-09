from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'contract'

urlpatterns = [
    #Company    
    path('contract-create/', views.contract_create, name = 'url_contract_create'),
    path('', views.contracts_list, name='url_contracts_list'),
    path('contract/<slug:slug>/detail', views.contract_detail, name='url_contract_detail'),
    path('contract/<slug:slug>/edit', views.contract_edit, name='url_contract_edit'),
    path('contract/<slug:slug>/delete', views.contract_delete, name='url_contract_delete'),
    path('contract/delete_all/', views.contract_delete_all, name='url_contract_delete_all'),

    # URL PARA TRADUZIR O DATATABLES. USO GERAL
    path('contract/translate-js/', views.translate_datables_js, name='url_translate_datables_js'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'contract'

urlpatterns = [
    #Company    
    path('contract-create/', views.contract_create, name = 'url_contract_create'),
    path('list_actives/', views.contracts_list, name='url_contracts_list'),
    path('list_inactives/', views.contracts_list_inactives, name='url_contracts_list_inactives'),
    path('<slug:slug>/detail', views.contract_detail, name='url_contract_detail'),
    path('<slug:slug>/edit', views.contract_edit, name='url_contract_edit'),
    path('<slug:slug>/delete', views.contract_delete, name='url_contract_delete'),
    path('delete_all/', views.contract_delete_all, name='url_contract_delete_all'),
    path('contract-due-date/', views.contract_due_date, name='url_contract_due_date'),
    path('contract-invoice-date/', views.contract_invoice_date, name='url_contract_invoice_date'),
    path('contract-finish/', views.contract_finish, name='url_contract_finish'),
    
    #Upload Contract
    path('<int:contract>/upload_contract_create', views.upload_contract_create, name='url_upload_contract_create'),
    path('<slug:slug>/pdf/delete', views.upload_delete, name='url_upload_delete'),

    #Nimbi
    path('<slug:contract>/nimbi_create', views.nimbi_contract_create, name='url_nimbi_contract_create'),
    path('<slug:slug>/nimbi/delete', views.nimbi_contract_delete, name='url_nimbi_contract_delete'),   
    
    #Contact Provider
    path('<slug:contract>/contact_provider_create', views.contact_provider_create, name='url_contact_provider_create'),
    path('<slug:slug>/contacts/delete', views.contact_provider_delete, name='url_contact_provider_delete'),

    #Department Contract
    path('<slug:contract>/department-contract-create', views.department_contract_create, name='url_department_contract_create'),
    path('<slug:slug_department>/<slug:slug_contract>/department-contracts/delete', views.department_contract_delete, name='url_department_contract_delete'),

    #Cost Center
    path('cost-centers', views.cost_center_list, name='url_cost_centers_list'),

    # URL PARA TRADUZIR O DATATABLES. USO GERAL
    path('contract/translate-js/', views.translate_datables_js, name='url_translate_datables_js'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

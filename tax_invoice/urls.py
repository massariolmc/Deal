from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'tax_invoice'

urlpatterns = [
    #Company    
    path('<slug:slug>/create', views.tax_invoice_create, name = 'url_tax_invoice_create'),
    path('<slug:slug>/list', views.tax_invoices_list, name='url_tax_invoices_list'),
    path('<slug:slug>/detail', views.tax_invoice_detail, name='url_tax_invoice_detail'),
    path('<slug:slug>/edit', views.tax_invoice_edit, name='url_tax_invoice_edit'),
    path('<slug:slug>/delete', views.tax_invoice_delete, name='url_tax_invoice_delete'),
    path('delete_all/', views.tax_invoice_delete_all, name='url_tax_invoice_delete_all'),

    #Providers Choose
    path('providers-choose/', views.providers_choose, name='url_providers_choose'),

    #Upload Delete
    path('<slug:slug>/pdf/delete', views.upload_delete, name='url_upload_delete'),

    # URL PARA TRADUZIR O DATATABLES. USO GERAL
    path('tax_invoice/translate-js/', views.translate_datables_js, name='url_translate_datables_js'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

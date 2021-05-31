from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'company'

urlpatterns = [
    #Company    
    path('company-create/', views.company_create, name = 'url_company_create'),
    path('', views.companies_list, name='url_companies_list'),
    path('company/<slug:slug>/detail', views.company_detail, name='url_company_detail'),
    path('company/<slug:slug>/edit', views.company_edit, name='url_company_edit'),
    path('company/<slug:slug>/delete', views.company_delete, name='url_company_delete'),
    path('company/delete_all/', views.company_delete_all, name='url_company_delete_all'),

    # URL PARA TRADUZIR O DATATABLES. USO GERAL
    path('company/translate-js/', views.translate_datables_js, name='url_translate_datables_js'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
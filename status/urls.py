from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'status'

urlpatterns = [
    #status    
    path('status-create/', views.status_create, name = 'url_status_create'),
    path('', views.status_list, name='url_status_list'),
    path('<slug:slug>/detail', views.status_detail, name='url_status_detail'),
    path('<slug:slug>/edit', views.status_edit, name='url_status_edit'),
    path('<slug:slug>/delete', views.status_delete, name='url_status_delete'),
    path('delete_all/', views.status_delete_all, name='url_status_delete_all'),

    # URL PARA TRADUZIR O DATATABLES. USO GERAL
    path('status/translate-js/', views.translate_datables_js, name='url_translate_datables_js'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

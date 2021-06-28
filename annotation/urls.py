from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'annotation'

urlpatterns = [
    #annotation    
    path('<slug:contract>/annotation-create/', views.annotation_create, name = 'url_annotation_create'),
    path('<slug:contract>/list', views.annotations_list, name='url_annotations_list'),
    path('<slug:slug>/detail', views.annotation_detail, name='url_annotation_detail'),
    path('<slug:slug>/edit', views.annotation_edit, name='url_annotation_edit'),
    path('<slug:slug>/delete', views.annotation_delete, name='url_annotation_delete'),
    path('delete_all/', views.annotation_delete_all, name='url_annotation_delete_all'),

    # URL PARA TRADUZIR O DATATABLES. USO GERAL
    path('annotation/translate-js/', views.translate_datables_js, name='url_translate_datables_js'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

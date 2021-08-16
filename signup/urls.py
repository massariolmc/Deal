from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'signup'

urlpatterns = [    
    path('signup-create/', views.signup_create, name = 'url_signup_create'),
    path('', views.signup_list, name='url_signup_list'),
    path('<int:pk>/delete', views.signup_delete, name='url_signup_delete'),
    path('inactive_all/', views.signup_inactive_all, name='url_signup_inactive_all'),
    path('<int:pk>/detail', views.signup_detail, name='url_signup_detail'),
    path('<int:pk>/edit', views.signup_edit, name='url_signup_edit'),

    #Password Change
    path('<int:pk>/password-change/', views.user_password_change, name='url_user_password_change'),

    #User Contract
    path('<int:user>/user-contract-create', views.user_contract_create, name='url_user_contract_create'),
    path('<int:pk>/<slug:slug_contract>/user-contracts/delete', views.user_contract_delete, name='url_user_contract_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
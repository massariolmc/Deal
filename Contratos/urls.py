"""Contratos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('manager_mlx/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),    
]
urlpatterns += i18n_patterns(

#urlpatterns = [    
    path('vetorial/', include('core.urls')),
    path('vetorial/companies/',include('company.urls')),
    path('vetorial/providers/',include('provider.urls')),
    path('vetorial/contact_providers/',include('contact_provider.urls')),
    path('vetorial/service_types/',include('service_type.urls')),
    path('vetorial/status/',include('status.urls')),
    path('vetorial/contracts/',include('contract.urls')),
    path('vetorial/tax_invoices/',include('tax_invoice.urls')),
    path('vetorial/annotations/',include('annotation.urls')),
    path('vetorial/accounts/', include('django.contrib.auth.urls')),
    prefix_default_language=False
#]
)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

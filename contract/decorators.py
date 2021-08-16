from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import ugettext as _
# accounts/decorators.py
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test

from django.core.exceptions import PermissionDenied
from .models import Contract

def check(request,slug):
    contract = Contract.objects.get(slug=slug)
    v = contract.members_user.all()        
    aux = 0        
    for i in v:
        if i.id == request.user.id:
            aux = 1 
    return aux               

# Verifica se o usuário tem acesso ao contrato
def user_has_access_contract(function):
    def wrap(request, *args, **kwargs):
        if not request.user.is_superuser:                 
            slug = kwargs.get('slug',None)
            aux = 0
            if slug: #Edit, Detail e Delete
                aux = check(request,slug)
            else: #Delete All
                slugs = request.POST["checkbox_selected"].split(",")            
                for x in slugs:
                    aux = check(request,x)
                    if not aux:
                        break
                
            if aux:
                return function(request, *args, **kwargs)
            else:            
                #raise PermissionDenied
                return redirect('core:url_not_authorized')
        else:
            return function(request, *args, **kwargs)

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

# Verifica se é Admin. Só Admin cria e deleta usuário
def user_contract_delete(function=None, login_url='core:url_not_authorized', redirect_field_name=REDIRECT_FIELD_NAME):
    print("from django.contrib.auth import REDIRECT_FIELD_NAME", redirect_field_name)
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_superuser,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
from django.shortcuts import render,get_object_or_404, get_list_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.utils.translation import ugettext as _
from django.contrib import messages
from .models import Provider
from .form import ProviderForm
from django.forms import modelformset_factory, inlineformset_factory
from account.models import User
from django.contrib.auth.decorators import login_required, permission_required
from .decorators import verify_superuser
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db import IntegrityError
from django.db.models import Q, Sum, Count, Prefetch
from django.template.loader import render_to_string
import os
import json

####### PROVIDER  ################

def provider_save_form(request,form,template_name, data, user_created=None):    
    if request.method == 'POST':                                              
        if form.is_valid():
            obj = form.save(commit=False)                                   
            if user_created:# Se cair aqui é EDIT                               
                obj.user_created = user_created                
            else:# Se cair aqui é CREATE                
                obj.user_created = request.user
            obj.user_updated = request.user  
            obj.save()         
                
            return redirect('provider:url_provider_detail', obj.slug)
        else:
            print("algo não está valido.")               
    
    data['form'] = form
    return render(request,template_name,data)

@login_required(login_url='login')
@verify_superuser
def provider_create(request):
    template_name = 'provider/form.html'    
    data = {
            "title": _("Create Provider"),
            "back":_("Back"),
            "save":_("Save"),
            "clear":_("Clear"),
        }    
    if request.method == 'POST':                       
        form = ProviderForm(request.POST, request.FILES)                
    else:
        form = ProviderForm()             
    
    return provider_save_form(request, form, template_name, data)

@login_required(login_url='login')
@verify_superuser
def provider_edit(request, slug):    
    template_name='provider/form.html'
    data = {
            "title": _("Edit"),
            "back":_("Back"),
            "save":_("Save"),
            "clear":_("Clear"),
        }    
    provider = get_object_or_404(Provider, slug=slug)           
    user_created = provider.user_created # Esta linha faz com que o user_created não seja modificado, para mostrar quem criou esta pessoa    
    if request.method == 'POST':        
        form = ProviderForm(request.POST, request.FILES, instance=provider)                
    else:
        form = ProviderForm(instance=provider)       
    return provider_save_form(request, form, template_name, data, user_created=user_created)

@login_required(login_url='login')
@verify_superuser
def providers_list(request):
    template_name = "provider/list.html"
    providers = Provider.objects.all()    
    data = {}    
    
    def pagination(request,objects,lines=10):
        page = request.GET.get('page', 1)
        print("Valor de page: ",page)
        paginator = Paginator(objects, int(lines))        
        try:
            objects = paginator.page(page)
        except PageNotAnInteger:
            objects = paginator.page(1)
        except EmptyPage:
            objects = paginator.page(paginator.num_pages)
        
        return objects
    
    def search(request, query,lines, model):
        obj_search = ""              
        print("model",model)
        if query:            
            obj_search = model.filter(
                Q(name__icontains=query) | Q(fantasy_name__icontains=query) | Q(cnpj__icontains=query) | Q(email__icontains=query)                
                
            ).distinct()   
            print("obj_search",obj_search)          
        else:
            print("Não existe") 
            obj_search = model

        objs = pagination(request,obj_search,int(lines))                           
        return objs

    if request.is_ajax():
        query = request.GET.get('q')
        lines = request.GET.get('l')        
        objs = search(request, query,lines,providers)
        data['html_signup_list'] = render_to_string('provider/_table.html', {'providers': objs})       
        return JsonResponse(data)
            
                 
    lines = 10
    providers = pagination(request,providers,int(lines))

    context = {
        'providers': providers,
        'title': _("Registered Providers"),
        'add': _("Add")      
    }
    return render(request,template_name,context)

@login_required(login_url='login')
@verify_superuser
def provider_detail(request, slug):    
    template_name = "provider/detail.html"
    provider = get_object_or_404(Provider,slug=slug)   
    context = {
        'provider': provider,
        'title': _("Detail Info"),
        'edit': _("Edit"),
        'show': _("Show"),
        'list_all': _("List All"),        
    }
    return render(request, template_name, context)

@login_required(login_url='login')
@verify_superuser
def provider_delete(request, slug):    
    provider = get_object_or_404(Provider, slug=slug)    
    if request.method == 'POST':        
       try:
           provider.delete()
           messages.success(request, _('Completed successful.'))
           return redirect('provider:url_providers_list')
       except IntegrityError:
           messages.warning(request, _('You cannot delete. This provider has an existing department.'))
           return redirect('provider:url_providers_list')    

@login_required(login_url='login')
@verify_superuser
def provider_delete_all(request):
    marc = 0    
    if request.method == "POST":        
        context = request.POST["checkbox_selected"].split(",")
        context = [str(x) for x in context]      
        if context:                
            b = Provider.objects.filter(slug__in=context)            
            for i in b:                
                try:
                    i.delete()
                except IntegrityError:
                    marc = 1                    
    if marc == 0:
        messages.success(request, _('Completed successful.'))
    else:
        messages.warning(request, _('You cannot delete. This provider has an existing department.'))
    
    return redirect('provider:url_providers_list')
    
########### FIM PROVIDER ############################


# VIEW PARA TRADUZIR O DATATABLES. USO GERAL
def translate_datables_js(request):    
    if request.method == "GET":
        module_dir = os.path.dirname(__file__)  # get current directory       
        file_path = os.path.join(module_dir, 'templates/default')        
        translate = ""        
        with open(file_path+"/translate_data_tables-"+request.LANGUAGE_CODE+".json", 'r') as arquivo:
            for linha in arquivo:
                translate += linha        
        obj = json.loads(translate)        
    return JsonResponse(obj)

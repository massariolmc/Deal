from django.shortcuts import render,get_object_or_404, get_list_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.utils.translation import ugettext as _
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from .decorators import verify_superuser
from .models import ServiceType
from .form import ServiceTypeForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.template.loader import render_to_string
from account.models import User
from django.db import IntegrityError
from django.db.models import Q, Sum, Count, Prefetch
import os
import json

####### SERVICETYPE  ################

def service_type_save_form(request,form,template_name, data, user_created=None):    
    if request.method == 'POST':                                              
        if form.is_valid():
            obj = form.save(commit=False)                                   
            if user_created:# Se cair aqui é EDIT                               
                obj.user_created = user_created                
            else:# Se cair aqui é CREATE                
                obj.user_created = request.user
            obj.user_updated = request.user  
            obj.save()         
                
            return redirect('service_type:url_service_type_detail', obj.slug)
        else:
            print("algo não está valido.")               
    
    data['form'] = form
    return render(request,template_name,data)

@login_required(login_url='login')
@verify_superuser
def service_type_create(request):
    template_name = 'service_type/form.html'    
    data = {
            "title": _("Create ServiceType"),
            "back":_("Back"),
            "save":_("Save"),
            "clear":_("Clear"),
        }    
    if request.method == 'POST':                       
        form = ServiceTypeForm(request.POST, request.FILES)                
    else:
        form = ServiceTypeForm()             
    
    return service_type_save_form(request, form, template_name, data)

@login_required(login_url='login')
@verify_superuser
def service_type_edit(request, slug):    
    template_name='service_type/form.html'
    data = {
            "title": _("Edit"),
            "back":_("Back"),
            "save":_("Save"),
            "clear":_("Clear"),
        }    
    service_type = get_object_or_404(ServiceType, slug=slug)           
    user_created = service_type.user_created # Esta linha faz com que o user_created não seja modificado, para mostrar quem criou esta pessoa    
    if request.method == 'POST':        
        form = ServiceTypeForm(request.POST, request.FILES, instance=service_type)                
    else:
        form = ServiceTypeForm(instance=service_type)       
    return service_type_save_form(request, form, template_name, data, user_created=user_created)

@login_required(login_url='login')
@verify_superuser 
def service_types_list(request):
    template_name = "service_type/list.html"
    service_types = ServiceType.objects.all()    
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
                Q(name__icontains=query) | Q(description__icontains=query)                
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
        objs = search(request, query,lines,service_types)
        data['html_signup_list'] = render_to_string('service_type/_table.html', {'service_types': objs})       
        return JsonResponse(data)
            
                 
    lines = 10
    service_types = pagination(request,service_types,int(lines))

    context = {
        'service_types': service_types,
        'title': _("Registered Service Types"),
        'add': _("Add")      
    }
    return render(request,template_name,context)

@login_required(login_url='login')
@verify_superuser
def service_type_detail(request, slug):    
    template_name = "service_type/detail.html"
    service_type = get_object_or_404(ServiceType,slug=slug)
    context = {
        'service_type': service_type,
        'title': _("Detail Info"),
        'edit': _("Edit"),
        'list_all': _("List All")
    }
    return render(request, template_name, context)

@login_required(login_url='login')
@verify_superuser
def service_type_delete(request, slug):    
    service_type = get_object_or_404(ServiceType, slug=slug)    
    if request.method == 'POST':        
       try:
           service_type.delete()
           messages.success(request, _('Completed successful.'))
           return redirect('service_type:url_service_types_list')
       except IntegrityError:
           messages.warning(request, _('You cannot delete. This service_type has an existing deal.'))
           return redirect('service_type:url_service_types_list')    

@login_required(login_url='login')
@verify_superuser
def service_type_delete_all(request):
    marc = 0    
    if request.method == "POST":        
        context = request.POST["checkbox_selected"].split(",")
        context = [str(x) for x in context]      
        if context:                
            b = ServiceType.objects.filter(slug__in=context)            
            for i in b:                
                try:
                    i.delete()
                except IntegrityError:
                    marc = 1                    
    if marc == 0:
        messages.success(request, _('Completed successful.'))
    else:
        messages.warning(request, _('You cannot delete. This service_type has an existing deal.'))
    
    return redirect('service_type:url_service_types_list')
    
########### FIM SERVICETYPE ############################

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
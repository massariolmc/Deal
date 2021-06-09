from django.shortcuts import render,get_object_or_404, get_list_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.utils.translation import ugettext as _
from django.contrib import messages
from .models import Status
from .form import StatusForm
from account.models import User
from django.db import IntegrityError
from django.db.models import Q, Sum, Count, Prefetch
import os
import json

####### STATUS  ################

def status_save_form(request,form,template_name, data, user_created=None):    
    if request.method == 'POST':                                              
        if form.is_valid():
            obj = form.save(commit=False)                                   
            if user_created:# Se cair aqui é EDIT                               
                obj.user_created = user_created                
            else:# Se cair aqui é CREATE                
                obj.user_created = request.user
            obj.user_updated = request.user  
            obj.save()         
                
            return redirect('status:url_status_list')
        else:
            print("algo não está valido.")               
    
    data['form'] = form
    return render(request,template_name,data)

def status_create(request):
    template_name = 'status/form.html'    
    data = {
            "title": _("Create Status"),
            "back":_("Back"),
            "save":_("Save"),
            "clear":_("Clear"),
        }    
    if request.method == 'POST':                       
        form = StatusForm(request.POST, request.FILES)                
    else:
        form = StatusForm()             
    
    return status_save_form(request, form, template_name, data)

def status_edit(request, slug):    
    template_name='status/form.html'
    data = {
            "title": _("Edit"),
            "back":_("Back"),
            "save":_("Save"),
            "clear":_("Clear"),
        }    
    status = get_object_or_404(Status, slug=slug)           
    user_created = status.user_created # Esta linha faz com que o user_created não seja modificado, para mostrar quem criou esta pessoa    
    if request.method == 'POST':        
        form = StatusForm(request.POST, request.FILES, instance=status)                
    else:
        form = StatusForm(instance=status)       
    return status_save_form(request, form, template_name, data, user_created=user_created)
    
def status_list(request):
    template_name = "status/list.html"
    status = Status.objects.all()    
    context = {
        'status': status,
        'title': _("Registered Status"),
        'add': _("Add")      
    }
    return render(request,template_name,context)

def status_detail(request, slug):    
    template_name = "status/detail.html"
    status = get_object_or_404(Status,slug=slug)
    context = {
        'status': status,
        'title': _("Detail Info"),
        'edit': _("Edit"),
        'list_all': _("List All")
    }
    return render(request, template_name, context)

def status_delete(request, slug):    
    status = get_object_or_404(Status, slug=slug)    
    if request.method == 'POST':        
       try:
           status.delete()
           messages.success(request, _('Completed successful.'))
           return redirect('status:url_status_list')
       except IntegrityError:
           messages.warning(request, _('You cannot delete. This status has an existing deal.'))
           return redirect('status:url_status_list')    

def status_delete_all(request):    
    marc = 0    
    if request.method == "POST":              
        context = request.POST["checkbox_selected"].split(",")
        context = [str(x) for x in context]              
        if context:                
            b = Status.objects.filter(slug__in=context)            
            for i in b:                
                try:
                    i.delete()
                except IntegrityError:
                    marc = 1                    
    if marc == 0:
        messages.success(request, _('Completed successful.'))
    else:
        messages.warning(request, _('You cannot delete. This status has an existing deal.'))
    
    return redirect('status:url_status_list')
    
########### FIM STATUS ############################

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


from django.shortcuts import render,get_object_or_404, get_list_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.utils.translation import ugettext as _
from django.contrib import messages
from contract.models import Contract
from .models import Annotation
from .form import AnnotationForm
from account.models import User
from django.db import IntegrityError
from django.db.models import Q, Sum, Count, Prefetch
import os
import json

####### SERVICETYPE  ################

def annotation_save_form(request,form,template_name, data, user_created=None):    
    if request.method == 'POST':                                              
        if form.is_valid():
            obj = form.save(commit=False)                                   
            if user_created:# Se cair aqui é EDIT                               
                obj.user_created = user_created                
            else:# Se cair aqui é CREATE                
                obj.user_created = request.user
            obj.user_updated = request.user  
            obj.save()         
                
            return redirect('annotation:url_annotations_list',data['contract'].slug)
        else:
            print("algo não está valido.")               
    
    data['form'] = form
    return render(request,template_name,data)

def annotation_create(request,contract):
    contract = get_object_or_404(Contract, slug=contract)
    template_name = 'annotation/form.html'    
    data = {
            "title": _("Create Annotation"),
            "back":_("Back"),
            "save":_("Save"),
            "clear":_("Clear"),
            "contract": contract,
        }    
    if request.method == 'POST':                       
        form = AnnotationForm(request.POST, request.FILES,contract=contract.id)                
    else:
        form = AnnotationForm(contract=contract.id)             
    
    return annotation_save_form(request, form, template_name, data)

def annotation_edit(request, slug):    
    annotation = get_object_or_404(Annotation, slug=slug)    
    contract = get_object_or_404(Contract, slug=annotation.contract.slug) 
    template_name='annotation/form.html'
    data = {
            "title": _("Edit"),
            "back":_("Back"),
            "save":_("Save"),
            "clear":_("Clear"),
            "contract": contract,
        }     
    user_created = annotation.user_created # Esta linha faz com que o user_created não seja modificado, para mostrar quem criou esta pessoa    
    if request.method == 'POST':        
        form = AnnotationForm(request.POST, request.FILES, instance=annotation)                
    else:
        form = AnnotationForm(instance=annotation)       
    return annotation_save_form(request, form, template_name, data, user_created=user_created)
    
def annotations_list(request,contract):
    contract = get_object_or_404(Contract, slug=contract) 
    template_name = "annotation/list.html"
    annotations = Annotation.objects.filter(contract=contract.id)
    context = {
        'annotations': annotations,
        'contract': contract,
        'title': _("Registered Annotations"),
        'add': _("Add"),
        'vars': [_("Contract"), _("Provider")],   
        'back': _("Back"),    
    }
    return render(request,template_name,context)

def annotation_detail(request, slug):    
    template_name = "annotation/detail.html"
    annotation = get_object_or_404(Annotation,slug=slug)
    contract = get_object_or_404(Contract,slug=annotation.contract.slug)
    context = {
        'annotation': annotation,
        'contract': contract,
        'title': _("Detail Info"),
        'edit': _("Edit"),
        'list_all': _("List All"),
        'vars': [_("Contract"), _("Provider")], 
    }
    return render(request, template_name, context)

def annotation_delete(request, slug):    
    annotation = get_object_or_404(Annotation, slug=slug)    
    slug = annotation.contract.slug  
    if request.method == 'POST':        
       try:
           annotation.delete()
           messages.success(request, _('Completed successful.'))
           return redirect('annotation:url_annotations_list', contract=slug)
       except IntegrityError:
           messages.warning(request, _('You cannot delete. This annotation has an existing deal.'))
           return redirect('annotation:url_annotations_list', contract=slug)    

def annotation_delete_all(request):
    marc = 0    
    if request.method == "POST":        
        context = request.POST["checkbox_selected"].split(",")
        context = [str(x) for x in context]      
        if context:  
            contract_slug = Annotation.objects.prefetch_related('contract').values('contract__slug').distinct()
            contract_slug = contract_slug[0]['contract__slug']               
            b = Annotation.objects.filter(slug__in=context)            
            for i in b:                
                try:
                    i.delete()
                except IntegrityError:
                    marc = 1                    
    if marc == 0:
        messages.success(request, _('Completed successful.'))
    else:
        messages.warning(request, _('You cannot delete. This annotation has an existing deal.'))
    
    return redirect('annotation:url_annotations_list', contract=contract_slug)
    
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

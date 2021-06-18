from django.shortcuts import render,get_object_or_404, get_list_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.utils.translation import ugettext as _
from django.contrib import messages
from .models import Contract
from .form import ContractForm
from account.models import User
from django.db import IntegrityError
from django.db.models import Q, Sum, Count, Prefetch
import os
import json

####### CONTRACT  ################

def contract_save_form(request,form,template_name, data, user_created=None):    
    if request.method == 'POST':                                              
        if form.is_valid():
            obj = form.save(commit=False)                                   
            if user_created:# Se cair aqui é EDIT                               
                obj.user_created = user_created                
            else:# Se cair aqui é CREATE                
                obj.user_created = request.user
            obj.user_updated = request.user  
            obj.save()         
                
            return redirect('contract:url_contracts_list')
        else:
            print("algo não está valido.")               
    
    data['form'] = form
    return render(request,template_name,data)

def contract_create(request):
    template_name = 'contract/form.html'    
    data = {
            "title": _("Create Contract"),
            "back":_("Back"),
            "save":_("Save"),
            "clear":_("Clear"),
        }    
    if request.method == 'POST':                       
        form = ContractForm(request.POST, request.FILES)                
    else:
        form = ContractForm()             
    
    return contract_save_form(request, form, template_name, data)

def contract_edit(request, slug):    
    template_name='contract/form.html'
    data = {
            "title": _("Edit"),
            "back":_("Back"),
            "save":_("Save"),
            "clear":_("Clear"),
        }    
    contract = get_object_or_404(Contract, slug=slug)           
    user_created = contract.user_created # Esta linha faz com que o user_created não seja modificado, para mostrar quem criou esta pessoa    
    if request.method == 'POST':        
        form = ContractForm(request.POST, request.FILES, instance=contract)                
    else:
        form = ContractForm(instance=contract)       
    return contract_save_form(request, form, template_name, data, user_created=user_created)
    
def contracts_list(request):
    template_name = "contract/list.html"
    contracts = Contract.objects.filter(status='Ativo')   
    context = {
        'contracts': contracts,
        'title': _("Registered Contracts"),
        'add': _("Add")      
    }
    return render(request,template_name,context)

def contracts_list_inactives(request):
    template_name = "contract/list.html"
    contracts = Contract.objects.filter(status='Encerrado')    
    context = {
        'contracts': contracts,
        'title': _("Inactives Contracts"),
        'add': _("Add")      
    }
    return render(request,template_name,context)

def contract_detail(request, slug):    
    template_name = "contract/detail.html"
    contract = get_object_or_404(Contract,slug=slug)
    context = {
        'contract': contract,
        'title': _("Detail Info"),
        'edit': _("Edit"),
        'list_all': _("List All")
    }
    return render(request, template_name, context)

def contract_delete(request, slug):    
    contract = get_object_or_404(Contract, slug=slug)    
    if request.method == 'POST':        
       try:
           contract.delete()
           messages.success(request, _('Completed successful.'))
           return redirect('contract:url_contracts_list')
       except IntegrityError:
           messages.warning(request, _('You cannot delete. This contract has an existing tax invoices.'))
           return redirect('contract:url_contracts_list')    

def contract_delete_all(request):
    marc = 0    
    if request.method == "POST":        
        context = request.POST["checkbox_selected"].split(",")
        context = [str(x) for x in context]      
        if context:                
            b = Contract.objects.filter(slug__in=context)            
            for i in b:                
                try:
                    i.delete()
                except IntegrityError:
                    marc = 1                    
    if marc == 0:
        messages.success(request, _('Completed successful.'))
    else:
        messages.warning(request, _('You cannot delete. This contract has an existing tax invoices.'))
    
    return redirect('contract:url_contracts_list')
    
########### FIM COMPANY ############################

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

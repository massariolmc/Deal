from django.shortcuts import render,get_object_or_404, get_list_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.utils.translation import ugettext as _
from django.contrib import messages
from .models import TaxInvoice
from .form import TaxInvoiceForm
from contract.models import Contract
from account.models import User
from django.db import IntegrityError
from django.db.models import Q, Sum, Count, Prefetch
import os
import json
import sys

####### CONTRACT  ################

def tax_invoice_save_form(request,form,template_name, data, user_created=None):    
    if request.method == 'POST':                                              
        if form.is_valid():
            obj = form.save(commit=False)                                   
            if user_created:# Se cair aqui é EDIT                               
                obj.user_created = user_created                
            else:# Se cair aqui é CREATE                
                obj.user_created = request.user
            obj.user_updated = request.user  
            obj.save()         
                
            return redirect('tax_invoice:url_tax_invoices_list', data['contract'].slug)
        else:
            print("algo não está valido.")               
    
    data['form'] = form
    return render(request,template_name,data)

def tax_invoice_create(request, contract):
    contract = get_object_or_404(Contract, slug=contract)
    template_name = 'tax_invoice/form.html'    
    data = {
            "title": _("Create TaxInvoice"),
            "back":_("Back"),
            "save":_("Save"),
            "clear":_("Clear"),
            "contract": contract,
            "vars": [_("Provider"),], 
        }    
    if request.method == 'POST':                       
        form = TaxInvoiceForm(request.POST, request.FILES,contract=contract.id)                
    else:
        form = TaxInvoiceForm(contract=contract.id)             
    
    return tax_invoice_save_form(request, form, template_name, data)

def tax_invoice_edit(request, slug): 
    tax_invoice = get_object_or_404(TaxInvoice, slug=slug)           
    contract = get_object_or_404(Contract, slug=tax_invoice.contract.slug)   
    template_name='tax_invoice/form.html'
    data = {
            "title": _("Edit"),
            "back":_("Back"),
            "save":_("Save"),
            "clear":_("Clear"),
            "contract": contract,
            "vars": [_("Provider"),],
        }    
    
    user_created = tax_invoice.user_created # Esta linha faz com que o user_created não seja modificado, para mostrar quem criou esta pessoa    
    if request.method == 'POST':        
        form = TaxInvoiceForm(request.POST, request.FILES, instance=tax_invoice)                
    else:
        form = TaxInvoiceForm(instance=tax_invoice)       
    return tax_invoice_save_form(request, form, template_name, data, user_created=user_created)
    
def tax_invoices_list(request,contract):
    contract = get_object_or_404(Contract, slug=contract)  
    template_name = "tax_invoice/list.html"
    tax_invoices = TaxInvoice.objects.filter(contract=contract.id)    
    context = {
        'tax_invoices': tax_invoices,
        'contract': contract,
        'title': _("Registered TaxInvoices"),
        'add': _("Add"),
        'vars': [_("Contract"), _("Provider")],      
    }    
    return render(request,template_name,context)

def providers_choose(request):
    template_name = "tax_invoice/providers_choose.html"
    contracts = Contract.objects.filter(status='Ativo')        
    context = {
        'contracts': contracts,
        'title': _("Choose Provider"),
        'add': _("Add Provider")      
    }
    return render(request,template_name,context)

def tax_invoice_detail(request, slug):    
    template_name = "tax_invoice/detail.html"
    tax_invoice = get_object_or_404(TaxInvoice,slug=slug)
    contract = get_object_or_404(Contract,slug=tax_invoice.contract.slug)
    context = {
        'tax_invoice': tax_invoice,
        'contract': contract,
        'title': _("Detail Info"),
        'edit': _("Edit"),
        'list_all': _("List All"),
        'vars': [_("Provider"),_("Number Invoice")]
    }
    return render(request, template_name, context)

def tax_invoice_delete(request, slug):    
    tax_invoice = get_object_or_404(TaxInvoice, slug=slug)  
    slug = tax_invoice.contract.slug      
    if request.method == 'POST':        
       try:
           tax_invoice.delete()
           messages.success(request, _('Completed successful.'))
           return redirect('tax_invoice:url_tax_invoices_list', contract=slug)
       except IntegrityError:
           messages.warning(request, _('You cannot delete. This tax_invoice has an existing department.'))
           return redirect('tax_invoice:url_tax_invoices_list', contract=slug)    

def tax_invoice_delete_all(request):
    marc = 0    
    if request.method == "POST":        
        context = request.POST["checkbox_selected"].split(",")
        context = [str(x) for x in context]              
        if context:                
            contract_slug = TaxInvoice.objects.prefetch_related('contract').values('contract__slug').distinct()
            contract_slug = contract_slug[0]['contract__slug']                        
            b = TaxInvoice.objects.filter(slug__in=context)            
            for i in b:                
                try:
                    i.delete()
                except IntegrityError:
                    marc = 1                    
    if marc == 0:
        messages.success(request, _('Completed successful.'))
    else:
        messages.warning(request, _('You cannot delete. This tax_invoice has an existing department.'))
    
    return redirect('tax_invoice:url_tax_invoices_list', contract=contract_slug)
    
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
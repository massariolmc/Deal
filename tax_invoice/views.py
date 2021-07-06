from django.shortcuts import render,get_object_or_404, get_list_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.utils.translation import ugettext as _
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import TaxInvoice, UploadTaxInvoice
from .form import TaxInvoiceForm
from contract.models import Contract
from account.models import User
from django.db import IntegrityError
from django.db.models import Q, Sum, Count, Prefetch
import os
import json
import sys
from hurry.filesize import size, iec, si # converter GB,MB para template
import magic # Mesma coisa que o file no linux, verificar o formato do arquivo

####### CONTRACT  ################

###validação do upload
def validation_files(pdf_contract):
        print("validação")                    
        size_max = 3000000
        formats = "PDF"
        msg_size =  _(f"Maximum size allowed {size(size_max, system=si)}")
        msg_format =  _(f"This format not allowed {formats}")
        if pdf_contract:   
            file = magic.from_buffer(pdf_contract.read()) 
            print("valor do file",file)  
            if pdf_contract.size > size_max:
                return False
            elif not formats in file: 
                return False
            else:
                return True
        return False

def tax_invoice_save_form(request,form,template_name, data, user_created=None):    
    if request.method == 'POST':  
        files = request.FILES.getlist('pdf_invoice')                                            
        if form.is_valid():
            obj = form.save(commit=False)                                   
            if user_created:# Se cair aqui é EDIT                               
                obj.user_created = user_created                
            else:# Se cair aqui é CREATE                
                obj.user_created = request.user
            obj.user_updated = request.user  
            obj.save()   
            ###### Faz a parte do Upload #################
            val = list()
            arqs = ""
            for file in files:
                if validation_files(file):
                    UploadTaxInvoice.objects.create(pdf_tax_invoice=file, tax_invoice=obj, user_created=request.user,user_updated=request.user )
                else:
                   val.append(file)                              
            if val:
                for i in val:
                    arqs += f"{i}, "
                messages.warning(request, _(f"Errors in the following files: {arqs}. Maximum size allowed: 3MB. This format is allowed: PDF"))       
            ###### FIM Faz a parte do Upload #################    
            return redirect('tax_invoice:url_tax_invoices_list', data['contract'].slug)
        else:
            print("algo não está valido.")               
    
    data['form'] = form
    return render(request,template_name,data)

@login_required
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
        form = TaxInvoiceForm(request.POST, request.FILES,contract=contract)                
    else:
        form = TaxInvoiceForm(contract=contract)             
    
    return tax_invoice_save_form(request, form, template_name, data)

@login_required
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

@login_required    
def tax_invoices_list(request,contract):
    contract = get_object_or_404(Contract, slug=contract)  
    template_name = "tax_invoice/list.html"
    tax_invoices = TaxInvoice.objects.filter(contract=contract.id)    
    context = {
        'tax_invoices': tax_invoices,
        'contract': contract,
        'title': _("Registered TaxInvoices"),
        'add': _("Add"),
        'back': _("Back"),
        'vars': [_("Contract"), _("Provider")],      
    }    
    return render(request,template_name,context)

@login_required
def providers_choose(request):
    template_name = "tax_invoice/providers_choose.html"
    contracts = Contract.objects.filter(status='Ativo')        
    context = {
        'contracts': contracts,
        'title': _("Entry with a tax invoice"),
        'add': _("Add Contract")      
    }
    return render(request,template_name,context)

@login_required
def tax_invoice_detail(request, slug):    
    template_name = "tax_invoice/detail.html"
    tax_invoice = get_object_or_404(TaxInvoice,slug=slug)
    contract = get_object_or_404(Contract,slug=tax_invoice.contract.slug)
    pdfs = UploadTaxInvoice.objects.prefetch_related('tax_invoice').filter(tax_invoice=tax_invoice)
    context = {
        'tax_invoice': tax_invoice,
        'contract': contract,
        'title': _("Detail Info"),
        'edit': _("Edit"),
        'list_all': _("List All"),
        'vars': [_("Provider"),_("Number Invoice")],
        'pdfs': pdfs,
    }
    return render(request, template_name, context)

@login_required
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

@login_required
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

@login_required
def upload_delete(request, slug):    
    upload = get_object_or_404(UploadTaxInvoice, slug=slug)   
    tax_invoice =  upload.tax_invoice.slug
    if request.method == 'POST':        
       try:
           upload.delete()
           messages.success(request, _('Completed successful.'))
           return redirect('tax_invoice:url_tax_invoice_detail', tax_invoice)
       except IntegrityError:
           messages.warning(request, _('You cannot delete. This contract has an existing tax invoices.'))
           return redirect('tax_invoice:url_tax_invoice_detail', tax_invoice)
    
########### FIM TAX INVOICE ############################

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
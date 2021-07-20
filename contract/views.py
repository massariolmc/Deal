from django.shortcuts import render,get_object_or_404, get_list_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.utils.translation import ugettext as _
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Contract, UploadContract, ContractCompany
from .form import ContractForm,UploadContractForm, validation_files
from company.models import Company
from django.forms import modelformset_factory, inlineformset_factory
from account.models import User
from django.db import IntegrityError
from django.db.models import Q, Sum, Count, Prefetch
from .slug_file import unique_uuid
import os
import sys
import json

####### CONTRACT  ################

def contract_save_form(request,form, template_name, data, user_created=None):    
    if request.method == 'POST':
        ### USADO PARA O MANY TO MANY ###################### 
        members_contract_list = list()        
        company_list = list() 
        compare = set() 
        if user_created:# Se cair aqui é EDIT 
            print("mudou",form.has_changed())    
            print("quem",form.changed_data) 
            print("instance",form.instance.members_contract.values('id'))                                                
            members_contract_initals = form.instance.members_contract.values('id')                  
            for v in members_contract_initals:
                members_contract_list.append(v['id'])
            print("mostra todos",members_contract_list)
        ### FIM USADO PARA O MANY TO MANY #################

        if form.is_valid():               
            companies = form.cleaned_data["members_contract"]                    
            obj = form.save(commit=False)                                               
            if user_created:# Se cair aqui é EDIT                               
                obj.user_created = user_created # Não deixa atualizar quem criou                
            else:# Se cair aqui é CREATE                
                obj.user_created = request.user
            obj.user_updated = request.user  
            obj.save()
            #form.save_m2m()
            
            ### USADO PARA O MANY TO MANY ###################### 
            for company in companies:           
                print("company",company.id)
                company_list.append(company.id)                
                obj.members_contract.add(company, through_defaults={'slug': unique_uuid(ContractCompany),'user_created':request.user, 'user_updated':request.user})
            compare.update(members_contract_list)
            id_cc = compare.difference(company_list)
            if id_cc:
                print("valor", id_cc)
                for i in id_cc:
                    obj.members_contract.remove(get_object_or_404(Company, id=i))
             ### FIM USADO PARA O MANY TO MANY #################
                
            return redirect('contract:url_contract_detail', obj.slug)
        else:
            print("algo não está valido.")               
    
    data['form'] = form    
    return render(request,template_name,data)

@login_required
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

@login_required
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

@login_required    
def contracts_list(request):
    template_name = "contract/list.html"
    contracts = Contract.objects.prefetch_related('members_contract').filter(status='Ativo')   
    context = {
        'contracts': contracts,
        'title': _("Registered Contracts"),
        'add': _("Add"),
        'back': _("Back"),    
    }
    return render(request,template_name,context)

@login_required
def contracts_list_inactives(request):
    template_name = "contract/list.html"
    contracts = Contract.objects.prefetch_related('members_contract').filter(status='Encerrado')    
    context = {
        'contracts': contracts,
        'title': _("Inactives Contracts"),
        'add': _("Add"),
        'back': _("Back"),    
    }
    return render(request,template_name,context)

@login_required
def contract_detail(request, slug):    
    template_name = "contract/detail.html"
    contract = get_object_or_404(Contract,slug=slug)
    upload_contract = upload_contract_create(request,contract)
    pdfs = UploadContract.objects.prefetch_related('contract').filter(contract=contract)
    contract = Contract.objects.prefetch_related('members_contract').get(slug=slug)    
    companies = contract.members_contract.all()           
    context = {
        'contract': contract,
        'companies': companies,
        'title': _("Detail Info"),
        'edit': _("Edit"),       
        'annotations': _("Annotations"),
        'attachments': _("Attachments"),
        'list_all': _("List All"),
        'form': upload_contract,
        'pdfs': pdfs,
    }
    return render(request, template_name, context)

@login_required
def contract_delete(request, slug):    
    contract = get_object_or_404(Contract, slug=slug)    
    if request.method == 'POST':        
       try:
           contract.delete()
           messages.success(request, _('Completed successful.'))
           return redirect('contract:url_contracts_list')
       except IntegrityError:
           messages.warning(request, _('You cannot delete. This contract has an existing tax invoices or files attachments.'))
           return redirect('contract:url_contracts_list')    

@login_required
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
        messages.warning(request, _('You cannot delete. This contract has an existing tax invoices or files attachments.'))
    
    return redirect('contract:url_contracts_list')
   
########### FIM CONTRACT ############################

########### CONTRACT WITH UPLOAD CONTACT ###########

@login_required
def upload_contract_create(request, contract):      
    if contract.__class__  is int:          
        contract = get_object_or_404(Contract, pk=contract)  
        val = list()  
        arqs = ""
    if request.method == 'POST':
        if not request.FILES.getlist('pdf_contract'):
            return redirect('contract:url_contract_detail', contract.slug)    
        files = request.FILES.getlist('pdf_contract')    
        form = UploadContractForm(request.POST, request.FILES)                                            
        print("Files", files)                
        if form.is_valid():                                                           
            for file in files:
                if validation_files(file):
                    UploadContract.objects.create(pdf_contract=file, contract=contract, user_created=request.user,user_updated=request.user )
                else:
                   val.append(file)                              
            if val:
                for i in val:
                    arqs += f"{i}, "
                messages.warning(request, _(f"Errors in the following files: {arqs}. Maximum size allowed: 3MB. This format is allowed: PDF"))                
            return redirect('contract:url_contract_detail', contract.slug)

        else:                    
            print("não validou",form.errors)   
            messages.warning(request, _("File not added. This name already exists or was entered incorrectly"))                
            return redirect('contract:url_contract_detail', contract.slug)             
    else:
        form = UploadContractForm()
        return form

@login_required
def upload_delete(request, slug):    
    upload_contract = get_object_or_404(UploadContract, slug=slug)   
    contract =  upload_contract.contract.slug
    if request.method == 'POST':        
       try:
           upload_contract.delete()
           messages.success(request, _('Completed successful.'))
           return redirect('contract:url_contract_detail', contract)
       except IntegrityError:
           messages.warning(request, _('You cannot delete. This contract has an existing tax invoices.'))
           return redirect('contract:url_contract_detail', contract)

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

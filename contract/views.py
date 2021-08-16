from django.shortcuts import render,get_object_or_404, get_list_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.utils.translation import ugettext as _
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from .models import Contract, UploadContract, ContractCompany, CostCenter, NimbiContract, DepartmentContract, UserContract
from .form import ContractForm,UploadContractForm, validation_files, NimbiContractForm, DepartmentContractForm, UserContractForm
from .decorators import user_has_access_contract, user_contract_delete
from company.models import Company, Department
from contact_provider.models import ContactProvider
from contact_provider.form import ContactProviderForm
from django.forms import modelformset_factory, inlineformset_factory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.template.loader import render_to_string
from account.models import User
from django.db import IntegrityError
from django.db.models import Q, Sum, Count, Prefetch
from .slug_file import unique_uuid
import os
import sys
import json
from datetime import date, datetime, timedelta
from django.urls import reverse

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

@login_required(login_url='login')
@permission_required('signup.add_choice', login_url='core:url_not_authorized')
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

@login_required(login_url='login')
@user_has_access_contract
def contract_edit(request, slug):    
    contract = get_object_or_404(Contract, slug=slug)      
    template_name='contract/form.html'
    data = {
            "title": _("Edit"),
            "back":_("Back"),
            "save":_("Save"),
            "clear":_("Clear"),
        }                   
    user_created = contract.user_created # Esta linha faz com que o user_created não seja modificado, para mostrar quem criou esta pessoa    
    if request.method == 'POST':        
        form = ContractForm(request.POST, request.FILES, instance=contract)                
    else:
        form = ContractForm(instance=contract)       
    return contract_save_form(request, form, template_name, data, user_created=user_created)

@login_required(login_url='login')   
def contracts_list(request):
    template_name = "contract/list.html"
    data = {}
    contracts = ""
    if request.user.is_superuser:        
        contracts = Contract.objects.prefetch_related('members_contract').prefetch_related('members_contract').filter(status='Ativo')               
    else:
        contracts = request.user.members_user_contract.prefetch_related('members_contract').filter(status='Ativo')        
    
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
                Q(provider__name__icontains=query) | Q(name__icontains=query) | Q(type__name__icontains=query) | Q(annual_budget__icontains=query) |
                Q(members_contract__name__icontains=query) | Q(members_contract__cnpj__icontains=query)
                
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
        objs = search(request, query,lines,contracts)
        data['html_signup_list'] = render_to_string('contract/_table.html', {'contracts': objs})       
        return JsonResponse(data)
            
                 
    lines = 10
    contracts = pagination(request,contracts,int(lines))

    context = {
        'contracts': contracts,
        'title': _("List Actives Contracts"),
        'add': _("Add"),
        'back': _("Back"),    
    }
    return render(request,template_name,context)

@login_required(login_url='login')
def contracts_list_inactives(request):
    template_name = "contract/list.html" 
    data = {}
    contracts = ""
    if request.user.is_superuser:        
        contracts = Contract.objects.prefetch_related('members_contract').prefetch_related('members_contract').filter(status='Encerrado')               
    else:
        contracts = request.user.members_user_contract.prefetch_related('members_contract').filter(status='Encerrado')        
    
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
                Q(provider__name__icontains=query) | Q(name__icontains=query) | Q(type__name__icontains=query) | Q(annual_budget__icontains=query) |
                Q(members_contract__name__icontains=query) | Q(members_contract__cnpj__icontains=query)
                
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
        objs = search(request, query,lines,contracts)
        data['html_signup_list'] = render_to_string('contract/_table.html', {'contracts': objs})       
        return JsonResponse(data)
            
                 
    lines = 10
    contracts = pagination(request,contracts,int(lines))    

    context = {
        'contracts': contracts,
        'title': _("Inactives Contracts"),
        'add': _("Add"),
        'back': _("Back"),    
    }
    return render(request,template_name,context)

@login_required(login_url='login')
@user_has_access_contract
def contract_detail(request, slug):    
    template_name = "contract/detail.html"
    contract = get_object_or_404(Contract,slug=slug)
    upload_contract = upload_contract_create(request,contract)
    nimbi_contract = nimbi_contract_create(request,contract.slug)
    form_contact = contact_provider_create(request,contract.slug)
    form_department_contract = department_contract_create(request,contract.slug)    
    pdfs = UploadContract.objects.prefetch_related('contract').filter(contract=contract)
    nimbi = NimbiContract.objects.prefetch_related('contract').filter(contract=contract)
    contacts = ContactProvider.objects.prefetch_related('contract').filter(contract=contract)    
    contract = Contract.objects.prefetch_related('members_contract').get(slug=slug) 
    departments_contract = contract.members_cost_center.all()    
    companies = contract.members_contract.all()    
    users_contract = contract.members_user.all()           
    context = {
        'contract': contract,
        'companies': companies,
        'title': _("Detail Info"),
        'edit': _("Edit"),       
        'annotations': _("Annotations"),
        'attachments': _("Add"),
        'nimbi_alias': _("Add"),
        'cost_center_alias': _("Add"),
        'user_alias': _("Users"),
        'contact_alias': _("Add"),
        'list_contracts_inactives': _("Inactives Contracts"),
        'list_contracts_actives': _("List Actives Contracts"),
        'form': upload_contract,
        'form_nimbi': nimbi_contract,
        'form_contact': form_contact,
        'form_department_contract': form_department_contract,        
        'pdfs': pdfs,
        'nimbi': nimbi,
        'departments_contract': departments_contract,        
        'contacts': contacts,
        'users_contract': users_contract,
    }
    return render(request, template_name, context)

@login_required(login_url='login')
@user_contract_delete
@user_has_access_contract
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

@login_required(login_url='login')
@user_contract_delete
@user_has_access_contract
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


#################### CONTROLE DE VENCIMENTO DE BOLETO, CONTRATOS (RENOVAÇÕES E TÉRMINOS)

@login_required(login_url='login')
def contract_invoice_date(request):# Controla o dia do vencimento do boleto ou fatura
    template_name = 'contract/list_contract_invoice_date.html'
    contracts = Contract.objects.filter(status='Ativo').order_by("-pay_day")    
    data = []
    def cal_time(month,year,contracts, label=None): 
        today = date.today()  
        marc = 0
        data = []    
        fields = {}
        for i in contracts:    
            #print("i", i.pay_day)
            if i.pay_day:        
                date_contract = date(int(year),int(month),int(i.pay_day))            
                if date_contract > today:
                    r_days = date_contract - today
                    marc = 0
                elif date_contract <= today:
                    r_days = today - date_contract
                    marc = -1                               
                fields = {
                    'id': i.id,
                    'name': i.name,
                    'provider': i.provider,
                    label: i.pay_day,
                    'marc': marc,
                    'left': r_days.days
                }
                data.append(fields)   
        return data

    if request.method == "POST":        
        month,year = request.POST["sel"].split("/")        
        data = cal_time(month,year,contracts)
         
    else:
        month = date.today().month
        year = date.today().year
        data = cal_time(month,year,contracts, label='pay_day')

    context = {        
        'contracts': data,
        'title': _("Invoice Dates"),
        'date': f"Mês da pesquisa: {month}/{year}",
        'back': _("Back"),    
    }  
    return render(request,template_name,context)

@login_required(login_url='login')
def contract_due_date(request):# Controla as datas de renovação do contrato
    template_name = 'contract/list_contract_due_date.html'
    if request.user.is_superuser:        
        #contracts = Contract.objects.prefetch_related('members_contract').filter(status='Ativo')
        contracts = Contract.objects.prefetch_related('members_contract').filter(status='Ativo').order_by("dt_renovation")               
    else:
        contracts = request.user.members_user_contract.filter(status='Ativo').order_by("dt_renovation")                
        
    data = {}

    def cal_time(month,year,contracts,label=None): 
        today = date.today()  
        marc = 0
        data = []    
        fields = {}
        for i in contracts:    
            print("i", i.dt_renovation)
            if i.dt_renovation:        
                date_contract = i.dt_renovation
                if date_contract > today:
                    r_days = date_contract - today
                    marc = 0
                elif date_contract <= today:
                    r_days = today - date_contract
                    marc = -1                               
                fields = {
                    'id': i.id,
                    'name': i.name,
                    'provider': i.provider,
                    label: i.dt_renovation,
                    'marc': marc,
                    'left': r_days.days
                }
                data.append(fields)   
        return data 
    
    month = date.today().month
    year = date.today().year
    contracts = cal_time(month,year,contracts,label='dt_renovation')  

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
        if query:
            print("entrei")
            obj_search = Contract.objects.filter(
                Q(provider__name__icontains=query) | Q(name__icontains=query) |
                Q(dt_renovation__icontains=query) 
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
        objs = search(request, query,lines,contracts)
        data['html_signup_list'] = render_to_string('contract/_table_contract_due_date.html', {'contracts': objs})       
        return JsonResponse(data)
            
                 
    lines = 10
    contracts = pagination(request,contracts,int(lines))  
        
    context = {        
        'contracts': contracts,
        'title': _("Due Date"),
        'date': f"Mês da pesquisa: {month}/{year}",
        'back': _("Back"),    
    }  
    return render(request,template_name,context)

@login_required(login_url='login')
def contract_finish(request):# Controla as datas de término do contrato
    template_name = 'contract/list_contract_finish.html'
    if request.user.is_superuser:        
        #contracts = Contract.objects.prefetch_related('members_contract').filter(status='Ativo')
        contracts = Contract.objects.prefetch_related('members_contract').filter(status='Ativo').order_by("dt_end")                
    else:
        contracts = request.user.members_user_contract.filter(status='Ativo').order_by("dt_end") 
        
    data = {}
    def cal_time(month,year,contracts,label=None): 
        today = date.today()  
        marc = 0
        data = []    
        fields = {}
        for i in contracts:    
            print("i", i.dt_end)
            if i.dt_end:        
                date_contract = i.dt_end
                if date_contract > today:
                    r_days = date_contract - today
                    marc = 0
                elif date_contract <= today:
                    r_days = today - date_contract
                    marc = -1                               
                fields = {
                    'id': i.id,
                    'name': i.name,
                    'provider': i.provider,
                    label: i.dt_end,
                    'marc': marc,
                    'left': r_days.days
                }
                data.append(fields)   
        return data 

    month = date.today().month
    year = date.today().year
    contracts = cal_time(month,year,contracts,label='dt_end')        

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
        if query:
            print("entrei")
            obj_search = Contract.objects.filter(
                Q(provider__name__icontains=query) | Q(name__icontains=query) |
                Q(dt_end__icontains=query) 
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
        objs = search(request, query,lines,contracts)
        data['html_signup_list'] = render_to_string('contract/_table_contract_finish.html', {'contracts': objs})       
        return JsonResponse(data)
            
                 
    lines = 10
    contracts = pagination(request,contracts,int(lines))  

    context = {        
        'contracts': contracts,
        'title': _("Contract Finish"),        
        'back': _("Back"),    
    }  
    return render(request,template_name,context)
################ FIM CONTROLE DE VENCIMENTO DE BOLETO, CONTRATOS (RENOVAÇÕES E TÉRMINOS) #######

########### FIM CONTRACT ############################



########### CONTRACT WITH UPLOAD CONTACT ###########

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

#NIMBI CONTRACT

def nimbi_contract_create(request, contract):                       
    data = {}
    if request.method == 'POST':
        contract = get_object_or_404(Contract, slug=contract)            
        form = NimbiContractForm(request.POST, request.FILES)                                                            
        if form.is_valid():
            obj = form.save(commit=False)
            obj.contract = contract                                                         
            obj.user_created = request.user
            obj.user_updated = request.user  
            obj.save()         
                
            return redirect('contract:url_contract_detail', contract.slug)
        else:
            print("algo não está valido.")
            messages.warning(request, _("Verify informations in the Nimbi fields. Maybe the dates are incorrect."))                
            return redirect('contract:url_contract_detail', contract.slug)
                           
    else:
        form = NimbiContractForm()
        return form    


def nimbi_contract_delete(request, slug):    
    nimbi_contract = get_object_or_404(NimbiContract, slug=slug)   
    contract =  nimbi_contract.contract.slug
    if request.method == 'POST':        
       try:
           nimbi_contract.delete()
           messages.success(request, _('Completed successful.'))
           return redirect('contract:url_contract_detail', contract)
       except IntegrityError:
           messages.warning(request, _('You cannot delete. This contract has an existing tax invoices.'))
           return redirect('contract:url_contract_detail', contract)

########### PROVIDER WITH CONTACT_PROVIDER ###########

def contact_provider_create(request, contract):     
    data = {}
    contract = get_object_or_404(Contract, slug=contract)    
    if request.method == 'POST':
        form = ContactProviderForm(request.POST)        
        if form.is_valid():
            obj = form.save(commit=False)
            obj.contract = contract                                                         
            obj.user_created = request.user
            obj.user_updated = request.user  
            obj.save()                      
                   
            return redirect('contract:url_contract_detail', contract.slug)
        else:            
            messages.warning(request, _("Contact not added. This name already exists or was entered incorrectly"))    
            return redirect('contract:url_contract_detail', contract.slug)             
    else:
        form = ContactProviderForm()
        return form


def contact_provider_delete(request, slug):    
    contact_provider = get_object_or_404(ContactProvider, slug=slug)   
    contract =  contact_provider.contract.slug
    if request.method == 'POST':        
       try:
           contact_provider.delete()
           messages.success(request, _('Completed successful.'))
           return redirect('contract:url_contract_detail', contract)
       except IntegrityError:
           messages.warning(request, _('You cannot delete. This contract has an existing tax invoices.'))
           return redirect('contract:url_contract_detail', contract)

########### PROVIDER WITH CONTACT_PROVIDER ###########

########### DEPARTMENT CONTRACT - COST CENTER ##########

def department_contract_create(request, contract):     
    data = {}
    contract = get_object_or_404(Contract, slug=contract)    
    if request.method == 'POST':
        form = DepartmentContractForm(request.POST, contract=contract)        
        if form.is_valid():
            obj = form.save(commit=False)                
            contract.members_cost_center.add(obj.number_cost_center, through_defaults={'slug': unique_uuid(DepartmentContract),'user_created':request.user, 'user_updated':request.user})              
            
            messages.success(request, _('Completed successful.'))   
            return redirect('contract:url_contract_detail', contract.slug)
        else:            
            messages.warning(request, _("Contact not added. This name already exists or was entered incorrectly"))    
            return redirect('contract:url_contract_detail', contract.slug)             
    else:
        form = DepartmentContractForm(contract=contract)
        return form

def department_contract_delete(request, slug_department, slug_contract):    
    contract = get_object_or_404(Contract, slug=slug_contract)   
    department = get_object_or_404(Department, slug=slug_department)   
        
    if request.method == 'POST':        
       try:
           contract.members_cost_center.remove(department)
           messages.success(request, _('Completed successful.'))
           return redirect('contract:url_contract_detail', contract.slug)
       except IntegrityError:
           messages.warning(request, _('You cannot delete. This contract has an existing tax invoices.'))
           return redirect('contract:url_contract_detail', contract.slug)

########### DEPARTMENT CONTRACT - COST CENTER ###########

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

############## SOMENTE PARA CONSULTA DO CENTRO DE CUSTO - EU INSERI ESSE DADOS DE UM CSV. NÃO TEM FORM PARA ELE #########
@login_required(login_url='login')
def cost_center_list(request):
    template_name = 'contract/list_cost_centers.html'
    cost_centers_find = CostCenter.objects.all()#.order_by('-name')
    data = dict()      

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

    if request.is_ajax():
        query = request.GET.get('q')
        lines = request.GET.get('l')
        obj_search = ""              
        if query:
            obj_search = CostCenter.objects.filter(
                Q(cod__icontains=query) | Q(name__icontains=query) |
                Q(branch__icontains=query) | Q(plant__icontains=query) | Q(created_at__icontains=query)
            ).distinct() 
        else:
            print("Não existe") 
            obj_search = CostCenter.objects.all()#.order_by('-first_name')            

        objs = pagination(request,obj_search,int(lines))                           
    
        data['html_signup_list'] = render_to_string('contract/_table_cost_center.html', {'cost_centers': objs})       
        return JsonResponse(data)
            
                 
    lines = 10
    cost_centers = pagination(request,cost_centers_find,int(lines))   
    data = {
        'cost_centers': cost_centers,
        'title': _("List Cost Centers"),
        'add': _("Add"),
    }    
    return render(request,template_name,data)
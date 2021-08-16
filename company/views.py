from django.shortcuts import render,get_object_or_404, get_list_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.utils.translation import ugettext as _
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from .models import Company, Department
from .form import CompanyForm, DepartmentForm
from .decorators import verify_superuser
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string
from django.http import JsonResponse
from account.models import User
from django.db import IntegrityError
from django.db.models import Q, Sum, Count, Prefetch
import os
import json

####### COMPANY  ################

def company_save_form(request,form,template_name, data, user_created=None):    
    if request.method == 'POST':                                              
        if form.is_valid():
            obj = form.save(commit=False)                                   
            if user_created:# Se cair aqui é EDIT                               
                obj.user_created = user_created                
            else:# Se cair aqui é CREATE                
                obj.user_created = request.user
            obj.user_updated = request.user  
            obj.save()         
                
            return redirect('company:url_company_detail', obj.slug)
        else:
            print("algo não está valido.")               
    
    data['form'] = form
    return render(request,template_name,data)

@login_required(login_url='login')
@verify_superuser
def company_create(request):
    template_name = 'company/form.html'    
    data = {
            "title": _("Create Company"),
            "back":_("Back"),
            "save":_("Save"),
            "clear":_("Clear"),
        }    
    if request.method == 'POST':                       
        form = CompanyForm(request.POST, request.FILES)                
    else:
        form = CompanyForm()             
    
    return company_save_form(request, form, template_name, data)

@login_required(login_url='login')
@verify_superuser
def company_edit(request, slug):    
    template_name='company/form.html'
    data = {
            "title": _("Edit"),
            "back":_("Back"),
            "save":_("Save"),
            "clear":_("Clear"),
        }    
    company = get_object_or_404(Company, slug=slug)           
    user_created = company.user_created # Esta linha faz com que o user_created não seja modificado, para mostrar quem criou esta pessoa    
    if request.method == 'POST':        
        form = CompanyForm(request.POST, request.FILES, instance=company)                
    else:
        form = CompanyForm(instance=company)       
    return company_save_form(request, form, template_name, data, user_created=user_created)

@login_required(login_url='login')
@verify_superuser
def companies_list(request):
    template_name = "company/list.html"
    companies = Company.objects.all() 
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
                Q(name__icontains=query) | Q(fantasy_name__icontains=query) | Q(cnpj__icontains=query) | Q(email__icontains=query) |
                Q(status__icontains=query)
                
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
        objs = search(request, query,lines,companies)
        data['html_signup_list'] = render_to_string('company/_table.html', {'companies': objs})       
        return JsonResponse(data)
            
                 
    lines = 10
    companies = pagination(request,companies,int(lines))    

    context = {
        'companies': companies,
        'title': _("Registered Companies"),
        'add': _("Add")      
    }
    return render(request,template_name,context)

@login_required(login_url='login')
@verify_superuser
def company_detail(request, slug):    
    template_name = "company/detail.html"
    company = get_object_or_404(Company,slug=slug)
    context = {
        'company': company,
        'title': _("Detail Info"),
        'edit': _("Edit"),
        'list_all': _("List Companies")
    }
    return render(request, template_name, context)

@login_required(login_url='login')
@verify_superuser
def company_delete(request, slug):    
    company = get_object_or_404(Company, slug=slug)    
    if request.method == 'POST':        
       try:
           company.delete()
           messages.success(request, _('Completed successful.'))
           return redirect('company:url_companies_list')
       except IntegrityError:
           messages.warning(request, _('You cannot delete. This company has an existing dependency.'))
           return redirect('company:url_companies_list')    


@login_required(login_url='login')
@verify_superuser
def company_delete_all(request):
    marc = 0    
    if request.method == "POST":        
        context = request.POST["checkbox_selected"].split(",")
        context = [str(x) for x in context]      
        if context:                
            b = Company.objects.filter(slug__in=context)            
            for i in b:                
                try:
                    i.delete()
                except IntegrityError:
                    marc = 1                    
    if marc == 0:
        messages.success(request, _('Completed successful.'))
    else:
        messages.warning(request, _('You cannot delete. This company has an existing dependency.'))
    
    return redirect('company:url_companies_list')
    
########### FIM COMPANY ############################

####### DEPARTMENT  ################

def department_save_form(request,form,template_name, data, user_created=None):    
    if request.method == 'POST':                                              
        if form.is_valid():
            obj = form.save(commit=False)                                   
            if user_created:# Se cair aqui é EDIT                               
                obj.user_created = user_created                
            else:# Se cair aqui é CREATE                
                obj.user_created = request.user
            obj.user_updated = request.user  
            obj.save()         
                
            return redirect('company:url_department_detail', obj.slug)
        else:
            print("algo não está valido.")               
    
    data['form'] = form
    return render(request,template_name,data)

@login_required(login_url='login')
@verify_superuser
def department_create(request):
    template_name = 'department/form.html'    
    data = {
            "title": _("Create Department"),
            "back":_("Back"),
            "save":_("Save"),
            "clear":_("Clear"),
        }    
    if request.method == 'POST':                       
        form = DepartmentForm(request.POST, request.FILES)                
    else:
        form = DepartmentForm()             
    
    return department_save_form(request, form, template_name, data)

@login_required(login_url='login')
@verify_superuser
def department_edit(request, slug):    
    template_name='department/form.html'
    data = {
            "title": _("Edit"),
            "back":_("Back"),
            "save":_("Save"),
            "clear":_("Clear"),
        }    
    department = get_object_or_404(Department, slug=slug)           
    user_created = department.user_created # Esta linha faz com que o user_created não seja modificado, para mostrar quem criou esta pessoa    
    if request.method == 'POST':        
        form = DepartmentForm(request.POST, request.FILES, instance=department)                
    else:
        form = DepartmentForm(instance=department)       
    return department_save_form(request, form, template_name, data, user_created=user_created)

@login_required(login_url='login')
@verify_superuser
def departments_list(request):
    template_name = "department/list.html"
    departments = Department.objects.select_related('company').all()
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
                Q(company__name__icontains=query) | Q(cod__icontains=query) | Q(name__icontains=query) | Q(plant__icontains=query) |
                Q(status__icontains=query)
                
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
        objs = search(request, query,lines,departments)
        data['html_signup_list'] = render_to_string('department/_table.html', {'departments': objs})       
        return JsonResponse(data)
            
                 
    lines = 10
    departments = pagination(request,departments,int(lines))    
    context = {
        'departments': departments,
        'title': _("Registered Departments"),
        'add': _("Add")      
    }
    return render(request,template_name,context)

@login_required(login_url='login')
@verify_superuser
def department_detail(request, slug):    
    template_name = "department/detail.html"
    department = get_object_or_404(Department,slug=slug)
    context = {
        'department': department,
        'title': _("Detail Info"),
        'edit': _("Edit"),
        'list_all': _("List Departments")
    }
    return render(request, template_name, context)

@login_required(login_url='login')
@verify_superuser
def department_delete(request, slug):    
    department = get_object_or_404(Department, slug=slug)    
    if request.method == 'POST':        
       try:
           department.delete()
           messages.success(request, _('Completed successful.'))
           return redirect('company:url_departments_list')
       except IntegrityError:
           messages.warning(request, _('You cannot delete. This department has an existing dependency.'))
           return redirect('compaby:url_departments_list')    

@login_required(login_url='login')
@verify_superuser
def department_delete_all(request):
    marc = 0    
    if request.method == "POST":        
        context = request.POST["checkbox_selected"].split(",")
        context = [str(x) for x in context]      
        if context:                
            b = Department.objects.filter(slug__in=context)            
            for i in b:                
                try:
                    i.delete()
                except IntegrityError:
                    marc = 1                    
    if marc == 0:
        messages.success(request, _('Completed successful.'))
    else:
        messages.warning(request, _('You cannot delete. This department has an existing dependency.'))
    
    return redirect('company:url_departments_list')
    
########### FIM DEPARTMENT ############################


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
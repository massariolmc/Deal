from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.template.loader import render_to_string
from .form import UserCreationForm, UserChangeForm
from account.models import User
from django.db import IntegrityError
from django.db.models import Q, Sum, Count, Prefetch
from django.utils.translation import ugettext, ugettext_lazy as _

def signup_save_form(request,form,template_name, data, user_created=None):    
    if request.method == 'POST':                                              
        if form.is_valid():
            obj = form.save(commit=False)                                   
            if user_created:# Se cair aqui é EDIT                               
                obj.user_created = user_created                
            else:# Se cair aqui é CREATE                
                obj.user_created = request.user
            obj.user_updated = request.user  
            obj.save()         
                
            return redirect('signup:url_signup_detail', obj.id)
        else:
            print("algo não está valido.")               
    
    data['form'] = form
    return render(request,template_name,data)

def signup_create(request):
    template_name = "signup/form.html"
    data = {
            "title": _("Create User"),
            "back":_("Back"),
            "save":_("Save"),
            "clear":_("Clear"),
        }    
    if request.method == 'POST':                       
        form = UserCreationForm(request.POST, request.FILES)                
    else:
        form = UserCreationForm()             
    
    return signup_save_form(request, form, template_name, data)   

def signup_list(request):
    template_name = 'signup/list.html'
    users_find = User.objects.all().order_by('-first_name')
    data = dict()      

    def pagination(request,users,lines=10):
        page = request.GET.get('page', 1)
        print("Valor de page: ",page)
        paginator = Paginator(users, int(lines))        
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        
        return users

    if request.is_ajax():
        query = request.GET.get('q')
        lines = request.GET.get('l')
        users_search = ""              
        if query:
            users_search = User.objects.filter(
                Q(cpf__icontains=query) | Q(first_name__icontains=query) |
                Q(last_name__icontains=query) | Q(email__icontains=query) | Q(created_at__icontains=query)
            ).distinct() 
        else:
            print("Não existe") 
            users_search = User.objects.all().order_by('-first_name')            

        users = pagination(request,users_search,int(lines))                           
    
        data['html_signup_list'] = render_to_string('signup/_table.html', {'users': users})       
        return JsonResponse(data)
            
                 
    lines = 10
    users = pagination(request,users_find,int(lines))   
    data = {
        'users': users,
        'title': _("Registered Users"),
        'add': _("Add"),
    }    
    return render(request,template_name,data)

def signup_edit(request,pk):
    template_name = 'signup/edit.html'     
    data = {
            "title": _("Edit"),
            "back":_("Back"),
            "save":_("Save"),
            "clear":_("Clear"),
        }    
    user = get_object_or_404(User, pk=pk)           
    user_created = user.user_created # Esta linha faz com que o user_created não seja modificado, para mostrar quem criou esta pessoa  
    if request.method == 'POST':        
        form = UserChangeForm(request.POST, request.FILES, instance=user)                
    else:
        form = UserChangeForm(instance=user)       
    return signup_save_form(request, form, template_name, data, user_created=user_created)      

def signup_detail(request,pk):
    template_name = 'signup/detail.html'
    user = User.objects.get(pk=pk)
    data = {        
        'user': user,
        'title': _("Detail Info"),
        'edit': _("Edit"),
        'list_all': _("List All")    
    }
    return render(request, template_name,data)

def signup_delete(request,pk):    
    user = get_object_or_404(User, pk=pk)  
    if not user.date_login:
        if request.method == 'POST':        
            try:
                user.delete()
                messages.success(request, _('Completed successful.'))
                return redirect('signup:url_signup_list')
            except IntegrityError:
                messages.warning(request, _('You cannot delete. This user has an existing related.'))
                return redirect('signup:url_signup_list')    
    else:
        messages.warning(request, _('You cannot delete. This user has already accessed the system. You can inactivate it. '))
        return redirect('signup:url_signup_list')    

def signup_inactive_all(request):       
    context = []    
    if request.method == "POST":        
        context = request.POST["checkbox_selected"].split(",")
        print("valor do context", context)
        messages.success(request, _('Completed successful.'))                  
        context = [int(x) for x in context]      
        if context:                
            b = User.objects.filter(id__in=context).update(is_active=False)
            print("Valor do b",b)

        return redirect('signup:url_signup_list')   
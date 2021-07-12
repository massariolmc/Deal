from django.forms import ModelForm, TextInput, Textarea, NumberInput, DateInput, Select, SelectDateWidget, HiddenInput, DateTimeInput, EmailInput, FileInput, ClearableFileInput, CheckboxInput
from django.forms import BaseModelFormSet, ModelChoiceField, MultipleChoiceField, SelectMultiple,CheckboxSelectMultiple
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Contract, UploadContract
from company.models import Company
from account.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, Row, Column, Button, ButtonHolder, HTML, Hidden, Button
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from hurry.filesize import size, iec, si # converter GB,MB para template
import magic # Mesma coisa que o file no linux, verificar o formato do arquivo
import sys


class ContractForm(ModelForm):   

    class Meta:        
        model = Contract
        fields = ['name','object','type','dt_start','dt_end','dt_renovation', 'pay_day', 'number_months', 'value_month', 'number_contract', 'provider','status', 'dt_conclusion', 'value','description', 'members_contract']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'object': Textarea(attrs={'class': 'form-control'}),
            'type': Select(attrs={'class': 'form-control'}),            
            'dt_start': DateInput(attrs={'class': 'form-control calendario'}),            
            'dt_end': DateInput(attrs={'class': 'form-control calendario'}),
            'dt_renovation': DateInput(attrs={'class': 'form-control calendario'}),
            'pay_day': Select(attrs={'class': 'form-control'}),
            'number_months': TextInput(attrs={'class': 'form-control'}),
            'value_month': TextInput(attrs={'class': 'form-control money'}),
            'number_contract': TextInput(attrs={'class': 'form-control'}),
            'provider': Select(attrs={'class': 'form-control'}),
            'status': Select(attrs={'class': 'form-control'}),
            'dt_conclusion': DateInput(attrs={'class': 'form-control calendario'}),            
            'value': TextInput(attrs={'class': 'form-control money'}),
            #'company': Select(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control'}),                                   
            #'members_contract': SelectMultiple(attrs={'class': 'form-control'}), 
            'members_contract': CheckboxSelectMultiple(attrs={'class': 'form-control'}), 
        }              
        
    #VALIDAÇÃO     
    def clean_name(self):        
        name = self.cleaned_data['name']           
        msg = _("There is a alias for this Contract. Choose other name. ")
        n = False
        if self.instance.id:
            n = Contract.objects.filter(name__iexact=name).exclude(id=self.instance.id).exists()#Verifica se o nome já existe                                  
        
        if n:
            raise ValidationError(msg)

        return name   

    def clean(self):
        cleaned_data = super(ContractForm,self).clean()        
        status = cleaned_data.get('status', None)
        dt_conclusion = cleaned_data.get('dt_conclusion')        
        msg_1 = _(f"Input the date conclusion.")        
        print("Valor do dt conclusion", dt_conclusion)
        if status == 'Encerrado' and dt_conclusion == None:
            self.add_error('dt_conclusion',msg_1)        
        
        return cleaned_data   
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)   
        #self.fields['company'].queryset = Company.objects.filter(status='Ativo')
        self.fields['value'].localize = True
        self.fields['value'].widget.is_localized = True
        self.fields['value_month'].localize = True
        self.fields['value_month'].widget.is_localized = True  
        #self.fields['members_contract'].queryset = Contract.objects.prefetch_related('members_contract').filter(company__status='Ativo').values('company__name').distinct()
        self.fields['members_contract'].queryset = Company.objects.filter(status='Ativo')
        self.helper = FormHelper()
        self.enctype = "multipart/form-data"        
        self.helper.layout = Layout(                                               
            Row(
                Column('name', css_class='form-group col-md-12 mb-0'),             
                css_class='form-row'
            ),
            Row(
                Column('provider', css_class='form-group col-md-3 mb-0'),               
                Column('type', css_class='form-group col-md-3 mb-0'),  
                Column('value', css_class='form-group col-md-3 mb-0'),
                Column('number_contract', css_class='form-group col-md-3 mb-0'),                                
                css_class='form-row'
            ),        
            Row(               
                Column('object', css_class='form-group col-md-12 mb-0'),                
                css_class='form-row'
            ),     
            Row(                                
                Column('dt_start', css_class='form-group col-md-3 mb-0'),  
                Column('dt_end', css_class='form-group col-md-3 mb-0'),
                Column('dt_renovation', css_class='form-group col-md-3 mb-0'),              
                Column('pay_day', css_class='form-group col-md-3 mb-0'),              
                css_class='form-row'
            ),     
                       
            Row(
                Column('value_month', css_class='form-group col-md-3 mb-0'),  
                Column('number_months', css_class='form-group col-md-3 mb-0'), 
                Column('status', css_class='form-group col-md-3 mb-0'),  
                Column('dt_conclusion', css_class='form-group col-md-3 mb-0'),                       
                css_class='form-row'
            ),
            Row(
                Column('members_contract', css_class='form-group col-md-6 mb-0'),   
            ),          
            Row(               
                Column('description', css_class='form-group col-md-12 mb-0'),                
                css_class='form-row'
            ),
            HTML('''
                <hr class="divider" />
                 <div class="row">    
                    <div class="col-sm-6">
                        <span class="float-left">
                            <button type="submit" class="btn btn-primary">{{ save }}</button>  	  
                            <button type="reset" class="btn btn-secondary">{{ clear }}</button>
                        </span>
                    </div>
                    <div class="col-sm-6">
                        <span class="float-right">
                            <a href="{% url 'contract:url_contracts_list'%}" class="btn btn-warning">{{ back }}</a>
                        </span>  
                    </div>
                </div>'''
            ),       
            
            
        )

class UploadContractForm(ModelForm):       
    
    class Meta:        
        model = UploadContract
        fields = ['pdf_contract']
        widgets = {           
            'pdf_contract': ClearableFileInput(attrs={'multiple': True}),                        
        }              
      

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)             
        self.helper = FormHelper()
        self.enctype = "multipart/form-data"
        self.helper.form_tag = False        
        self.helper.layout = Layout(                                               
            Row(
                Column('pdf_contract', css_class='form-group col-md-12 mb-0'),             
                css_class='form-row'
            ),
        )

################### VALIDAÇÃO DO PDF DO CONTRACTA. NÃO FAZ PARTE DE NENHUM FORM. ELE É CHAMADO NA VIEW, NA PARTE DO UPLOAD CONTRACT ############################################
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
################### FIM VALIDATION UPLOAD ###########################################

# class ContractCompanyForm(ModelForm):
#     class Meta:        
#         model = UploadContract
#         fields = ['pdf_contract']
#         widgets = {           
#             'pdf_contract': ClearableFileInput(attrs={'multiple': True}),                        
#         }
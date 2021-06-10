from django.forms import ModelForm, TextInput, Textarea, NumberInput, DateInput, Select, SelectDateWidget, HiddenInput, DateTimeInput, EmailInput, FileInput, CheckboxInput
from django.forms import BaseModelFormSet, ModelChoiceField, MultipleChoiceField, SelectMultiple
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Contract
from account.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, Row, Column, Button, ButtonHolder, HTML, Hidden, Button
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from hurry.filesize import size, iec, si # converter GB,MB para template
import magic # Mesma coisa que o file no linux, verificar o formato do arquivo


class ContractForm(ModelForm):   

    class Meta:        
        model = Contract
        fields = ['name','object','type','dt_start','dt_end','dt_renovation', 'pay_day', 'number_months', 'value_month', 'number_contract', 'provider','status','pdf_contract','value','company','description']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'object': Textarea(attrs={'class': 'form-control'}),
            'type': Select(attrs={'class': 'form-control'}),            
            'dt_start': DateInput(attrs={'class': 'form-control calendario'}),            
            'dt_end': DateInput(attrs={'class': 'form-control calendario'}),
            'dt_renovation': DateInput(attrs={'class': 'form-control calendario'}),
            'pay_day': DateInput(attrs={'class': 'form-control calendario'}),
            'number_months': TextInput(attrs={'class': 'form-control'}),
            'value_month': TextInput(attrs={'class': 'form-control'}),
            'number_contract': TextInput(attrs={'class': 'form-control'}),
            'provider': Select(attrs={'class': 'form-control'}),
            'status': Select(attrs={'class': 'form-control'}),
            'pdf_contract': FileInput(attrs={'class': 'form-control'}),            
            'value': NumberInput(attrs={'class': 'form-control'}),
            'company': Select(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control'}),                                   
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
    
    def clean_pdf_contract(self):        
        pdf_contract = self.cleaned_data['pdf_contract']
        size_max = 3000000
        formats = "PDF"
        msg_size =  _(f"Maximum size allowed {size(size_max, system=si)}")
        msg_format =  _(f"This format not allowed {formats}")
        if pdf_contract:   
            file = magic.from_buffer(pdf_contract.read()) 
            print("valor do file",file)  
            if pdf_contract.size > size_max:
                raise ValidationError(msg_size)
            elif not formats in file: 
                raise ValidationError(msg_format)
        return pdf_contract
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)        
        self.helper = FormHelper()
        self.enctype = "multipart/form-data"
        self.helper.layout = Layout(                                               
            Row(
                Column('name', css_class='form-group col-md-12 mb-0'),             
                css_class='form-row'
            ),
            Row(
                Column('provider', css_class='form-group col-md-3 mb-0'),
                Column('company', css_class='form-group col-md-3 mb-0'),
                Column('status', css_class='form-group col-md-2 mb-0'),
                Column('value', css_class='form-group col-md-2 mb-0'),
                Column('number_contract', css_class='form-group col-md-2 mb-0'),                                
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
                Column('type', css_class='form-group col-md-3 mb-0'),   
                Column('pdf_contract', css_class='form-group col-md-3 mb-0'),                                                                           
                css_class='form-row'
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

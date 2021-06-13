from django.forms import ModelForm, TextInput, Textarea, NumberInput, DateInput, Select, SelectDateWidget, HiddenInput, DateTimeInput, EmailInput, FileInput, CheckboxInput
from django.forms import BaseModelFormSet, ModelChoiceField, MultipleChoiceField, SelectMultiple
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import TaxInvoice
from contract.models import Contract
from account.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, Row, Column, Button, ButtonHolder, HTML, Hidden, Button
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from hurry.filesize import size, iec, si # converter GB,MB para template
import magic # Mesma coisa que o file no linux, verificar o formato do arquivo


class TaxInvoiceForm(ModelForm):   

    class Meta:        
        model = TaxInvoice
        fields = ['contract','dt_issue','number_invoice','ref_month','value','pay_day', 'telecom_data', 'time_start', 'time_end', 'forfeit_satus', 'value_forfeit','description','pdf_invoice']
        widgets = {
            'contract': Select(attrs={'class': 'form-control'}),
            'dt_issue': DateInput(attrs={'class': 'form-control calendario'}),
            'number_invoice': TextInput(attrs={'class': 'form-control'}),            
            'ref_month': DateInput(attrs={'class': 'form-control calendario'}),            
            'value': NumberInput(attrs={'class': 'form-control'}),
            'pay_day': DateInput(attrs={'class': 'form-control calendario'}),
            'telecom_data': DateInput(attrs={'class': 'form-control'}),
            'time_start': TextInput(attrs={'class': 'form-control calendario'}),
            'time_end': TextInput(attrs={'class': 'form-control calendario'}),
            'forfeit_satus': Select(attrs={'class': 'form-control'}),
            'value_forfeit': NumberInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control'}),
            'pdf_invoice': FileInput(attrs={'class': 'form-control'}),                                                        
        }              
        
    #VALIDAÇÃO 
   
    
    def clean_pdf_invoice(self):        
        pdf_contract = self.cleaned_data['pdf_invoice']
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
        self.contract = kwargs.get('contract',None)
        if self.contract:
            del(kwargs['contract'])
        super().__init__(*args, **kwargs) 
        if self.contract:  
            self.fields['contract'].queryset = Contract.objects.filter(pk=self.contract)     
        self.helper = FormHelper()
        self.enctype = "multipart/form-data"
        self.helper.layout = Layout(                                                           
            Row(
                Column('contract', css_class='form-group col-md-2 mb-0'),
                Column('number_invoice', css_class='form-group col-md-2 mb-0'),
                Column('dt_issue', css_class='form-group col-md-2 mb-0'),                
                Column('ref_month', css_class='form-group col-md-2 mb-0'),
                Column('value', css_class='form-group col-md-2 mb-0'),  
                Column('pay_day', css_class='form-group col-md-2 mb-0'),                              
                css_class='form-row'
            ),                       
            Row(                               
                Column('time_start', css_class='form-group col-md-2 mb-0'),
                Column('time_end', css_class='form-group col-md-2 mb-0'),   
                Column('forfeit_satus', css_class='form-group col-md-2 mb-0'),  
                Column('value_forfeit', css_class='form-group col-md-2 mb-0'),           
                Column('pdf_invoice', css_class='form-group col-md-2 mb-0'),             
                css_class='form-row'
            ),            
            Row(
                Column('telecom_data', css_class='form-group col-md-3 mb-0'),                               
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
                            <a href="{% url 'tax_invoice:url_providers_choose'%}" class="btn btn-warning">{{ back }}</a>
                        </span>  
                    </div>
                </div>'''
            ),       
            
            
        )

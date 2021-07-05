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
from datetime import datetime


class TaxInvoiceForm(ModelForm):   
    pdf_invoice = forms.FileField(label=_("Files"), required=True, widget = forms.FileInput(attrs={'multiple': True}))
    class Meta:        
        model = TaxInvoice
        fields = ['contract','company','dt_issue','number_invoice','ref_month','value','pay_day', 'telecom_data', 'time_start', 'time_end', 'forfeit_status', 'value_forfeit','description', 'number_req_nimbi', 'number_cod_nimbi', 'number_pc_nimbi', 'number_cod_project', 'number_cost_center', 'dt_create_rc', 'dt_send_nf_fiscal']
        widgets = {
            'contract': Select(attrs={'class': 'form-control'}),
            'company': Select(attrs={'class': 'form-control'}),
            'dt_issue': DateInput(attrs={'class': 'form-control calendario'}),
            'number_invoice': TextInput(attrs={'class': 'form-control'}),            
            'ref_month': TextInput(attrs={'class': 'form-control ref'}),            
            'value': TextInput(attrs={'class': 'form-control money'}),
            'pay_day': DateInput(attrs={'class': 'form-control calendario'}),
            'telecom_data': DateInput(attrs={'class': 'form-control'}),
            'time_start': TextInput(attrs={'class': 'form-control calendario'}),
            'time_end': TextInput(attrs={'class': 'form-control calendario'}),
            'forfeit_status': Select(attrs={'class': 'form-control'}),
            'value_forfeit': TextInput(attrs={'class': 'form-control money'}),
            'description': Textarea(attrs={'class': 'form-control'}),             
            # Fields Nimbi
            'number_req_nimbi': TextInput(attrs={'class': 'form-control'}),
            'number_cod_nimbi': TextInput(attrs={'class': 'form-control'}),
            'number_pc_nimbi': TextInput(attrs={'class': 'form-control'}),
            'number_cod_project': TextInput(attrs={'class': 'form-control'}),
            'number_cost_center': TextInput(attrs={'class': 'form-control'}),   
            'dt_create_rc': TextInput(attrs={'class': 'form-control calendario'}),
            'dt_send_nf_fiscal': TextInput(attrs={'class': 'form-control calendario'}),                                                   
        }              
        
    #VALIDAÇÃO 
   
    
    # def clean_pdf_invoice(self):        
    #     pdf_contract = self.cleaned_data['pdf_invoice']
    #     size_max = 3000000
    #     formats = "PDF"
    #     msg_size =  _(f"Maximum size allowed {size(size_max, system=si)}")
    #     msg_format =  _(f"This format not allowed {formats}")
    #     if pdf_contract:   
    #         file = magic.from_buffer(pdf_contract.read()) 
    #         print("valor do file",file)  
    #         if pdf_contract.size > size_max:
    #             raise ValidationError(msg_size)
    #         elif not formats in file: 
    #             raise ValidationError(msg_format)
    #     return pdf_contract
    
    def clean_ref_month(self):
        ref_month = self.cleaned_data['ref_month']
        msg_format =  _(f"This format not allowed.")
        try:
            datetime.strptime(ref_month, '%m/%Y')

        except ValueError:
            raise ValidationError(msg_format)
        
        return ref_month

    
    def clean(self):
        cleaned_data = super(TaxInvoiceForm,self).clean()        
        status = cleaned_data.get('forfeit_status', None)
        value = cleaned_data.get('value_forfeit')        
        msg_1 = _(f"The field Forfeit is checked like No.")
        msg_2 = _(f"The field Forfeit is checked like Yes.")
        
        if status == 'No' and value != 0.0:
            self.add_error('value_forfeit',msg_1)
        elif status == 'Yes' and value == 0.0:
            self.add_error('value_forfeit',msg_2)          
        
        return cleaned_data


    def __init__(self, *args, **kwargs):
        self.contract = kwargs.get('contract',None)
        if self.contract:
            del(kwargs['contract'])
        super().__init__(*args, **kwargs) 
        self.fields['value'].localize = True
        self.fields['value'].widget.is_localized = True
        self.fields['value_forfeit'].localize = True
        self.fields['value_forfeit'].widget.is_localized = True
        if self.instance.id:  
            self.fields['contract'].queryset = Contract.objects.filter(pk=self.instance.contract.id)          
            self.fields['company'].queryset = self.instance.contract.members_contract.all()
        else:
            self.fields['contract'].queryset = Contract.objects.filter(pk=self.contract.id)          
            self.fields['company'].queryset = self.contract.members_contract.all()
        self.helper = FormHelper()
        self.enctype = "multipart/form-data"
        self.helper.layout = Layout(                                                           
            Row(
                Column('contract', css_class='form-group col-md-2 mb-0'),
                Column('company', css_class='form-group col-md-2 mb-0'),
                Column('number_invoice', css_class='form-group col-md-2 mb-0'),
                Column('dt_issue', css_class='form-group col-md-1 mb-0'),                
                Column('ref_month', css_class='form-group col-md-1 mb-0'),
                Column('value', css_class='form-group col-md-2 mb-0'),  
                Column('pay_day', css_class='form-group col-md-2 mb-0'),                              
                css_class='form-row'
            ),                       
            Row(                               
                Column('time_start', css_class='form-group col-md-2 mb-0'),
                Column('time_end', css_class='form-group col-md-2 mb-0'),   
                Column('forfeit_status', css_class='form-group col-md-2 mb-0'),  
                Column('value_forfeit', css_class='form-group col-md-2 mb-0'), 
                Column('pdf_invoice', css_class='form-group col-md-4 mb-0'),         
                css_class='form-row'
            ),  
             Row(                               
                Column('number_req_nimbi', css_class='form-group col-md-2 mb-0'),
                Column('number_cod_nimbi', css_class='form-group col-md-1 mb-0'),   
                Column('number_pc_nimbi', css_class='form-group col-md-1 mb-0'),  
                Column('number_cod_project', css_class='form-group col-md-2 mb-0'),           
                Column('number_cost_center', css_class='form-group col-md-2 mb-0'),             
                Column('dt_create_rc', css_class='form-group col-md-2 mb-0'),             
                Column('dt_send_nf_fiscal', css_class='form-group col-md-2 mb-0'),             
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
                            <a href="{% url 'tax_invoice:url_tax_invoices_list' contract.slug %}" class="btn btn-warning">{{ back }}</a>
                        </span>  
                    </div>
                </div>'''
            ),       
            
            
        )

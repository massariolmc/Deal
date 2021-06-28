from django.forms import ModelForm, TextInput, Textarea, NumberInput, DateInput, Select, SelectDateWidget, HiddenInput, DateTimeInput, EmailInput, FileInput, CheckboxInput
from django.forms import BaseModelFormSet, ModelChoiceField, MultipleChoiceField, SelectMultiple
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Annotation
from account.models import User
from contract.models import Contract
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, Row, Column, Button, ButtonHolder, HTML, Hidden, Button
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class AnnotationForm(ModelForm):

    class Meta:
        model = Annotation
        fields = ['name','description','contract']
        widgets = {
            'contract': HiddenInput(attrs={'class': 'form-control'}),
            'name': TextInput(attrs={'class': 'form-control'}),            
            'description': Textarea(attrs={'class': 'form-control'}),            
        }                    
    
    def __init__(self, *args, **kwargs):
        self.contract = kwargs.get('contract',None)
        if self.contract:
            del(kwargs['contract'])
        super().__init__(*args, **kwargs)             
        if self.instance.pk:
            self.contract = self.instance.contract.id                                
        self.helper = FormHelper()
        self.enctype = "multipart/form-data"
        self.helper.layout = Layout(   
            Hidden('contract',self.contract),                                                        
            Row(
                Column('name', css_class='form-group col-md-12 mb-0'),                                                                                      
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
                            <a href="{% url 'annotation:url_annotations_list' contract.slug %}" class="btn btn-warning">{{ back }}</a>
                        </span>  
                    </div>
                </div>'''
            ),       
            
            
        )

from django.forms import ModelForm, TextInput, Textarea, NumberInput, DateInput, Select, SelectDateWidget, HiddenInput, DateTimeInput, EmailInput, FileInput, CheckboxInput
from django.forms import BaseModelFormSet, ModelChoiceField, MultipleChoiceField, SelectMultiple
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import ContactProvider
from account.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, Row, Column, Button, ButtonHolder, HTML, Hidden, Button,Field
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from django.utils.translation import ugettext_lazy as _


class ContactProviderForm(ModelForm):

    class Meta:
        model = ContactProvider
        fields = ['name','phone_1','phone_2','email_1','email_2','description']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),     
            'phone_1': TextInput(attrs={'class': 'form-control'}),            
            'phone_2': TextInput(attrs={'class': 'form-control'}),
            'email_1': EmailInput(attrs={'class': 'form-control'}),
            'email_2': EmailInput(attrs={'class': 'form-control'}),     
            'description': TextInput(attrs={'class': 'form-control'}),            
        }                    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)        
        self.helper = FormHelper()
        self.enctype = "multipart/form-data"
        self.helper.form_tag = False
        self.helper.layout = Layout(                                                           
          'name',
          'phone_1',
          'phone_2',
          'email_1',
          'email_2',
          'description',           
            
        )

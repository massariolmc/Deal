from django.forms import ModelForm, TextInput, Textarea, NumberInput, PasswordInput, DateInput, Select, SelectDateWidget, HiddenInput, DateTimeInput, EmailInput, FileInput, CheckboxInput
from django.forms import BaseModelFormSet, ModelChoiceField, MultipleChoiceField, SelectMultiple
from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from account.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, Row, Column, Button, ButtonHolder, HTML, Hidden, Button


class UserCreationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ("cpf", "first_name", "last_name", "username", "email", "password1", "password2")
        widgets = {
            'cpf': TextInput(attrs={'class': 'form-control'}),
            'first_name': TextInput(attrs={'class': 'form-control'}),
            'last_name': TextInput(attrs={'class': 'form-control'}),
            'username': TextInput(attrs={'class': 'form-control'}),
            'email': EmailInput(attrs={'class': 'form-control'}),    
            'password1': PasswordInput(attrs={'class': 'form-control'}),        
            'password2': PasswordInput(attrs={'class': 'form-control'}),                                               
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)        
        self.helper = FormHelper()
        self.enctype = "multipart/form-data"
        self.helper.layout = Layout(
            'cpf',
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2',            
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
                            <a href="{% url 'signup:url_signup_list'%}" class="btn btn-warning">{{ back }}</a>
                        </span>  
                    </div>
                </div>'''
            ),       
            
            
        )    

class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("cpf", "first_name", "last_name", "username", "email", "is_active")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)        
        self.helper = FormHelper()
        self.enctype = "multipart/form-data"
        self.helper.layout = Layout(
            'cpf',
            'first_name',
            'last_name',
            'username',
            'email',            
            'is_active',
                        
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
                            <a href="{% url 'signup:url_signup_list'%}" class="btn btn-warning">{{ back }}</a>
                        </span>  
                    </div>
                </div>'''
            ),       
            
            
        )    

    # def save(self, commit=True):
    #     user = super(UserCreationForm, self).save(commit=False)
    #     user.email = self.cleaned_data["email"]
    #     if commit:
    #         user.save()
    #     return user
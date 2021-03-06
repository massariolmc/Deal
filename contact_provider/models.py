from django.db import models
from account.models import User
from django.utils.translation import ugettext_lazy as _
from contract.models import Contract
from .slug_file import unique_uuid


class ContactProvider(models.Model):
    name = models.CharField(_('Name'), max_length=100, blank=False, null=False)    
    slug = models.SlugField(_('Slug'), max_length=200, unique=True, blank=True)    
    contract = models.ForeignKey(Contract, verbose_name=_("Contract"), default=1, on_delete=models.CASCADE, blank=False, null=False)
    description = models.TextField(_('Description'), blank=True)   
    phone_1 = models.CharField(_("Main Phone"), max_length=20, blank=True)
    phone_2 = models.CharField(_("Secundary Phone"), max_length=20, blank=True) 
    email_1 = models.EmailField(_('Main Email'), max_length=100, blank=True)
    email_2 = models.EmailField(_('Secundary Email'), max_length=100, blank=True)        
    user_created = models.ForeignKey(User, related_name="contact_provider_user_created_id", verbose_name=_("Created by"), blank=True, on_delete=models.PROTECT)
    user_updated = models.ForeignKey(User, related_name="contact_provider_user_updated_id", verbose_name=_("Updated by"), blank=True, on_delete=models.PROTECT)
    created_at = models.DateTimeField(_('Created at'),auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    class Meta:
        verbose_name = _("ContactProvider")
        verbose_name_plural = _("ContactProviders")
        ordering = ["name"]   

    def save(self, *args, **kwargs):                
        #Insere um valor para o Slug            
        self.slug = unique_uuid(self.__class__)             
        super().save(*args, **kwargs)    
    
    def __str__(self):
        return self.name

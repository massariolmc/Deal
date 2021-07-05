from django.db import models
from account.models import User
from contract.models import Contract
from django.utils.translation import ugettext_lazy as _
from .slug_file import unique_uuid
from ckeditor.fields import RichTextField 


class Annotation(models.Model):
    contract = models.ForeignKey(Contract, related_name="annotation_contract_created_id", verbose_name=_("Contract"), blank=False, on_delete=models.CASCADE)
    name = models.CharField(_('Name'), max_length=100, unique=True, blank=False, null=False)    
    slug = models.SlugField(_('Slug'), max_length=200, unique=True, blank=True)                    
    description = RichTextField(_('Description'), blank=True)            
    user_created = models.ForeignKey(User, related_name="annotation_user_created_id", verbose_name=_("Created by"), blank=True, on_delete=models.PROTECT)
    user_updated = models.ForeignKey(User, related_name="annotation_user_updated_id", verbose_name=_("Updated by"), blank=True, on_delete=models.PROTECT)
    created_at = models.DateTimeField(_('Created at'),auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    class Meta:
        verbose_name = _("Annotation")
        verbose_name_plural = _("Annotations")
        ordering = ["name"]   

    def save(self, *args, **kwargs):                
        #Insere um valor para o Slug            
        self.slug = unique_uuid(self.__class__)             
        super().save(*args, **kwargs)    
    
    def __str__(self):
        return self.name
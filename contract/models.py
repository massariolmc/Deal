from django.db import models
from account.models import User
from service_type.models import ServiceType
from provider.models import Provider
from company.models import Company
from status.models import Status
from django.utils.translation import ugettext_lazy as _
from .compress_image import compress, delete_old_image, delete_old_file
from .slug_file import unique_uuid

class Contract(models.Model):
    name = models.CharField(_('Name'), max_length=100, unique=True, blank=False, null=False)
    object = models.TextField(_('Object'), blank=False, null=False)
    slug = models.SlugField(_('Slug'), max_length=200, unique=True, blank=True)
    type = models.ForeignKey(ServiceType, related_name="contract_type_created_id", verbose_name=_("Type"), blank=False, on_delete=models.PROTECT)
    dt_start = models.DateField(_('Date Initial'), max_length=100, blank=True)
    dt_end = models.DateField(_('Date End'), max_length=100, blank=True)
    dt_renovation = models.DateField(_('Date Renovation'), max_length=100, blank=True)
    pay_day = models.DateField(_('Payment Day'), default = '1950-01-01' , max_length=100, blank=True)
    number_months = models.PositiveIntegerField(_('Number of Months'), default = 0 , blank=True)
    value_month = models.DecimalField(_('Value Month'), default = 0, decimal_places=2, max_digits=12, blank=True)
    number_contract = models.CharField(_('Number Contract'), max_length=100, blank=True)    
    provider = models.ForeignKey(Provider, related_name="contract_provider_created_id", verbose_name=_("Provider"), blank=False, on_delete=models.PROTECT)
    status = models.ForeignKey(Status, related_name="contract_status_created_id", verbose_name=_("Status"), blank=False, on_delete=models.PROTECT)
    pdf_contract = models.FileField(upload_to = 'contract/', verbose_name =_('File'), blank=True, max_length=200)
    value = models.DecimalField(_('Contract Value'), decimal_places=2, max_digits=12, blank=False)
    company = models.ForeignKey(Company, related_name="contract_company_created_id", verbose_name=_("Company"), blank=False, on_delete=models.PROTECT)
    description = models.TextField(_('Description'), blank=True)        
    user_created = models.ForeignKey(User, related_name="contract_user_created_id", verbose_name=_("Created by"), blank=True, on_delete=models.PROTECT)
    user_updated = models.ForeignKey(User, related_name="contract_user_updated_id", verbose_name=_("Updated by"), blank=True, on_delete=models.PROTECT)
    created_at = models.DateTimeField(_('Created at'),auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    class Meta:
        verbose_name = _("Contract")
        verbose_name_plural = _("Contracts")
        ordering = ["name"]   

    def save(self, *args, **kwargs):        
        marc = 0
        if self.id:            
            #Deleta a imagem antiga, caso não for igual
            marc = delete_old_file(self.__class__, self.id, self.pdf_contract)            
        else:
            #Insere um valor para o Slug            
            self.slug = unique_uuid(self.__class__)                
        
        # save
        super().save(*args, **kwargs)

    # Sobreescreve este metodo para delete imagens. Sem a imagem continua em media, mesmo deletando a pessoa do banco
    def delete(self, *args, **kwargs):
        self.pdf_contract.delete(save=False)# Se deixar save=True ele deleta o arquivo e chama o metodo save automaticamente e ai isso gerar erro.
        super().delete(*args, **kwargs)
    
    def __str__(self):
        return self.name
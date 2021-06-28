from django.db import models
from account.models import User
from service_type.models import ServiceType
from provider.models import Provider
from company.models import Company
from status.models import Status
from django.utils.translation import ugettext_lazy as _
from .compress_image import compress, delete_old_image, delete_old_file
from .slug_file import unique_uuid
from ckeditor.fields import RichTextField 

class Contract(models.Model):
    days = (
        ("1", "1"),("2", "2"),("3", "3"),("4", "4"),("5", "5"),("6", "6"),("7", "7"),("8", "8"),("9", "9"),("10", "10"),("11", "11"),("12", "12"),
        ("13", "13"),("14", "14"),("14", "14"),("15", "15"),("16", "16"),("17", "17"),("18", "18"),("19", "19"),("20", "20"),("21", "21"),("22", "22"),
        ("23", "23"),("24", "24"),("25", "25"),("26", "26"),("27", "27"),("28", "28"),("29", "29"),("30", "30"),("31", "31"),        
    )
    select_status = (
        ('Ativo','Ativo'),
        ('Encerrado','Encerrado'),
    )
    name = models.CharField(_('Name'), max_length=100, unique=True, blank=False, null=False)
    #object = models.TextField(_('Object'), blank=False, null=False)
    object = RichTextField(_('Object'), blank=False, null=False)
    slug = models.SlugField(_('Slug'), max_length=200, unique=True, blank=True)
    type = models.ForeignKey(ServiceType, related_name="contract_type_created_id", verbose_name=_("Type"), blank=False, on_delete=models.PROTECT)
    dt_start = models.DateField(_('Date Initial'), max_length=100, blank=True)
    dt_end = models.DateField(_('Date End'), max_length=100, blank=True)
    dt_renovation = models.DateField(_('Date Renovation'), max_length=100, blank=True)    
    pay_day = models.CharField(_('Payment Day'),max_length=100, choices = days,blank=True, null=True)
    number_months = models.PositiveIntegerField(_('Number of Months'), default = 0 , blank=True)
    value_month = models.DecimalField(_('Value Month'), default = 0, decimal_places=2, max_digits=20, blank=True)
    number_contract = models.CharField(_('Number Contract'), max_length=100, blank=True)    
    provider = models.ForeignKey(Provider, related_name="contract_provider_created_id", verbose_name=_("Provider"), blank=False, on_delete=models.PROTECT)
    status = models.CharField(_('Status'), max_length=100, choices = select_status, default="Ativo",blank=False)    
    dt_conclusion =  models.DateField(_('Date End'), max_length=100, blank=True, null=True)    
    value = models.DecimalField(_('Contract Value'), decimal_places=2, max_digits=20, blank=False)
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
        #Insere um valor para o Slug            
        self.slug = unique_uuid(self.__class__)             
        super().save(*args, **kwargs)    
    
    def __str__(self):
        return f"{self.provider.name} - {self.name}"


class UploadContract(models.Model):
    contract = models.ForeignKey(Contract, related_name="upload_contract_contract_created_id", verbose_name=_("Contract"), blank=True, on_delete=models.PROTECT)
    pdf_contract = models.FileField(upload_to = 'upload_contract/', verbose_name =_('File'), blank=True, max_length=200)
    slug = models.SlugField(_('Slug'), max_length=200, unique=True, blank=True)
    user_created = models.ForeignKey(User, related_name="upload_contract_user_created_id", verbose_name=_("Created by"), blank=True, on_delete=models.PROTECT)
    user_updated = models.ForeignKey(User, related_name="upload_contract_user_updated_id", verbose_name=_("Updated by"), blank=True, on_delete=models.PROTECT)
    created_at = models.DateTimeField(_('Created at'),auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    class Meta:
        verbose_name = _("Upload Contract")
        verbose_name_plural = _("Upload Contracts")
        ordering = ["updated_at"]   

    def save(self, *args, **kwargs):                
        #Insere um valor para o Slug            
        self.slug = unique_uuid(self.__class__)             
        super().save(*args, **kwargs)

    # Sobreescreve este metodo para delete imagens. Sem a imagem continua em media, mesmo deletando a pessoa do banco
    def delete(self, *args, **kwargs):
        self.pdf_contract.delete(save=False)# Se deixar save=True ele deleta o arquivo e chama o metodo save automaticamente e ai isso gerar erro.
        super().delete(*args, **kwargs)
    
    def __str__(self):
        return f"{self.contract}"
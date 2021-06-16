from django.db import models
from account.models import User
from contract.models import Contract
from status.models import Status
from django.utils.translation import ugettext_lazy as _
from .compress_image import compress, delete_old_image, delete_old_file
from .slug_file import unique_uuid

class TaxInvoice(models.Model):

    yes_or_no = (
        ('Yes', _('Yes')), 
        ('No', _('No')),
    )

    contract = models.ForeignKey(Contract, related_name="tax_invoice_contract_created_id", verbose_name=_("Contract"), blank=False, on_delete=models.PROTECT)
    slug = models.SlugField(_('Slug'), max_length=200, unique=True, blank=True)
    dt_issue = models.DateField(_('Issue Date'), max_length=100, blank=True, null=True)
    number_invoice = models.CharField(_('Number Invoice'), max_length=100, blank=False)    
    ref_month = models.DateField(_('Reference Month'), max_length=100, blank=False)
    value = models.DecimalField(_('Invoice Value'), decimal_places=2, max_digits=20, blank=False)
    pay_day = models.DateField(_('Payment Day'),max_length=100, blank=True, null=True)
    telecom_data = models.CharField(_('Telecom Data'), max_length=100, blank=True)
    time_start = models.DateField(_('Time Start'), max_length=100, blank=True, null=True)
    time_end = models.DateField(_('Time End'), max_length=100, blank=True, null=True)
    forfeit_satus = models.CharField(_('Forfeit Status'), max_length=100, choices = yes_or_no, blank=True, null=True)
    value_forfeit = models.DecimalField(_('Value Forfeit'), decimal_places=2, max_digits=20, default = "0,00", blank=True, null=True)    
    description = models.TextField(_('Description'), blank=True)        
    pdf_invoice = models.FileField(upload_to = 'tax_invoice/', verbose_name =_('File'), blank=True, max_length=200)
    user_created = models.ForeignKey(User, related_name="tax_invoice_user_created_id", verbose_name=_("Created by"), blank=True, on_delete=models.PROTECT)
    user_updated = models.ForeignKey(User, related_name="tax_invoice_user_updated_id", verbose_name=_("Updated by"), blank=True, on_delete=models.PROTECT)
    created_at = models.DateTimeField(_('Created at'),auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)  
    
    class Meta:
        verbose_name = _("Tax Invoice")
        verbose_name_plural = _("Tax Invoices")
        ordering = ["created_at"]   

    def save(self, *args, **kwargs):        
        marc = 0
        if self.id:            
            #Deleta a imagem antiga, caso não for igual
            marc = delete_old_file(self.__class__, self.id, self.pdf_invoice)            
        else:
            #Insere um valor para o Slug            
            self.slug = unique_uuid(self.__class__)                
        
        # save
        super().save(*args, **kwargs)

    # Sobreescreve este metodo para delete imagens. Sem a imagem continua em media, mesmo deletando a pessoa do banco
    def delete(self, *args, **kwargs):
        self.pdf_invoice.delete(save=False)# Se deixar save=True ele deleta o arquivo e chama o metodo save automaticamente e ai isso gerar erro.
        super().delete(*args, **kwargs)
    
    def __str__(self):
        return f"{self.contract.name} - {self.ref_month}"
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Contratos.settings")
django.setup()
from contract.models import CostCenter
from contract.slug_file import unique_uuid
from account.models import User
from datetime import datetime

#Carregar informações do Centro de Custo
class CostCenterClass:

    def inserir():        
        aux = []
        aux2 = []
        #arq = open('/home/massariol/Documentos/HD_EXT/APPS/Apps_Python/DJANGO/VetorialContratos/cost_center.csv','r')
        arq = open('/home/mlx/Projects/Contracts/cost_center.csv','r')
        for read in arq.readlines():            
            aux = read.strip("\n").split("\t")             
            if aux:# Se a lista for verdadeira, ou seja, tenha valores na lista           
                print(aux)
                data = dict(                
                    cod    = aux[0],                
                    name      = aux[1],
                    branch    = aux[2],                                    
                    plant =   aux[3],          
                    slug = unique_uuid(CostCenter),
                    user_created = User.objects.get(pk=1), 
                    user_updated = User.objects.get(pk=1),                
                )   
                obj = CostCenter(**data)            
                aux2.append(obj)        
        CostCenter.objects.bulk_create(aux2)

CostCenterClass.inserir()



from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from account.forms import UserCustomCreateForm
from account.models import User
import pandas as pd
import os
import sys
from datetime import datetime, timedelta
import locale

@login_required
def home(request):
    template_name = "core/base.html"    
    return render(request,template_name,{})

def signup(request):
    template_name = 'registration/signup.html'
    if request.method == 'POST':
        form = UserCustomCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserCustomCreateForm()
       
    return render(request, template_name ,{'form': form})


# Essa parte foi desenvolvida para ler o arquivo xlsx do financeiro. Não deverá mais ser usada.
def rel(request):
    template_name = 'core/rel.html' 
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')       
    arq = os.path.join(os.getcwd(),'core/arq/AnaliseDados.xls')
    df = pd.read_excel(arq, sheet_name='Dados')
    #print("pandas",df.head())  

    detail = ""
    if request.method == "POST":
        detail = request.POST["account"]

    data_1 = df.groupby("Nome do PN").agg({'Montante Pago / Recebido': ['sum','mean', 'min', 'max']}).reset_index()        
    nome_fornecedores = data_1["Nome do PN"]
    data_1.loc[:,'QTDE'] = df.groupby("Nome do PN").size().values.tolist()    
    data_1 = data_1[["Nome do PN", "Montante Pago / Recebido", "QTDE"]].values.tolist()
    data_1 = [[f,locale.currency(t, grouping=True),locale.currency(me, grouping=True),locale.currency(men, grouping=True),locale.currency(mai, grouping=True),qtde] for f,t,me,men,mai,qtde in data_1]
    total_pago_fornecedores = locale.currency(df["Montante Pago / Recebido"].sum(), grouping=True)
    if detail:
        filtro = df["Nome do PN"]== detail
        print(df.loc[filtro,["Nome do PN","Lançamento","Vencimento","Observação","Montante Pago / Recebido","Filial"]])
        detail = df.loc[filtro,["Nome do PN","Lançamento","Vencimento","Observação","Montante Pago / Recebido","Filial"]].values.tolist()        
    
    juros = ""
    filtro = df["Observação"] == "JUROS POR ATRASO"
    juros = df.loc[filtro,["Nome do PN","Montante Pago / Recebido"]]
    juros = juros.groupby("Nome do PN")["Montante Pago / Recebido"].sum().reset_index()
    juros = juros[["Nome do PN","Montante Pago / Recebido"]].values.tolist()
    juros = [[fornecedor,locale.currency(valor, grouping=True)] for fornecedor,valor in juros]   
    #print("juros",juros[["Nome do PN","Montante Pago / Recebido"]].values.tolist())
    

    #Fazem a mesma coisa, de formas diferentes -- Quantidade de pagamentos por CNPJ da Vetorial
    #print(df.groupby("Filial").agg({'Montante Pago / Recebido': ['sum','mean', 'min', 'max']}))
    #print(df.groupby("Filial")["Montante Pago / Recebido"].sum())

    data_2 = df.groupby("Filial")["Montante Pago / Recebido"].sum().reset_index()
    data_2.loc[:,'QTDE'] = df.groupby("Filial").size().values.tolist() 
    data_2 = data_2[["Filial", "Montante Pago / Recebido", "QTDE"]].values.tolist()
    data_2 = [[filial,locale.currency(valor, grouping=True),qtde] for filial,valor,qtde in data_2]   

    data = {
        'data_1': data_1,
        'nome_fornecedores': nome_fornecedores,
        'detail': detail,
        'juros': juros,
        'total_pago_fornecedores': total_pago_fornecedores,
        'data_2': data_2,        
    }
    return render(request,template_name,data)

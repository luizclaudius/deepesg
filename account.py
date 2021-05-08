import pandas
import sqlite3
import os
import random

localDir=os.path.join(os.path.dirname(__file__))
account_dict={}
accounts_filename='chart_of_accounts.xlsx'

#Conexão com BD
def dbConnect():
    conn=None
    try:
        conn = sqlite3.connect(os.path.join(localDir,'db.sqlite'))        
        founddb=True
        return conn
    except sqlite3.Error as e:
        return {'status':'erro','descricao':e}     
    
#Realiza contabilização de dados de BD
def sumFromDb(teste=False):
    try:       
        conn=dbConnect()
        if not teste:
            sql="select account,value from general_ledger"
        else:
            sql="select account,value from teste"
        cursor=conn.execute(sql)
        results=cursor.fetchall()
        
        for i in range(len(results)):
            array_account_split=results[i][0].split('.')        
            key=''
            for j in range(len(array_account_split)):
                key=key+array_account_split[j]            
                account_dict[key]=round(account_dict[key]+float(results[i][1].replace(',','.')),2)                
                if j<len(array_account_split)-1:
                    key=key+'.'
        return {'status':'sucesso','descricao':account_dict}
    except sqlite3.Error as e:
        return {'status':'erro','descricao':e}

#Realiza contabilização de arquivo em Excel
def sumFromExcel(filename):
    try:        
        general_ledger = pandas.read_excel(os.path.join(localDir,filename))
        for i in range(len(general_ledger['account'].values)):
            array_account_split=general_ledger['account'][i].split('.')        
            key=''
            for j in range(len(array_account_split)):
                key=key+array_account_split[j]            
                account_dict[key]=round(account_dict[key]+general_ledger['value'][i],2)            
                if j<len(array_account_split)-1:
                    key=key+'.'
        return {'status':'sucesso','descricao':account_dict}
    except os.error as e:        
        return {'status':'erro','descricao':'Arquivo não encontrado'}   

#Inicializa contas com valor 0
def initAccounts():
    accounts=getChartOfAccounts()
    for i in range(len(accounts)):        
        account_dict[accounts[i]]=0

#Retorna lista de contas
def getChartOfAccounts():
    chart_of_acounts = pandas.read_excel(os.path.join(localDir,accounts_filename))
    accounts = chart_of_acounts['account'].values
    return accounts

#Zera a tabela de teste e inicializa com contas e valores aleatórios
def prepareTest():
    conn=dbConnect()   
    sql="DELETE from 'teste';"
    conn.execute(sql)
    conn.commit()
    accounts=getChartOfAccounts()
    
    sql=''
    for i in range(1000):
        random_account=random.randint(0, len(accounts)-1)
        random_value=random.randint(0, 1000000)/100 
        sql+="INSERT INTO 'teste' (account,value) values ('"+accounts[random_account]+"','"+str(random_value).replace(".",",")+"');"

    conn.executescript(sql)
    conn.commit()


#Função principal
def main():
    initAccounts()
    print(sumFromExcel('general_ledger.xlsx'))
    initAccounts()
    print(sumFromDb())
    initAccounts()
    prepareTest()    
    print(sumFromDb(True))

#Início
main()
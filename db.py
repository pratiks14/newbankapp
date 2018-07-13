from db import dbase
import random

class Generator():

    @staticmethod
    def generateBugIndex(no_of_bugs,max_bugs,bug_list):
        if no_of_bugs> max_bugs:
            no_of_bugs = max_bugs
        bugs_created = 0     
        while bugs_created < no_of_bugs:
            randindex = random.randint(0,max_bugs-1)
            if bug_list[randindex] == False:
                bug_list[randindex] = True
                bugs_created +=1
        return bug_list

    @staticmethod   
    def generateCustomerid():
        db = dbase.getDB()
        cursor = db.cursor()
        sql = 'select * from netbankusers where customerid = {customerid}'
        while True:
            customerid =  str(random.randint(10**(7-1),10**7-1))
            sql_exe = sql.format(customerid = customerid)
            cursor.execute(sql_exe)
            account = cursor.fetchone()
            if account is None:
                return customerid	

    @staticmethod
    def calculateRewardPoints(amount):
        if amount > 10000:
            points = random.randint(1,100)
        else:
            points = random.randint(1,50)
        return points    


    @staticmethod
    def generateAccountNumber():
        db = dbase.getDB()
        cursor = db.cursor()
        sql = 'select * from accountdetails where accountno = {accountno}'
        while True:
            accountno =  str(random.randint(10**(16-1),10**16-1))
            sql_exe = sql.format(accountno=accountno)
            cursor.execute(sql_exe)
            account = cursor.fetchone()
            if account is None:
                return accountno

    @staticmethod
    def generateDebitCard():
        db = dbase.getDB()
        cursor = db.cursor()
        sql = 'select * from accountdetails where debitcardno = {cardno}'
        while True:
            cardno =  str(random.randint(10**(16-1),10**16-1))
            sql_exe = sql.format(cardno=cardno)
            cursor.execute(sql_exe)
            account = cursor.fetchone()
            if account is None:
                return cardno  


    @staticmethod
    def generateDepositNumber():
        db = dbase.getDB()
        cursor = db.cursor()
        sql = 'select * from depositdetails where depositno = {depositno}'
        while True:
            depositno = str(random.randint(10**(10-1),10**10-1))
            sql_exe = sql.format(depositno = depositno)
            cursor.execute(sql_exe)
            account = cursor.fetchone()
            if account is None:
                return depositno

import json
# import pyodbc
import time
import sqlite3
from flask import session as login_session
import logging
from logging.handlers import RotatingFileHandler

class dbase():
    __dbname = ''
    @staticmethod
    def initDB(dbname):
        dbase.__dbname = dbname
        db = sqlite3.connect(dbase.__dbname)
        cursor = db.cursor()
        try:
            cursor.execute('''
            create table netbankusers(
        customerid char(7) primary key,
        emailid varchar(50) not null,
        mobileno char(10) not null,
        name varchar(25) not null,
        password varchar(25) not null,
        login_time datetime,
        reward_points int default 0
        )
            ''')
            cursor.execute('''
            create table accountdetails(
        accountno char(16) primary key,
        customerid char(7) references netbankusers(customerid) on delete cascade,
        acc_balance decimal(20,2) default 10000.0 ,
        acc_type varchar(15),
        mail_address varchar(250),
        branch_name varchar(25) not null,
        branch_code varchar(10) ,
        created_date datetime  ,
        debitcardno char(16),
        aadhar_no char(12),
        status varchar(20) default 'Applied' ,
        debit_pin char(4) default '0000'
        )   
            ''')
            cursor.execute('''
            create table depositdetails(
        depositno char(10) primary key,
        customerid char(7) references netbankusers(customerid),
        deposit_amount decimal(20,2),
        debit_acc char(16) references accountdetails(accountno) on delete cascade,
        recur_months  char(2),
        day_of_month char(2),
        created_on datetime
        )
            ''')
            cursor.execute('''
            create table transactions(
        tranxid int identity(1,1) primary key,
        from_account char(16) references accountdetails(accountno),
        to_account char(16) references accountdetails(accountno),
        amount decimal(20,2),
        checked varchar(3) default 'no',
        date datetime2
        )    
            ''')
            db.commit()     

        except Exception as e:
            db.rollback()
            raise e
        
        return 'created'

    @staticmethod
    def createNewDB():
        db = sqlite3.connect(login_session['remote_user'])
        cursor = db.cursor()
        try:
            cursor.execute('delete from transactions;')
            cursor.execute('delete from depositdetails;')
            cursor.execute('delete from accountdetails;')
            cursor.execute('delete from netbankusers;')
            db.commit()
        except Exception as e:
            db.rollback()
            raise e

    @staticmethod
    def test():
        return login_session['remote_user']
    @staticmethod
    def getDB():
        # filename = 'dbconfig.json'
        # with open(filename, 'r') as f:
        #     dbdata = json.load(f)
        # return pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+dbdata['server']+';DATABASE='+dbdata['database']+';UID='+dbdata['username']+';PWD='+ dbdata['password'])
        return sqlite3.connect(login_session['remote_user']) 
    @staticmethod
    def getAccounts(customerid):
        db = dbase.getDB()
        cursor = db.cursor()
        sql = "select * from accountdetails where customerid ='%s' and status in ('Live','Applied') and acc_type IN ('SAVINGS','CURRENT')"%(customerid)
        cursor.execute(sql)
        
        accounts = cursor.fetchall()
        return accounts

    @staticmethod
    def getLiveAccounts(customerid):
        db = dbase.getDB()
        cursor = db.cursor()
        sql = "select * from accountdetails where customerid ='%s' and status ='Live' and acc_type IN ('SAVINGS','CURRENT')"%(customerid)
        cursor.execute(sql)
        
        accounts = cursor.fetchall()
        return accounts

    @staticmethod
    def getAppliedAccounts():
        db = dbase.getDB()
        cursor = db.cursor()
        sql = "select * from accountdetails where status = 'Applied'"
        cursor.execute(sql)
        accounts = cursor.fetchall()
        return accounts


    @staticmethod
    def acceptAccCreation(accountno):
        db = dbase.getDB()
        cursor = db.cursor()
        sql = "update accountdetails set status = 'Live' where accountno = '%s'"%(accountno)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            print("db error occured")
            raise Exception("DB error occured!!")

    @staticmethod
    def rejectAccCreation(accountno):
        db = dbase.getDB()
        cursor = db.cursor()
        sql = "update accountdetails set status = 'Rejected' where accountno = '%s'"%(accountno)
        try:
            cursor.execute(sql)
            db.commit()
        except Exception as e:
            
            print(e)
            db.rollback()
            raise Exception("DB error occured!!")

    @staticmethod
    def getRejectedAccounts(customerid):
        db = dbase.getDB()
        cursor = db.cursor()
        sql = "select * from accountdetails where customerid = '%s'and status='Rejected'"%(customerid)
        
        cursor.execute(sql)
        accounts = cursor.fetchall()
        return accounts

    @staticmethod
    def deleteRejectedAccounts(customerid):
        db = dbase.getDB()
        cursor = db.cursor()
        sql = "delete from accountdetails where customerid = '%s' and status ='Rejected'"%(customerid)
        try:
            cursor.execute(sql)
            db.commit()
        except Exception as e:
            
            print(e)
            db.rollback()


    @staticmethod
    def getAccountBalance(accountno):
        db = dbase.getDB()
        cursor = db.cursor()
        sql = "select acc_balance from accountdetails where accountno = '%s'"%(accountno)
        
        cursor.execute(sql)
        amount = cursor.fetchone()[0]
        return amount

    # @staticmethod
    # def createDebitAccount(customerid,params):
    #     db = dbase.getDB()
    #     cursor = db.cursor()
    #     depositno = Generator.generateDepositNumber()
    #     sql = """insert into depostdetails(depositno,customerid,deposit_amount,debit_acc,recur_months,day_of_month) values
    #     ('%s','%s','%.2f','%s','%s','%s')
    #             """%(depositno,customerid,params['amount'],params['depositperiod'],params['deductiondate'])
    #     try:
    #         cursor.execute(sql)
    #         db.commit()
    #     except Exception as e:
    #         db.rollback()
    #         raise e



    @staticmethod
    def debitAmountFromAccount(accountno,amount):
        db = dbase.getDB()
        cursor = db.cursor()
        sql = "update accountdetails set acc_balance =acc_balance - %.2f where accountno = '%s'"%(amount,accountno)
        cursor.execute(sql)
        db.commit()

    @staticmethod
    def getDepositAccounts(customerid):
        db = dbase.getDB()
        cursor = db.cursor()
        sql = "select * from depositdetails where customerid = '%s'"%(customerid)
        
        cursor.execute(sql)
        accounts = cursor.fetchall()
        return accounts

    @staticmethod
    def getAccountDetails(accountno):
        db = dbase.getDB()
        cursor = db.cursor()
        sql = "select * from accountdetails where accountno = '%s'"%(accountno)
        
        cursor.execute(sql)
        account = cursor.fetchone()
        return account

    @staticmethod
    def deleteAccount(accountno):
        db = dbase.getDB()
        cursor = db.cursor()
        sql = "delete from accountdetails where accountno = '%s'"%(accountno)
        try:
            cursor.execute(sql)
            db.commit()
        except Exception as e:
            db.rollback()
            raise e


    @staticmethod
    def updateAccountDetails(accountno,accounttype,aadharno):
        db = dbase.getDB()
        cursor = db.cursor()
        sql = "update accountdetails set acc_type = '%s' , aadhar_no = '%s' where accountno = '%s'"%(accounttype,aadharno,accountno)
        try:
            cursor.execute(sql)
            db.commit()
        except Exception as e:
            db.rollback()
            raise e

    @staticmethod
    def getDebitCards(customerid):
        db = dbase.getDB()
        cursor = db.cursor()
        sql = "select debitcardno,acc_balance,debit_pin from accountdetails where customerid = '%s' and status = 'Live'"%(customerid)
        cursor.execute(sql)
        cards = cursor.fetchall()
        return cards

    @staticmethod
    def updateDebitPin(cardno,pin):
        db = dbase.getDB()
        cursor = db.cursor()
        sql = "update accountdetails set debit_pin ='%s' where debitcardno = '%s'"%(pin,cardno)
        try:
            cursor.execute(sql)
            db.commit()
        except Exception as e:
            print(e)
            db.rollback()
            raise(e)

    @staticmethod
    def performAccountTransfer(fromaccount,toaccount,amount):
        db = dbase.getDB()
        cursor = db.cursor()
        try:
            sql = "update accountdetails set acc_balance = acc_balance - %.2f where accountno = '%s'"%(amount,fromaccount)
            cursor.execute(sql)
            sql = "update accountdetails set acc_balance = acc_balance + %.2f where accountno = '%s'"%(amount,toaccount)
            cursor.execute(sql)
            sql = "insert into transactions(from_account,to_account,amount,date) values('%s','%s','%.2f','%s')"%(fromaccount,toaccount,amount,time.strftime('%Y-%m-%d %H:%M:%S'))
            cursor.execute(sql)
            db.commit()
        except Exception as e:
            db.rollback()
            raise(e)

    @staticmethod
    def getCreditTranx(customerid):
        db = dbase.getDB()
        cursor = db.cursor()
        
        sql ="""select  from_account,to_account,amount 
            from accountdetails a
            inner join transactions t
            on a.accountno = t.to_account
            where a.customerid = '%s'
            and checked = 'no'
            """%(customerid)
        try:
            cursor.execute(sql)
            tranx = cursor.fetchall()
            sql = """
            update transactions
            set checked = 'yes'
            where exists(
            select *
            from accountdetails a
            where transactions.to_account
            and a.customerid = '%s'
            and transactions.checked = 'no'
            )
            """%(customerid)
            cursor.execute(sql)

            db.commit()
        except Exception as e:
            db.rollback()
            raise e
        return tranx        

    @staticmethod
    def addRewardPoints(points,customerid):
        db = dbase.getDB()
        cursor = db.cursor()
        sql = "update netbankusers set reward_points = reward_points + %d where customerid = '%s'"%(points,customerid)
        try:
            cursor.execute(sql)
            db.commit()
        except Exception as e:
            db.rollback()
            raise e


    @staticmethod
    def updateRewardPoints(amount,accountno,customerid,bugs):
        db = dbase.getDB()
        cursor = db.cursor()
        sql ="update accountdetails set acc_balance = acc_balance + %.2f where accountno = '%s'"%(amount,accountno)
        sql2 = "update netbankusers set reward_points = 0 where customerid = '%s'"%(customerid)
        try:
            if not bugs:
                cursor.execute(sql)
            cursor.execute(sql2)
            db.commit()
        except Exception as e:
            db.rollback()
            raise e  

    @staticmethod
    def getCreditTransaction(accountno):
        db = dbase.getDB()
        cursor = db.cursor()
        sql = "select * from transactions where to_account = '%s'"%(accountno)
        cursor.execute(sql)
        tranx = cursor.fetchall()
        return tranx
    
    @staticmethod
    def getDebitTransaction(accountno):
        db = dbase.getDB()
        cursor = db.cursor()
        sql = "select * from transactions where from_account = '%s'"%(accountno)
        cursor.execute(sql)
        tranx = cursor.fetchall()
        return tranx

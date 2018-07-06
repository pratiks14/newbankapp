
import json
import pyodbc



class dbase():
    @staticmethod
    def getDB():
        filename = 'dbconfig.json'
        with open(filename, 'r') as f:
            dbdata = json.load(f)
        return pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+dbdata['server']+';DATABASE='+dbdata['database']+';UID='+dbdata['username']+';PWD='+ dbdata['password'])
    
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
        sql = "select * from accountdetails where customerid ='%s' and status ='live' and acc_type IN ('SAVINGS','CURRENT')"%(customerid)
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
        cursor.execute(sql)
        db.commit()

import sqlite3
import json
import traceback
import time
from hexhash import getTranxid
class Dbase():
    @staticmethod
    def emailExists(email):
        db = sqlite3.connect('database/main.db')
        cursor =  db.cursor()
        sql = "select * from netbankusers where email = ?"
        try :
            cursor.execute(sql,(email,))
        except Exception as e:

            traceback.print_exc()
            raise e
        if len(cursor.fetchall())==0:
            return False
        else:
            return True

    @staticmethod
    def securitynumberExists(ssn):
        db = sqlite3.connect('database/main.db')
        cursor =  db.cursor()
        sql = "select * from netbankusers where ssn = ?"
        try:
            cursor.execute(sql,(ssn,))
        except Exception as e:
            traceback.print_exc()
            raise e
        if len(cursor.fetchall())==0:
            return False
        else:
            return True

    @staticmethod
    def verificationNumberExists(number,verification_type):
        db = sqlite3.connect('database/main.db')
        cursor = db.cursor()
        tablename= verification_type
        try:
            sql = "select * from %s where number = ?"%(tablename)
            cursor.execute(sql,(number,))
        except Exception as e:

            traceback.print_exc()
            raise e
        if len(cursor.fetchall()) == 0:
            return False
        else:
            return True

    @staticmethod
    def verifyPassword(number,verification_type,password):
        db = sqlite3.connect('database/main.db')
        cursor = db.cursor()
        tablename= verification_type
        try:
            sql = "select * from %s where number = ? and password = ?"%(tablename)
            if verification_type in ('creditcard','debitcard'):
                sql = "select * from %s where number = ? and pin = ?"%(tablename)
            cursor.execute(sql,(number,password))
        except Exception as e:

            traceback.print_exc()
            raise e
        if len(cursor.fetchall()) == 0:
            return False
        else:
            return True

    @staticmethod
    def verifySecurityNumber(number,verification_type,securitynumber):
        db = sqlite3.connect('database/main.db')
        cursor = db.cursor()
        tablename= verification_type
        try:
            sql = "select * from %s where number = ? and ssn = ?"%(tablename)
            cursor.execute(sql,(number,securitynumber))
        except Exception as e:

            traceback.print_exc()
            raise e
        if len(cursor.fetchall()) == 0:
            return False
        else:
            return True

    @staticmethod
    def mobilenoExists(mobileno):
        db = sqlite3.connect('database/main.db')
        cursor =  db.cursor()
        sql = "select * from netbankusers where mobileno = ?"
        try :
            cursor.execute(sql,(mobileno,))
        except Exception as e:

            traceback.print_exc()
            raise e
        if len(cursor.fetchall())==0:
            return False
        else:
            return True


    @staticmethod
    def register(params):
        db = sqlite3.connect('database/main.db')
        cursor =  db.cursor()
        try:
            ssn = params['securitynumber']
            sql = "select number,'loanaccount',ssn from loanaccount where ssn = ?"
            cursor.execute(sql,(ssn,))
            loanaccounts = cursor.fetchall()
            sql = "select number,'insurance',ssn from insurance where ssn = ?"
            cursor.execute(sql,(ssn,))
            insurances  = cursor.fetchall()
            sql = "select number,'creditcard',ssn from creditcard where ssn = ?"
            cursor.execute(sql,(ssn,))
            creditcards  = cursor.fetchall()
            sql = "select number,'debitcard',ssn from debitcard where ssn = ?"
            cursor.execute(sql,(ssn,))
            debitcards = cursor.fetchall()
            sql = "insert into netbankusers values(?,?,?,?,?,?,?)"
            cursor.execute(sql,(params['securitynumber'],params['username'],params['userpassword'],params['question'],params['answer'],params['email'],params['mobileno']))
            sql = "insert into linkedaccount values(?,?,?)"
            for account in loanaccounts:
                cursor.execute(sql,account)
            for account in insurances:
                cursor.execute(sql,account)
            for account in creditcards:
                cursor.execute(sql,account)
            for account in debitcards:
                cursor.execute(sql,account)
            db.commit()

        except Exception as e:
            db.rollback()

            traceback.print_exc()
            raise e
        print('registered')
    @staticmethod
    def deleteNetBankUser(securitynumber):
        db = sqlite3.connect('database/main.db')
        cursor =  db.cursor()
        try:
            sql = "delete from netbankusers where ssn = ?"
            cursor.execute(sql,(securitynumber,))
            db.commit()
        except Exception as e:
            db.rollback()

            traceback.print_exc()
            raise e

    @staticmethod
    def usernameExists(username):
        db = sqlite3.connect('database/main.db')
        cursor =  db.cursor()
        try:
            sql = "select * from netbankusers where username = ?"
            cursor.execute(sql,(username,))
        except Exception as e:
            traceback.print_exc()
            raise e
        if len(cursor.fetchall())==0:
            return False
        else:
            return True

    @staticmethod
    def verifyLoginPassword(username,password):
        db = sqlite3.connect('database/main.db')
        cursor =  db.cursor()
        try:
            sql = "select * from netbankusers where username = ? and password = ?"
            cursor.execute(sql,(username,password))
        except Exception as e:
            traceback.print_exc()
            raise e
        if len(cursor.fetchall())==0:
            return False
        else:
            return True

    @staticmethod
    def getSecurityNumber(username):
        db = sqlite3.connect('database/main.db')
        cursor =  db.cursor()
        try:
            sql = 'select ssn from netbankusers  where username = ?'
            cursor.execute(sql,(username,))
        except Exception as e:
            traceback.print_exc()
            raise e
        return cursor.fetchone()[0]
    @staticmethod
    def getCustomerName(ssn):
        db = sqlite3.connect('database/main.db')
        cursor =  db.cursor()
        try:
            sql = "select accounttype from linkedaccount where ssn = ?"
            cursor.execute(sql,(ssn,))
            accounttype = cursor.fetchone()[0]
            sql = "select name from "+accounttype+" where ssn = ?"
            cursor.execute(sql,(ssn,))
            name = cursor.fetchone()[0]
        except Exception as e:
            raise e
        return name


    @staticmethod
    def getLoanAccounts(ssn):
        db = sqlite3.connect('database/main.db')
        cursor =  db.cursor()
        try:
            sql = "select * from loanaccount where ssn = ?"
            cursor.execute(sql,(ssn,))
        except Exception as e:
            raise e
        return cursor.fetchall()

    @staticmethod
    def getCreditCards(ssn):
        db = sqlite3.connect('database/main.db')
        cursor =  db.cursor()
        try:
            sql = "select * from creditcard where ssn = ?"
            cursor.execute(sql,(ssn,))
        except Exception as e:
            raise e
        return cursor.fetchall()

    @staticmethod
    def getDebitCards(ssn):
        db = sqlite3.connect('database/main.db')
        cursor =  db.cursor()
        try:
            sql = "select * from debitcard where ssn = ?"
            cursor.execute(sql,(ssn,))
        except Exception as e:
            raise e
        return cursor.fetchall()

    @staticmethod
    def getInsuranceAccounts(ssn):
        db = sqlite3.connect('database/main.db')
        cursor =  db.cursor()
        try:
            sql = "select * from insurance where ssn = ?"
            cursor.execute(sql,(ssn,))
        except Exception as e:
            raise e
        return cursor.fetchall()

    @staticmethod
    def getAccountDetails(accounttype,accountno):
        db = sqlite3.connect('database/main.db')
        cursor =  db.cursor()
        try:
            sql = "select * from "+accounttype+" where number = ?"
            cursor.execute(sql,(accountno,))
        except Exception as e:
            raise e
        return cursor.fetchone()

    @staticmethod
    def getTransactionDetails(accounttype,accountno):
        db = sqlite3.connect('database/main.db')
        cursor =  db.cursor()
        try:
            sql = "select * from transactions where account1 = ? and account1type = ?"
            cursor.execute(sql,(accountno,accounttype))
        except Exception as e:
            raise e
        return cursor.fetchall()

    @staticmethod
    def getDebitCardAccountno(number):
        db = sqlite3.connect('database/main.db')
        cursor =  db.cursor()
        try:
            sql = "Select accountno from debitcard where number = ?"
            cursor.execute(sql,(number,))
            return cursor.fetchone()[0]
        except Exception as e:
            raise e



    @staticmethod
    def getSavingsAccounts(ssn):
        db = sqlite3.connect('database/main.db')
        cursor =  db.cursor()
        try:
            sql = "select * from debitcard where ssn = ?"
            cursor.execute(sql,(ssn,))
        except Exception as e:
            raise e
        return cursor.fetchall()

    @staticmethod
    def hasAccountBalance(accountno,reqbalance):
        db = sqlite3.connect('database/main.db')
        cursor = db.cursor()
        try:
            sql = "select balance from debitcard where accountno = ?"
            cursor.execute(sql,(accountno,))
            balance = cursor.fetchone()[0]
            if float(balance) >= float(reqbalance):
                return True
            else:
                return False
        except Exception as e:
            raise e

    @staticmethod
    def transfer(fromaccount,toaccount,amount):
        db = sqlite3.connect('database/main.db')
        cursor = db.cursor()
        try:
            sql = "select balance from debitcard where accountno = ?"
            cursor.execute(sql,(fromaccount,))
            from_bal = cursor.fetchone()[0]
            cursor.execute(sql,(toaccount,))
            to_bal =  cursor.fetchone()[0]

            from_bal = "%.2f" % (float(from_bal) - float(amount))
            to_bal = "%.2f" % (float(to_bal) + float(amount) )
            sql = "update debitcard set balance = ?  where accountno = ?"
            cursor.execute(sql,(to_bal,toaccount))
            cursor.execute(sql,(from_bal,fromaccount))
            Dbase.addTransactions(cursor,fromaccount,'debitcard',toaccount,'debitcard',amount)
            db.commit()
        except Exception as e:
            db.rollback()
            print (e)
            raise Exception("Some Error Occured!")

    @staticmethod
    def pay(accounttype, number,fromaccount):
        db = sqlite3.connect('database/main.db')
        cursor = db.cursor()
        if accounttype =="loanaccount":
            debt_name = "loanamount"
        elif accounttype == "creditcard":
            debt_name = "amountdue"
        else:
            debt_name = "premium"
        try:
            sql = "select balance from debitcard where accountno = ?"
            cursor.execute(sql,(fromaccount,))
            from_bal =  cursor.fetchone()[0]
            sql ="select " + debt_name + " from " + accounttype + " where number = ?"
            cursor.execute(sql,(number,))
            debt_amount = cursor.fetchone()[0]

            from_bal = "%.2f" %(float(from_bal) - float(debt_amount))
            # debt_amount = "0"
            sql = "update debitcard set balance = ?  where accountno = ?"
            cursor.execute(sql,(from_bal,fromaccount))
            sql = "update "+ accounttype + " set " + debt_name + " = ? where number = ?"
            cursor.execute(sql,("0",number))
            Dbase.addTransactions(cursor,fromaccount,'debitcard',number,accounttype,debt_amount)

            db.commit()
        except Exception as e:
            db.rollback()
            print (e)
            raise Exception("Some Error Occured!")
    
    @staticmethod
    def addTransactions(cursor,fromaccount,fromaccounttype,toaccount,toaccounttype,amount):
        date = time.strftime('%m:%d:%Y %H:%M:%S')
        
        try:
            tranxid = getTranxid(fromaccount,toaccount,date)
            sql = "insert into transactions(tranxid,account1,account1type,account2,account2type,amount,tranxtype,tranx_time,tranx_status) values(?,?,?,?,?,?,?,?,?)"
            cursor.execute(sql,(tranxid,fromaccount,fromaccounttype,toaccount,toaccounttype,amount,"credit",date,"Completed"))
            tranxid = getTranxid(toaccount,fromaccount,date)
            cursor.execute(sql,(tranxid,toaccount,toaccounttype,fromaccount,fromaccounttype,amount,"credit",date,"Completed"))
        except Exception as e:
            raise e

    @staticmethod
    def accountExists(accountno):
        db = sqlite3.connect('database/main.db')
        cursor = db.cursor()
        try:
            sql = "select * from debitcard where accountno = ?"
            cursor.execute(sql,(accountno,))
            if (len(cursor.fetchall())==0):
                return False
            else:
                return True
        except Exception as e:
            traceback.print_exc()
            raise Exception("Some Error Occured")

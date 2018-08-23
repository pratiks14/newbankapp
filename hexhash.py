import sqlite3
import json
import traceback

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

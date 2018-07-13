from flask import make_response
import re
import json
from db import dbase


class Verification():
    @staticmethod
    def accVerification(params):
        response = Verification.validateAddress(params['address'] +params['address2']+params['city']+params['state']+params['zip'])
        if response is not None:
            return response
        
        response = Verification.validateZip(params['zip'])    
        if response is not None:
            return response

        response = Verification.validateAadhar(params['aadharno'])    
        if response is not None:
            return response
        
        
        
        
        return response

    @staticmethod
    def validateAadhar(aadharno):
        if re.match(r'^[0-9]{12}$',aadharno) is None:
            response = make_response(json.dumps('Invalid Aadhar Card Number'),401)
            response.headers['Content-Type'] = 'application/json'
            return response
        else:
            return None

    @staticmethod
    def validateAddress(address):
        if len(address) >220:
            response = make_response(json.dumps('Your Address is too long'),401) 
            response.headers['Content-Type'] = 'application/json'
            return response
        else:
            return None      

    @staticmethod
    def validateZip(zip):
        if re.match(r'^[0-9]{6}$',zip) is None:
            response = make_response(json.dumps('Invalid ZIP code'),401)
            response.headers['Content-Type'] = 'application/json'
            return response    
        else:
            return None

    @staticmethod
    def verifyDebitAccount(accountno,amount):
        if re.match(r'^\d+$',amount) is None:
            response = make_response(json.dumps('Amount should be a number.'),401)
            response.headers['Content-Type'] = 'application/json'
            return response

        if int(amount) % 500 != 0 or int(amount) / 500 == 0:
            response = make_response(json.dumps('Min Amount is Rs 500 or multiple of 500'),401)
            response.headers['Content-Type'] = 'application/json'
            return response

        db = dbase.getDB()
        cursor = db.cursor()
        sql = "select * from depositDetails where debit_acc ='%s'"%(accountno)
        cursor.execute(sql)
        account = cursor.fetchone()
        if account is not None:
            response = make_response(json.dumps('This account has already been linked to a Deposit Account'),401)
            response.headers['Content-Type'] = 'application/json'
            return response

        acc_balance = dbase.getAccountBalance(accountno)
        if float(acc_balance) < float(amount):
            response = make_response(json.dumps('Not enough balance in your acccount.'),401)
            response.headers['Content-Type'] = 'application/json'
            return response   
        
       

        return None


    
    @staticmethod
    def verifyAccountExists(accountno,live=False):
        if re.match(r'^\d{16}$',accountno) is None:
            response = make_response(json.dumps('Enter 16 digit account Number'),401)
            response.headers['Content-Type'] = 'application/json'
            return response
        db = dbase.getDB()
        cursor = db.cursor()
        sql = "select * from accountdetails where accountno='%s' "%(accountno)
        if live:
            sql = "select * from accountdetails where accountno='%s' and status='Live' "%(accountno)
        cursor.execute(sql)
        account = cursor.fetchall()
        if account == []:
            response = make_response(json.dumps('There is no Account with this Account Number!'),401)
            response.headers['Content-Type'] = 'application/json'
            return response
        return None    

    @staticmethod
    def validatePin(pin):
        if re.match(r'^\d+$',pin) is None:
            response = make_response(json.dumps('PIN should be digits'),401)
            response.headers['Content-Type'] = 'application/json'
            return response

        if len(pin) != 4:
            response = make_response(json.dumps('It should 4 digit!'),401)
            response.headers['Content-Type'] = 'application/json'
            return response
        
        return None

    @staticmethod
    def validateAmount(accountno,amount):
        if re.match(r'^\d+$',amount) is None:
            response = make_response(json.dumps('Amount should be a number.'),401)
            response.headers['Content-Type'] = 'application/json'
            return response

        if int(amount) % 500 != 0 or int(amount) / 500 == 0:
            response = make_response(json.dumps('Min Amount is Rs 500 or multiple of 500'),401)
            response.headers['Content-Type'] = 'application/json'
            return response
        
        acc_balance = dbase.getAccountBalance(accountno)
        if float(acc_balance) < float(amount):
            response = make_response(json.dumps('Not enough balance in your acccount.'),401)
            response.headers['Content-Type'] = 'application/json'
            return response

        return None 
        

    @staticmethod
    def validateAccTransfer(data):
        response = Verification.verifyAccountExists(data['toaccount'],True)
        if response is not None:
            return response
        response = Verification.validateAmount(data['fromaccount'],data['amount'])
        if response is not None:
            return response
        return None    

from flask import make_response
from flask import session as login_session
import re
import sqlite3
import json
import traceback
from db import Dbase
import time

class Validation():
    @staticmethod
    def email(email):
        if re.match(r"^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$",email) == None:
            response = make_response(json.dumps('Invalid Email Format'), 400)
            response.headers['Content-Type'] = 'application/json'
            return response
        elif len(email) > 254 :
            response = make_response(json.dumps('Email too long'), 400)
            response.headers['Content-Type'] = 'application/json'
            return response
        
        if Dbase.emailExists(email):
            response = make_response(json.dumps('This email has already been registered with an account'), 400)
            response.headers['Content-Type'] = 'application/json'
            return response
        return None
    
    @staticmethod
    def securitynumber(number,verification_type,securitynumber):
        if re.match(r"^[0-9]{6}$",securitynumber) == None:
            response = make_response(json.dumps('Invalid Security Number'), 400)
            response.headers['Content-Type'] = 'application/json'
            return response
        
        if not Dbase.verifySecurityNumber(number,verification_type,securitynumber):
            response = make_response(json.dumps('Security Number doesn\'t match'), 400)
            response.headers['Content-Type'] = 'application/json'
            return response
        return None
    
    @staticmethod
    def accountNumber(number,verification_type):
        if re.match(r"^[0-9]{16}$",number)== None:
            message = ''
            if verification_type == 'loanaccount':
                message = "Invalid Loan Account Number"
            elif verification_type == 'insurance':
                message  = 'Invalid Insurance number'
            else:
                message = 'Invalid Card Number'
            response = make_response(json.dumps(message), 400)
            response.headers['Content-Type'] = 'application/json'
            return response
        if not Dbase.verificationNumberExists(number,verification_type):
            response = make_response(json.dumps('Account with this number hasn\'t been opened.'), 400)
            response.headers['Content-Type'] = 'application/json'
            return response
        return None
    
    @staticmethod
    def password(number,verification_type, password):
        if not Dbase.verifyPassword(number,verification_type,password):
            if verification_type in ("creditcard","debitcard"):
                response = make_response(json.dumps('PIN doesn\'t match.'), 400)
                response.headers['Content-Type'] = 'application/json'
                return response
            response = make_response(json.dumps('Password doesn\'t match.'), 400)
            response.headers['Content-Type'] = 'application/json'
            return response
        return None
    
    @staticmethod
    def mobileno(mobileno):
        if re.match(r'^[0-9]{10}$',mobileno) == None:
            response = make_response(json.dumps('Invalid mobile Number'), 400)
            response.headers['Content-Type'] = 'application/json'
            return response
        if Dbase.mobilenoExists(mobileno):
            response = make_response(json.dumps('Mobile number already registered with an account'), 400)
            response.headers['Content-Type'] = 'application/json'
            return response
        
        return None

    @staticmethod
    def username(username):
        if len(username)<3:
            response = make_response(json.dumps('Username must have atleast 3 character'), 400)
            response.headers['Content-Type'] = 'application/json'
            return response
        if Dbase.usernameExists(username):
            response = make_response(json.dumps('Username already taken'), 400)
            response.headers['Content-Type'] = 'application/json'
            return response
        response = make_response(json.dumps('Valid Username'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    @staticmethod
    def userpassword(userpassword):
        if len(userpassword)<3:
            response = make_response(json.dumps('Password must have atleast 6 character'), 400)
            response.headers['Content-Type'] = 'application/json'
            return response
        if userpassword.upper() == userpassword or userpassword.lower() == userpassword or re.search(r'[0-9]+',userpassword) == None:
            response = make_response(json.dumps('Password must follow the Format given'), 400)
            response.headers['Content-Type'] = 'application/json'
            return response
        return None
    
   
class Operations():
    
    @staticmethod
    def validate(params):
        try:
            if params['registerno'] == '1':
                verification_type = params['verificationtype']
                securitynumber  = params['securitynumber']
                if Dbase.securitynumberExists(securitynumber):
                    response = make_response(json.dumps('You have already registered with us'), 400)
                    response.headers['Content-Type'] = 'application/json'
                    return response

                number = params['number'].strip()
                resp = Validation.accountNumber(number,verification_type)
                if resp != None:
                    return resp
                password = params['password'].strip()
                resp = Validation.password(number,verification_type,password)
                if resp != None:
                    return resp
                
                resp = Validation.securitynumber(number,verification_type,securitynumber)
                if resp != None:
                    return resp
                email = params['email'].strip()
                resp = Validation.email(email)
                if resp != None:
                    return resp
                mobileno = params['mobileno'].strip()
                resp = Validation.mobileno(mobileno)
                if resp != None:
                    return resp
                
            elif params['registerno'] == '2':
                username = params['username']
                userpassword = params['userpassword']
                resp = Validation.username(username)
                if resp != None:
                    return resp
                resp = Validation.userpassword(userpassword)
                if resp != None:
                    return resp
                
            elif params['registerno'] == '3':
                answer = params['answer']
                if len(answer)==0:
                    response = make_response(json.dumps('Give a valid Answer'), 400)
                    response.headers['Content-Type'] = 'application/json'
                    return response
                
            else:
                print(params['registerno'] == 'confirm')
                Dbase.register(params)
                customername = Dbase.getCustomerName(params['securitynumber'])
                login_session['ssn'] = params['securitynumber']
                login_session['customername'] = customername
                login_session['username'] = params['username']
                response = make_response(json.dumps('Registered'), 200)
                response.headers['Content-Type'] = 'application/json'
                return response
            response = make_response(json.dumps('Registered'), 200)
            response.headers['Content-Type'] = 'application/json'
            return response
        except Exception as e:
            raise e
        
    @staticmethod
    def loginValidate(params):
        try:
            if 'password' not in params:
                username = params['username']
                if not Dbase.usernameExists(username):
                    response = make_response(json.dumps('InValid Username'), 400)
                    response.headers['Content-Type'] = 'application/json'
                    return response
                response = make_response(json.dumps('Valid Username'), 200)
                response.headers['Content-Type'] = 'application/json'
                return response	
            else:
                username = params['username']
                password = params['password']
                if not Dbase.verifyLoginPassword(username,password):
                    response = make_response(json.dumps('Invalid Credentials'), 400)
                    response.headers['Content-Type'] = 'application/json'
                    return response	
				
				#login successful
                ssn = Dbase.getSecurityNumber(username)
                customername = Dbase.getCustomerName(ssn)
                login_session['ssn'] = ssn
                login_session['customername'] = customername
                login_session['username'] = username
                response = make_response(json.dumps('Valid Credentials'), 200)
                response.headers['Content-Type'] = 'application/json'
                return response
        except Exception as e:
            raise e
        
    @staticmethod
    def getCustomerDetailsDict(ssn):
        try:
            customerDetails = {}
            loanaccounts = Dbase.getLoanAccounts(ssn)
            loanaccountlist = []
            for loanaccount in loanaccounts:
                loanDict = {}
                loanDict['loannumber'] = loanaccount[0]
                loanDict['customername'] = loanaccount[1]
                loanDict['password'] = loanaccount[2]
                loanDict['loantype'] = loanaccount[4]
                loanDict['loanamount'] = str(loanamount[5])
                loanaccountlist.append(loanDict)
            customerDetails['loanaccounts'] = loanaccountlist

            creditCardAccounts = Dbase.getCreditCards(ssn)
            creditCardList = []
            for creditAccount in creditCardAccounts:
                creditDict = {}
                creditDict['cardnumber'] = creditAccount[0]
                creditDict['cardholder'] = creditAccount[1]
                creditDict['pin'] = creditAccount[2]
                creditDict['creditlimit'] = str(creditAccount[4])
                creditDict['amountdue'] = str(creditAccount[5])
                creditCardList.append(creditDict)
            customerDetails['creditcards'] = creditCardList

            debitCardAccounts = Dbase.getDebitCards(ssn)
            debitCardList = []
            for debitAccount in debitCardAccounts:
                debitDict = {}
                debitDict['cardnumber'] = debitAccount[0]
                debitDict['cardholder'] = debitAccount[2]
                debitDict['pin'] = debitAccount[3]
                debitDict['accountnumber'] = debitAccount[1]
                debitDict['accountbalance'] = str(debitAccount[5])
                debitDict['accounttype'] = debitAccount[6]
                debitCardList.append(debitDict)
            customerDetails['debitcards'] = debitCardList

            insuranceAccounts = Dbase.getInsuranceAccounts(ssn)
            insuranceList = []
            for insurance in insuranceAccounts:
                insuranceDict = {}
                insuranceDict['number'] = insurance[0]
                insuranceDict['customername'] = insurance[1]
                insuranceDict['password'] = insurance[2]
                insuranceDict['insurancetype'] = insurance[4]
                insuranceDict['premium'] = insurance[5]
                insuranceDict['duedate'] = time.strftime('%d\%m\%Y',time.strptime(insurance[6],'%d-%m-%Y'))
                insuranceList.append(insuranceDict)
            customerDetails['insurances'] = insuranceList
            
            return customerDetails
        except Exception as e:
            raise e
            

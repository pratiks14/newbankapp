from flask import Flask,render_template,request
from flask import redirect,jsonify,url_for,flash
from flask import session as login_session

import string
import json
import locale
from datetime import timedelta
# import httplib2
from flask import make_response
import pyodbc
import re
import time
import sys
from accverification import Verification
from generator import Generator
from db import dbase
import random


app = Flask(__name__)
state=sorted(["Andhra Pradesh","Arunachal Pradesh ","Assam","Bihar","Chhattisgarh","Goa","Gujarat","Haryana","Himachal Pradesh","Jammu and Kashmir","Jharkhand","Karnataka","Kerala","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Punjab","Rajasthan","Sikkim","Tamil Nadu","Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal","Andaman and Nicobar Islands","Chandigarh","Dadra and Nagar Haveli","Daman and Diu","Lakshadweep","Delhi","Puducherry"])	

bug_list = [False] * 10
filename = 'bugconfig.json'
with open(filename, 'r') as f:
	bugdata = json.load(f)
no_of_bugs = int(bugdata['no_of_bugs'])
bug_list = Generator.generateBugIndex(no_of_bugs,len(bug_list),bug_list)

@app.route('/')
def showIndex():
    return render_template('index2.html')


@app.route('/netlogin')
def netLoginPage():
	location = request.args.get('loc')

	return render_template('netbanklogin.html',location=location)




@app.route('/register')
def getRegisterForm():
	customerid = Generator.generateCustomerid()
	login_session['customerid'] = customerid
	return render_template('register.html',customerid=customerid)

def checkCustomerIdExists(customerid):
	filename = 'dbconfig.json'
	with open(filename, 'r') as f:
		dbdata = json.load(f)
	
	db = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+dbdata['server']+';DATABASE='+dbdata['database']+';UID='+dbdata['username']+';PWD='+ dbdata['password'])
	cursor = db.cursor()
	sql = "select * from netbankusers where customerid = '%s'" % (customerid,)
	cursor.execute(sql)
	account = cursor.fetchone()

	if account is not None :
	
		return account
	else:
		return False

def emailExists(email):
	filename = 'dbconfig.json'
	with open(filename, 'r') as f:
		dbdata = json.load(f)
	
	db = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+dbdata['server']+';DATABASE='+dbdata['database']+';UID='+dbdata['username']+';PWD='+ dbdata['password'])
	cursor = db.cursor()
	sql = "select * from netbankusers where emailid = '%s'"%(email,)
	cursor.execute(sql)
	account =cursor.fetchone()
	if bug_list[0]:
		return False
	if account is not None:
		return True
	else:
		return False	

def mobilenoExists(number):
	filename = 'dbconfig.json'
	with open(filename, 'r') as f:
		dbdata = json.load(f)
	
	db = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+dbdata['server']+';DATABASE='+dbdata['database']+';UID='+dbdata['username']+';PWD='+ dbdata['password'])
	cursor = db.cursor()
	sql = "select * from netbankusers where mobileno = '%s'"%(number,)
	cursor.execute(sql)
	account =cursor.fetchone()
	
	if account is not None:
		return True
	else:
		return False	

def validateEmail(email):
	if re.match(r"^[@a-zA-Z0-9]+\.com$",email) == None:
		response = make_response(json.dumps('Invalid Email Format'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	elif len(email) > 49 :
		response = make_response(json.dumps('Email too long'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	elif emailExists(email):
		response = make_response(json.dumps('Email already registered'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	
	return None

def validateMobile(number):
	if re.match(r"^[0-9]{10}$",number)==None:
		if not bug_list[1]:		
			response = make_response(json.dumps('Invalid Mobile Number'), 401)
			response.headers['Content-Type'] = 'application/json'
			return response
	elif mobilenoExists(number):
		response = make_response(json.dumps('Mobile No already linked to a CustomerId!'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	
	return None

def validatePassword(pwrd):
	if len(pwrd) < 6:
		if not bugs_list[2]:
			response = make_response(json.dumps('Password length less than 6'), 401)
			response.headers['Content-Type'] = 'application/json'
			return response
	
	return None	

def validateName(name):
	if len(name) == 0:
		response = make_response(json.dumps('Provide a valid name!'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	else:
		return None	

def register(params):

	if  "customerid" not in login_session:
		response = make_response(json.dumps('Session Expired!!'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	name_list = params['name'].split(' ')
	name_list = [a[0].upper()+a[1:] for a in name_list]
	name = ' '.join(name_list)
	login_session['name'] = name
	login_session['mobileno'] = params['mobileno']
	login_session['email'] = params['email']
	login_session['password'] = params['password']
	login_session['reward_points'] = 0
	last_login = ''
	current_login = time.strftime('%Y-%m-%d %H:%M:%S')

	try:
		filename = 'dbconfig.json'
		with open(filename, 'r') as f:
			dbdata = json.load(f)
		
		db = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+dbdata['server']+';DATABASE='+dbdata['database']+';UID='+dbdata['username']+';PWD='+ dbdata['password'])
		cursor = db.cursor()
		sql="""insert into netbankusers(customerid,emailid,mobileno,name,password,login_time)
		values('%s','%s','%s','%s','%s',
		'%s')"""%(login_session['customerid'],login_session['email'],login_session['mobileno'],login_session['name'],params['password'],current_login)
	


	
		cursor.execute(sql)
		db.commit()
	except Exception as e:
		db.rollback()
		print(e)
		exc_type, exc_value, exc_traceback = sys.exc_info() # most recent (if any) by default
		print(exc_traceback.tb_lineno)
		raise Exception(e)
	
	login_session['last_login'] = last_login

@app.route('/signup', methods=['POST'])
def signup():
	params = json.loads(request.data.decode('utf-8'))
	
	response = validateName(params['name'])
	if response is not None:
		return response
	
	response = validateEmail(params['email'])
	if response is not None:
		return response
	response = validateMobile(params['mobileno'])
	if response is not None:
		return response

	response = validatePassword(params['password'])
	if response  is not None:
		return response

	try:
		register(params)
		# login_session.permanent = True

	except Exception as e:
		print(e)		
		exc_type, exc_value, exc_traceback = sys.exc_info() # most recent (if any) by default
		print(exc_traceback.tb_lineno)

		# print(login_session['customerid'])
		response = make_response(json.dumps('Some Error Occured.Try Again!'), 402)
		response.headers['Content-Type'] = 'application/json'
		return response
	
	
	response = make_response(json.dumps('Registration Successfull!! Logging in.....'), 200)
	response.headers['Content-Type'] = 'application/json'
	return response



def setLoginTime():
	filename = 'dbconfig.json'
	with open(filename, 'r') as f:
		dbdata = json.load(f)
	
	db = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+dbdata['server']+';DATABASE='+dbdata['database']+';UID='+dbdata['username']+';PWD='+ dbdata['password'])
	cursor = db.cursor()
	sql = "update netbankusers set login_time = '%s' where customerid = '%s'"%(time.strftime('%Y-%m-%d %H:%M:%S'),login_session['customerid'])
	try:
		cursor.execute(sql)
		db.commit()
	except Exception as e:
		db.rollback()
		print(e)	


@app.route('/idlogin',methods=['POST'])
def idlogin():
	params = json.loads(request.data.decode('utf-8'))
	customerid = params['customerid']
	password = params['password']
	print(login_session)
	if "customerid" in login_session and login_session['customerid'] == customerid and password==login_session['password']:
		response = make_response(json.dumps('You are already logged in!'), 200)
		response.headers['Content-Type'] = 'application/json'
		return response

	account = checkCustomerIdExists(customerid)
	

	if account and account[4] == password:
		login_session['email'] = account[1]
		login_session['mobileno'] = account[2]
		login_session['name'] = account[3]
		login_session['customerid'] = customerid
		login_session['last_login'] = getLastlogin().strftime("%I:%M %p %a, %d %b %Y")
		login_session['password'] = password
		login_session['reward_points'] = account[6]
		if bug_list[2]:
			login_session['last_login'] = ''
		setLoginTime()
		
		response = make_response(json.dumps('Login Successfull!! Logging in.....'), 200)
		response.headers['Content-Type'] = 'application/json'
		return response
	else:
		response = make_response(json.dumps('Invalid Credentials.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response


@app.route('/adminlogin')
def adminLoginPage():
	return render_template('adminlogin.html')

@app.route('/login',methods=['POST'])
def login():
	params = json.loads(request.data.decode('utf-8'))
	password = params['password']
	if password == "admin@123":
		login_session.clear()
		login_session['name'] = "Admin"
		login_session['customerid'] = "admin@123"

		response = make_response(json.dumps('Loggin in..'),200)
		response.headers['Content-Type'] = 'application/json'
		return response
	else:
		response = make_response(json.dumps('Invalid Credentials.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

@app.route('/acceptaccrequest',methods=['POST'])
def acceptRequest():
	params = json.loads(request.data.decode('utf-8'))
	accountno = params['accountno']
	try:
		dbase.acceptAccCreation(accountno)
	except:
		response = make_response(json.dumps('Some Error Occured!Try Again'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	response = make_response(json.dumps('Account opened!'), 200)
	response.headers['Content-Type'] = 'application/json'
	return response


@app.route('/rejectaccrequest',methods=["POST"])
def rejectRequest():
	params = json.loads(request.data.decode('utf-8'))
	accountno = params['accountno']
	try:
		dbase.rejectAccCreation(accountno)
	except:
		response = make_response(json.dumps('Some Error Occured!Try Again'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	response = make_response(json.dumps('Account closed!'), 200)
	response.headers['Content-Type'] = 'application/json'
	return response


@app.route('/admin')
def admin():
	if "name" not in login_session:
		return redirect("/adminlogin")
	accounts = dbase.getAppliedAccounts()
	if accounts is not None:
		for account in accounts:
			account[7] = account[7].strftime("%d %b %Y")
	return render_template('admin.html',accounts = accounts)


@app.route('/admin/update')
def showUpdateAccount():
	if "name" not in login_session:
		return redirect("/netlogin/main")

	return render_template('updateaccount.html',account = None)

@app.route('/verifyaccount')
def verifyAccount():
	accountno = request.args.get('accountno')
	response = Verification.verifyAccountExists(accountno)
	if response is not None:
		return response	

	response = make_response(json.dumps('got account'), 200)
	response.headers['Content-Type'] = 'application/json'
	return response

@app.route('/admin/update/<accountno>')
def fetchAccount(accountno):
	account = dbase.getAccountDetails(accountno)
	account[7] = account[7].strftime("%d %b %Y")
	return render_template('updateaccount.html',account = account)



@app.route('/deleteaccount',methods=['POST'])
def deleteAccount():
	params = json.loads(request.data.decode('utf-8'))
	try:
		if not bug_list[3]:
			dbase.deleteAccount(params['accountno'])
	except Exception as e:
		print(e)
		response = make_response(json.dumps('Some Error Occured!Try Again'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	response = make_response(json.dumps('Account Deleted Successfully'), 200)
	response.headers['Content-Type'] = 'application/json'
	return response	

@app.route('/updateaccount',methods=['POST'])
def updateAccount():
	params = json.loads(request.data.decode('utf-8'))
	response = Verification.validateAadhar(params['aadharno'])
	if response is not None:
		return response
	accounttype = params['accounttype'].upper()
	accountno = params['accountno']
	aadharno = params['aadharno']
	try:
		if not bug_list[4]:
			dbase.updateAccountDetails(accountno,accounttype,aadharno)
	except Exception as e:
		print(e)
		response = make_response(json.dumps('Some Error Occured!Try Again'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	response = make_response(json.dumps('Account Updated Successfully'), 200)
	response.headers['Content-Type'] = 'application/json'
	return response

@app.route('/admin/transaction')
def showTranasac():
	if "name" not in login_session:
		return redirect("/adminlogin")
	return render_template('transactions.html',statements=None)

@app.route('/admin/transaction/<accountno>')
def fetchTransaction(accountno):
	creditTranx = dbase.getCreditTransaction(accountno)
	debitTranx = dbase.getDebitTransaction(accountno)
	final_statement = []
	for tranx in creditTranx:
		statement = "Account credited with Rs " +str(tranx[3])+" from Account No: "+tranx[1]+" on " +tranx[5].strftime("%I:%M %p , %d %b %Y")
		final_statement.append(statement)
	for tranx in debitTranx:
		statement =  "Rs "+str(tranx[3])+" debited  from Account to Account No: "+tranx[1]+" on " +tranx[5].strftime("%I:%M %p , %d %b %Y")
		final_statement.append(statement)	
	# print(final_statement)
	return render_template('transactions.html',statements = final_statement)


def getLastlogin():
	filename = 'dbconfig.json'
	with open(filename, 'r') as f:
		dbdata = json.load(f)
	
	db = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+dbdata['server']+';DATABASE='+dbdata['database']+';UID='+dbdata['username']+';PWD='+ dbdata['password'])
	cursor = db.cursor()
	sql = "select login_time from netbankusers where customerid ='%s'"%(login_session["customerid"],)
	
	cursor.execute(sql)	
	user = cursor.fetchone()
	return user[0]


@app.route('/main')
def showMain():
	if "customerid" not in login_session:
		return redirect("/netlogin/main")
	# try:
	rejected_account = dbase.getRejectedAccounts(login_session['customerid'])
	dbase.deleteRejectedAccounts(login_session['customerid'])
	if rejected_account is not None:
		for account in rejected_account:
			message = "Your application for <b>" + account[3].lower() + "</b> account has been rejected!" 
			flash(message)
	creditTranxList = dbase.getCreditTranx(login_session['customerid'])
	for tranx in creditTranxList:
		message = "Account: "+tranx[1]+" is <b>credited</b> by &#8377;"+str(tranx[2])+" to Account: "+tranx[0]
		flash(message)

	
	# except Exception as e:
	# 	print(e)

	accounts = dbase.getAccounts(login_session['customerid'])
	if accounts is not None:
		for account in accounts:
			account[7] = account[7].strftime("%d %b %Y")
	return render_template('main.html',accounts = accounts,last_login=login_session['last_login'],states=state)


@app.route('/createacc',methods=['POST'])
def createAccount():
	params  = json.loads(request.data.decode('utf-8'))
	response = Verification.accVerification(params)
	if response is not None:
		return response
	else:
		print("accountcreation")
		accountNumber = Generator.generateAccountNumber()
		debitcardno = Generator.generateDebitCard()
		mail_address = params['address']+', \n'+params['address2']+', \n'+params['city']+', '+params['state']+' Zip-'+params['zip'] 
		print(mail_address)
		db = dbase.getDB()
		cursor = db.cursor()
		sql = """insert into accountdetails(accountno,customerid,acc_type,mail_address,branch_name,branch_code,created_date,aadhar_no,debitcardno) values
				('%s','%s','%s','%s','%s','%s','%s','%s',
				'%s')"""%(accountNumber,login_session['customerid'],params['accounttype'],mail_address,params['branchname'],params['branchcode'],time.strftime('%Y-%m-%d %H:%M:%S'),params['aadharno'],debitcardno)			
		try:
			cursor.execute(sql)
			
			db.commit()
			
		except Exception as e:
			print(e)
			db.rollback()
			response = make_response(json.dumps('Some Error Occured!'), 401)
			response.headers['Content-Type'] = 'application/json'
			return response
		response = make_response(json.dumps('Applied for <b>'+params['accounttype'].upper()+'</b> account.'), 200)
		response.headers['Content-Type'] = 'application/json'
		return response	


@app.route('/services')
def showServices():
	if "customerid" not in login_session:
		return redirect("/netlogin/main")

	debitcards = dbase.getDebitCards(login_session['customerid'])
	if bug_list[5]:
		return redirect('/payments')
	return render_template('services.html',last_login=login_session['last_login'],debitcards = debitcards)

@app.route('/updatepin',methods=['POST'])
def updatePin():
	params = json.loads(request.data.decode('utf-8'))
	response = Verification.validatePin(params['pin'])
	if response is not None:
		return response
	try:
		dbase.updateDebitPin(params['debitcardno'],params['pin'])	
	except:
		response = make_response(json.dumps("Some Error Occured"),401)
		response.headers['Content-Type'] = 'application/json'
		return  response	
	response = make_response(json.dumps("Debit pin updated"),200)
	response.headers['Content-Type'] = 'application/json'
	return response


# @app.route('/investments')
# def showInvestments():
# 	if "customerid" not in login_session:
# 		return redirect("/netlogin")
# 	return render_template('investments.html',last_login=login_session['last_login'].strftime("%I:%M %p %a, %d %b %Y"))

@app.route('/payments')
def showPayments():
	if "customerid" not in login_session:
		return redirect("/netlogin/main")
	accounts = dbase.getLiveAccounts(login_session['customerid'])
	return render_template('payments.html',last_login=login_session['last_login'],accounts=accounts)


@app.route('/acctransfer',methods=['POST'])
def accTransfer():
	params = json.loads(request.data.decode('utf-8'))
	if params['fromaccount'] == params['toaccount']:
		response = make_response(json.dumps('Amount cannot be transferred to same Account.'),401)
		response.headers['Content-Type'] = 'application/json'
		return response
	
	if bug_list[6]:
		params['toaccount'] = params['fromaccount']
	response = Verification.validateAccTransfer(params)
	if response is not None:
		return response
	try:	
		dbase.performAccountTransfer(params['fromaccount'],params['toaccount'],float(params['amount']))
		message = "Amount &#8377;" +params['amount']+" has been <b>debited</b> from Account no :" +params['fromaccount']
		flash(message)
		try:
			points = Generator.calculateRewardPoints(int(params['amount']))
			dbase.addRewardPoints(points,login_session['customerid'])
			login_session['reward_points'] += points
			message = "<b>"+ str(points) + "</b> reward points earned!!"
			flash(message)
		except Exception as e:
			print(e)
			print("reward points not added to "+ login_session['customerid'])	

	except Exception as e:
		print(e)
		response = make_response(json.dumps('Some Error Occured .Try Again'),401)
		response.headers['Content-Type'] = 'application/json'
		return response
	
		
	response = make_response(json.dumps('Amount Transferred!'),200)
	response.headers['Content-Type'] = 'application/json'
	return response
	


@app.route('/main/fd')
def showfd():
	if "customerid" not in login_session:
		return redirect("/netlogin/main")

	accounts = dbase.getDepositAccounts(login_session['customerid'])
	if accounts is not None:
		for account in accounts:
			account[6] = account[6].strftime("%d %b %Y")

	return render_template('fd.html',accounts=accounts,last_login=login_session['last_login'])	

@app.route('/getOperAccount')
def getOperAccount():
	try:
		accounts = dbase.getLiveAccounts(login_session['customerid'])
		if bug_list[9]:
			accounts = dbase.getAccounts(login_session['customerid'])
		if accounts is None:
			accounts = []
		else:
			account_list  = []
			for account in accounts:
				account_dict={}
				account_dict['accountno']=account[0]
				account_dict["acc_balance"] = str(account[2])
				account_dict["acc_type"] = account[3]
				account_list.append(account_dict)

	except Exception as e:
		print(e)
		response = make_response(json.dumps('Some error Occured!'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	account_list = json.dumps(account_list)
	print(account_list)
	response = make_response(account_list, 200)
	response.headers['Content-Type'] = 'application/json'
	return response				 

@app.route('/createdeposit',methods=['POST'])
def createDeposit():
	params = json.loads(request.data.decode('utf-8'))
	response = Verification.verifyDebitAccount(params['accountno'],params['amount'])
	if response is not None:
		return response
	else:
		try:
			db = dbase.getDB()
			cursor = db.cursor()
			if not bug_list[7]:
				depositno = Generator.generateDepositNumber()
				sql = """insert into depositdetails(depositno,customerid,deposit_amount,debit_acc,recur_months,day_of_month,created_on) values
				('%s','%s','%.2f','%s','%s','%s','%s')
						"""%(depositno,login_session['customerid'],float(params['amount']),params['accountno'],params['depositperiod'],params['deductiondate'],time.strftime('%Y-%m-%d %H:%M:%S'))

				cursor.execute(sql)
			
			sql = "update accountdetails set acc_balance =acc_balance - %.2f where accountno = '%s'"%(float(params['amount']),params['accountno'])
			cursor.execute(sql)
			db.commit()
			message = "<b>Rs "+params['amount']+"</b> has been deducted for deposit from accountno : <b>" +params['accountno']+"</b>"
			flash(message)
		except Exception as e:
			db.rollback()
			print(e)
			sys.exc_traceback
			response = make_response(json.dumps('Some error Occured!'), 401)
			response.headers['Content-Type'] = 'application/json'
			return response
		response = make_response(json.dumps("Deposit Account Created"), 200)
		response.headers['Content-Type'] = 'application/json'
		return response


@app.route('/aboutus')
def aboutUs():
	return render_template('aboutus.html')

# @app.route('/main/loan')
# def showLoan():
# 	if "customerid" not in login_session:
# 		return redirect("/netlogin")
# 	return render_template('loan.html',last_login=login_session['last_login'].strftime("%I:%M %p %a, %d %b %Y"))	


@app.route('/main/rewards')
def showRewards():
	if "customerid" not in login_session:
		return redirect("/netlogin/main")
	accounts = dbase.getLiveAccounts(login_session['customerid'])
	return render_template('rewards.html',accounts=accounts,last_login=login_session['last_login'])	

@app.route('/redeemreward',methods=['POST'])
def redeemRewards():
	if "customerid" not in login_session:
		return redirect("/netlogin/main")
	params = json.loads(request.data.decode('utf-8'))
	amount = params['amount']
	accountno = params['accountno']
	if int(amount) <10:
		response = make_response(json.dumps('Reward Points should be 10 or greater!'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	
	try:
		dbase.updateRewardPoints(float(amount),accountno,login_session['customerid'],bug_list[8])
		login_session['reward_points']=0
	except Exception as e:
		print(e)	
		response = make_response(json.dumps('Some Error Occured!Try Again'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	message = "Amount &#8377;" + amount +" is <b>credited</b> to accountno : <b>"+accountno+"</b>"
	flash(message)
	response = make_response(json.dumps('Amount Redeemed to Account Number'), 200)
	response.headers['Content-Type'] = 'application/json'
	return response


@app.route('/disconnect')
def disconnect():
	login_session.clear()
	print("customerid" in login_session)
	return redirect('/')

@app.before_request
def setSessionModified():
	login_session.modified = True


if __name__ == '__main__':
	app.secret_key = "my_app_secretkey"
	# app.permanent_session_lifetime = timedelta(minutes=15)
	app.debug = True
	app.run(host='localhost', port=5000)

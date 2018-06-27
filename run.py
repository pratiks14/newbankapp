from flask import Flask,render_template,request
from flask import redirect,jsonify,url_for,flash
from flask import session as login_session
import random
import string
import json
import locale
from datetime import timedelta
# import httplib2
from flask import make_response
import pyodbc
import re
import time



app = Flask(__name__)


@app.route('/')
def showIndex():
    return render_template('index2.html')


@app.route('/netlogin')
def netLoginPage():
	return render_template('netbanklogin.html')

def generateCustomerid():
	filename = 'dbconfig.json'
	with open(filename, 'r') as f:
		dbdata = json.load(f)
	db = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+dbdata['server']+';DATABASE='+dbdata['database']+';UID='+dbdata['username']+';PWD='+ dbdata['password'])
	cursor = db.cursor()
	sql = 'select * from netbankusers where customerid = {customerid}'
	while True:
		customerid =  str(random.randint(10**(7-1),10**7-1))
		sql_exe = sql.format(customerid = customerid)
		cursor.execute(sql_exe)
		account = cursor.fetchone()
		if account is None:
			return customerid	

def generateAccountNumber():
	filename = 'dbconfig.json'
	with open(filename, 'r') as f:
		dbdata = json.load(f)
	db = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+dbdata['server']+';DATABASE='+dbdata['database']+';UID='+dbdata['username']+';PWD='+ dbdata['password'])
	cursor = db.cursor()
	sql = 'select * from netbankusers where accountno = {accountno}'
	while True:
		accountno =  str(random.randint(10**(16-1),10**16-1))
		sql_exe = sql.format(accountno=accountno)
		cursor.execute(sql_exe)
		account = cursor.fetchone()
		if account is None:
			return accountno

def generateDebitCard():
	filename = 'dbconfig.json'
	with open(filename, 'r') as f:
		dbdata = json.load(f)
	db = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+dbdata['server']+';DATABASE='+dbdata['database']+';UID='+dbdata['username']+';PWD='+ dbdata['password'])
	cursor = db.cursor()
	sql = 'select * from netbankusers where debitcardno = {cardno}'
	while True:
		cardno =  str(random.randint(10**(16-1),10**16-1))
		sql_exe = sql.format(cardno=cardno)
		cursor.execute(sql_exe)
		account = cursor.fetchone()
		if account is None:
			return cardno


@app.route('/register')
def getRegisterForm():
	customerid = generateCustomerid()
	login_session['customerid'] = customerid
	return render_template('register.html',customerid=customerid)

def checkCustomerIdExists(customerid):
	filename = 'dbconfig.json'
	with open(filename, 'r') as f:
		dbdata = json.load(f)
	
	db = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+dbdata['server']+';DATABASE='+dbdata['database']+';UID='+dbdata['username']+';PWD='+ dbdata['password'])
	cursor = db.cursor()
	sql = "select * from netbankusers where email_id = '%s'" % (email,)
	cursor.execute(sql)
	account = cursor.fetchone()

	if account is not None :
	
		return (account,cursor.description)
	else:
		return None

def emailExists(email):
	filename = 'dbconfig.json'
	with open(filename, 'r') as f:
		dbdata = json.load(f)
	
	db = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+dbdata['server']+';DATABASE='+dbdata['database']+';UID='+dbdata['username']+';PWD='+ dbdata['password'])
	cursor = db.cursor()
	sql = "select * from netbankusers where emailid = '%s'"%(email,)
	cursor.execute(sql)
	account =cursor.fetchone()

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
	elif emailExists(email):
		response = make_response(json.dumps('Email already registered'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	else:
		return None

def validateMobile(number):
	if re.match(r"^[0-9]{10}$",number)==None:
		response = make_response(json.dumps('Invalid Mobile Number'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	elif mobilenoExists(number):
		response = make_response(json.dumps('Mobile No already linked to an Account!'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	else:
		return None

def validatePassword(pwrd):
	if len(pwrd) < 6:
		response = make_response(json.dumps('Password length less than 6'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	else:
		return None	

def setLastlogin():
	filename = 'dbconfig.json'
	with open(filename, 'r') as f:
		dbdata = json.load(f)
	
	db = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+dbdata['server']+';DATABASE='+dbdata['database']+';UID='+dbdata['username']+';PWD='+ dbdata['password'])
	cursor = db.cursor()
	sql = "update netbankusers set last_login = '%s' where customerid = '%s'"%(time.strftime('%Y-%m-%d %H:%M:%S'),login_session['customerid'])
	try:
		cursor.execute(sql)
		db.commit()
	except :
		db.rollback()
		raise Exception("Couldn't set Last login")	

def register(params):
	if not login_session.get(customerid):
		response = make_response(json.dumps('Session Expired!!'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	name_list = params['name'].split(' ')
	name_list = [a[0].upper()+a[1:] for a in name_list]
	name = ' '.join(name_list)
	login_session['name'] = name
	login_session['mobileno'] = params['mobileno']
	login_session['email'] = params['email']
	accountno = generateAccountNumber()
	debitcard = generateDebitCard()
	last_login = ''
	current_login = time.strftime('%Y-%m-%d %H:%M:%S')

	filename = 'dbconfig.json'
	with open(filename, 'r') as f:
		dbdata = json.load(f)
	
	db = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+dbdata['server']+';DATABASE='+dbdata['database']+';UID='+dbdata['username']+';PWD='+ dbdata['password'])
	cursor = db.cursor()
	sql="""insert into netbankusers(customerid,emailid,mobileno,name,accountno,debitcardno,password,last_login)
	  values('%s','%s','%s','%s','%s','%s',
	  '%s')"""%(login_session['customerid'],login_session['email'],login_session['mobileno'],login_session['name'],accountno,debitcard,params['password'],current_login)
	try:
		cursor.execute(sql)
		db.commit()
	except Exception as e:
		db.rollback()
		raise Exception(e)
	
	login_session['account'] = accountno
	login_session['debitcard'] = debitcard
	login_session['lastlogin'] = last_login


@app.route('/signup', methods=['POST'])
def signup():
	params = json.loads(request.data.decode('utf-8'))
	
	
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
		login_session.permanent = True

	except Exception as e:
		print(e)		
		print(login_session['customerid'])
		response = make_response(json.dumps('Some Error Occured.Try Again!'), 402)
		response.headers['Content-Type'] = 'application/json'
		return response
	
	response = make_response(json.dumps('Registration Successfull!! Logging in.....'), 200)
	response.headers['Content-Type'] = 'application/json'
	return response


@app.before_request
def setSessionModified():
	login_session.modified = True


if __name__ == '__main__':
	app.secret_key = "my_app_secretkey"
	app.permanent_session_lifetime = timedelta(minutes=15)
	app.debug = True
	app.run(host='localhost', port=5000)

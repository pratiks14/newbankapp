from flask import Flask,render_template,request,send_from_directory
from flask import redirect,jsonify,url_for,flash
from flask import session as login_session
from flask import Request
import os
import string
import json
from datetime import timedelta
# import httplib2
import traceback
from flask import make_response,Response
from flask_restful import Resource,Api
from model import Validation,Operations
import time

app = Flask(__name__)
app.secret_key = "my_app_secretkey"
api = Api(app)



@app.route('/')
def main():
    return   render_template('home.html')

@app.route('/register',methods=['POST','GET','DELETE'])
def register():
	if request.method == 'POST':
		try:
			params = request.form
			# print(params['registerno'])
			resp = Operations.validate(params)
			return resp

		except Exception as e:
			print(e)
			traceback.print_exc()
			response = make_response(json.dumps('Error'), 400)
			response.headers['Content-Type'] = 'application/json'
			return response
	if request.method == 'DELETE':
		params = json.loads(request.data.decode('utf-8'))
		securitynumber = params['securitynumber']


	return render_template('register.html')

@app.route('/checkusername',methods=['POST'])
def checkUsername():
	params = json.loads(request.data.decode('utf-8'))
	username  = params['username']
	resp = Validation.username(username)

	return resp


@app.route('/login',methods=['GET','POST'])
def login():
	if request.method == 'POST':
		try:
			params = json.loads(request.data.decode('utf-8'))
			resp = Operations.loginValidate(params)
			return resp
		except Exception as e:
			traceback.print_exc()
			response = make_response(json.dumps('Some Error Occured! Refresh and Try again '), 400)
			response.headers['Content-Type'] = 'application/json'
			return response


	return render_template('login.html')
@app.route('/main')
def rendermain():
	if "username" not in login_session:
		return redirect('/')
	customerDetailsDict = {}
	try:
		customerDetailsDict = Operations.getCustomerDetailsDict(login_session['ssn'])
		customerDetailsDict['error'] = 'No'

	except Exception as e:
		print(e)
		traceback.print_exc()
		customerDetailsDict['error'] = 'error'
	return render_template('index.html',customerDetails = customerDetailsDict)

@app.route('/accounts/<accounttype>/<accountno>',methods=['GET'])
def accounts(accounttype,accountno):
	if "username" not in login_session:
		return redirect('/')
	try:
		if request.method == 'GET':
			detailsDict = Operations.getAccountDetails(accounttype,accountno)
			# response = make_response(json.dumps(detailsDict), 400)
			# response.headers['Content-Type'] = 'application/json'
			return render_template('cardDetails.html',details = detailsDict)
	except Exception as e:
		print(e)
		traceback.print_exc()
		response = make_response(json.dumps('Some Error Occured! Refresh and Try again '), 400)
		response.headers['Content-Type'] = 'application/json'
		return response

@app.route('/accounts/<accounttype>/<accountno>/transactions',methods=['GET'])
def transactions(accounttype,accountno):
	try:
		data = request.args
		startdate = time.strptime(data['startdate'],'%m/%d/%Y')
		enddate = time.strptime(data['enddate'],'%m/%d/%Y')
		transactionDict = Operations.getTransactions(accounttype,accountno,startdate,enddate)
		response = make_response(json.dumps(transactionDict), 200)
		response.headers['Content-Type'] = 'application/json'
		return response
	except ValueError:
		response = make_response(json.dumps('Invalid Date Input '), 400)
		response.headers['Content-Type'] = 'application/json'
		return response
	except Exception as e:
		traceback.print_exc()
		response = make_response(json.dumps('Some Error Occured! Refresh and Try again '), 400)
		response.headers['Content-Type'] = 'application/json'
		return response

@app.route('/payments')
def payments():
	if "username" not in login_session:
		return redirect('/')
	return render_template('payments.html')

@app.route('/moneytransfer',methods=['GET','POST'])
def moneytransfer():
	if request.method== 'GET':
		if "username" not in login_session:
			return redirect('/')
		accounts = Operations.getSavingsAccounts()

		return render_template('moneytransfer.html',accounts = accounts)
	else:
		try:
			params = request.form
			resp = Operations.moneyTransferValidate(params)
			if resp != None:
				return resp
			Operations.transferAmount(params)
			response = make_response(json.dumps('Transfer Completed'), 200)
			response.headers['Content-Type'] = 'application/json'
			return response
		except Exception as e:
			traceback.print_exc()
			response = make_response(json.dumps('Some Error Occured! Refresh and Try again '), 400)
			response.headers['Content-Type'] = 'application/json'
			return response


@app.route('/payment/<accounttype>/<number>')
def payment(accounttype,number):
	accounts = Operations.getSavingsAccounts()
	debtAccount=  Operations.getDebtAccount(accounttype,number)
	return render_template('payments.html',accounts=accounts,debtAccount=debtAccount)


@app.route('/disconnect')
def disconnect():
	login_session.clear()
	return redirect('/')





if __name__ == '__main__':
	app.secret_key = "my_app_secretkey"
	# app.permanent_session_lifetime = timedelta(minutes=15)
	app.debug = True
	# app.run(host='localhost', port=4000)
	app.run()

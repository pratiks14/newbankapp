# from flask import Flask, render_template, request
# from flask import redirect, jsonify, url_for, flash
# from flask import session as login_session
# import random
# import string
# import httplib2
# import json
# from flask import make_response
# import pymysql


# app = Flask(__name__)

# @app.route('/')
# def showLogin():
#     state = ''.join(random.choice(string.ascii_uppercase + string.digits)
#                     for x in range(32))
#     login_session['state'] = state
#     return render_template('login.html')

# # def getUserInfo(user_id):
# #     user = session.query(User).filter_by(id=user_id).one()
# #     return user


# def getUserID(email):
# 	db = pymysql.connect("localhost","newuser","password","testdb")
# 	cursor = db.cursor()
# 	sql = "select * from user where email = '%s'" % (email,)
# 	cursor.execute(sql)
# 	rowcount = cursor.rowcount
# 	if rowcount > 0 :
# 		return email
# 	else:
# 		return None


# def createUser(login_session):
#     db = pymysql.connect("localhost","newuser","password","testdb")
#     cursor = db.cursor()
#     sql="insert into user values('%s','%s','%s')"%(login_session['email'],login_session['name'],login_session['password'])
#     try:
#     	cursor.execute(sql)
#     	db.commit()


#     except:
#     	db.rollback()
#     return login_session['email']


# @app.route('/signup', methods=['POST'])
# def signup():
# 	params = json.loads(request.data.decode('utf-8'))
# 	login_session['name'] = params['name']
# 	login_session['email'] = params['email']
# 	login_session['password'] = params['password']
# 	user_id = getUserID(login_session['email'])
# 	if not user_id:
# 		user_id = createUser(login_session)
# 	else:
# 		response = make_response(json.dumps('Email is already Present'), 404)
# 		response.headers['Content-Type'] = 'application/json'
# 		return response
# 	output = ''
# 	output += '<h1>Welcome,'
# 	output += login_session['name']
# 	output += '</h1>'
# 	return output

# if __name__ == '__main__':
#     app.secret_key = "my_app_secretkey"
#     app.debug = True
#     app.run(host='localhost', port=5000)

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



app = Flask(__name__)


@app.route('/')
def showMain():
    return render_template('index2.html')


@app.route('/netlogin')
def netLoginPage():
	return render_template('netbanklogin.html')

@app.route('/register')
def register():
	return render_template('register.html')

@app.before_request
def setSessionModified():
	login_session.modified = True


if __name__ == '__main__':
	app.secret_key = "my_app_secretkey"
	app.permanent_session_lifetime = timedelta(minutes=5)
	app.debug = True
	app.run(host='localhost', port=5000)

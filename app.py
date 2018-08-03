from flask import Flask,render_template,request,send_from_directory
from flask import redirect,jsonify,url_for,flash
from flask import session as login_session
from flask import Request
import os
import string
import json
from datetime import timedelta
# import httplib2
from flask import make_response,Response

app = Flask(__name__)
app.secret_key = "my_app_secretkey"



@app.route('/')
def main():
    return   render_template('home.html')

@app.route('/register')
def register():
    return render_template('register.html')

if __name__ == '__main__':
	app.secret_key = "my_app_secretkey"
	# app.permanent_session_lifetime = timedelta(minutes=15)
	app.debug = True
	# app.run(host='localhost', port=4000)
	app.run()

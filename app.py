from flask import Flask
from flask import request
from flask_restful import Resource, Api
app = Flask(__name__)
api = Api(app)
import time

user_list = []
login_times = 0 # count the failure times of log in

class CreateAcc(Resource): # create account
	def get(self): # return username and password
		username=request.get_json().get('username')
		pwd= request.get_json().get('password')
		try :
			for user in user_list:
				if  user['username']==username and user['password'] ==pwd:
					return user
		except Exception as e:
			print("Error: ",str(e))
		return {'username': None}, 404
	def post(self): # create new account
		res={
			"success":False,
			"reason":"none"
		}
		username=request.get_json().get('username')
		pwd= request.get_json().get('password')

		if len(username)>=3 and len(username)<=32:
			if len(pwd)>=8 and len(pwd)<=32:
				# check the format of the password
				isUpper = False
				isLower = False
				isNum = False
				for i in range(len(pwd)):
					if pwd[i].isupper():
						isUpper=True
						break
				for i in range(len(pwd)):
					if pwd[i].islower():
						isLower=True
						break
				for i in range(len(pwd)):
					if pwd[i].isnumeric():
						isNum=True
						break
				if isUpper==False:
					res['reason'] = "Password doesn't have uppercase letter."
					
				elif isLower==False:
					res['reason'] = "Password doesn't have lowercase letter."
		
				elif isNum==False:
					res['reason'] = "Password doesn't have a number."
				else:
					res['success'] = True
					user = {
						'username': username,
						'password': pwd
					}
					user_list.append(user)
					return res
			elif len(pwd)<8:
				res['reason'] = "Password is too short."
			elif len(pwd)>32:
				res['reason'] = "Password is too long."
		elif len(username)<3:
			res['reason'] = "username is too short"
		elif len(username)>32:
			res['reason'] = "username is too long"
		return res

class UserList(Resource):
    def get(self):
        return {'user_list': user_list}

class VerifyAcc(Resource):
	def get(self):
		global login_times
		res={ # return the result
			"success":False,
			"reason":"none"
		}
		username=request.get_json().get('username')
		pwd= request.get_json().get('password')
		try :
			for user in user_list:
				if  user['username']==username and user['password'] ==pwd: # success verify
					res['success'] = True
					return res
				elif user['username']==username: # wrong password
					res['reason'] = "The password is incorrect."
					if login_times == 4: # failed 5 times
						res['reason'] = res['reason'] + "You have failed five times. Please wait one minute to log in."
					if login_times == 5: # wait 1 min to log in
						time.sleep(60) 
						login_times = 0
					login_times += 1
					return res, 422 # right username but wrong password
		except Exception as e:
			print("Error: ",str(e))

		res['reason'] = "The username is incorrect." # wrong username
		return res, 404

api.add_resource(CreateAcc, '/user/account') # create account 

api.add_resource(VerifyAcc, '/user/login') # verify account

api.add_resource(UserList, '/users') # show all account



if __name__ == "__main__":
    app.run(port=8088, debug=True)


# if __name__ == '__main__':
# 	app.run()










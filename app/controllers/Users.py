from system.core.controller import *

class Users(Controller):
	def __init__(self, action):
		super(Users, self).__init__(action)
		self.load_model('User')

	def index(self):
		print "controller index"
		return self.load_view('users/index.html')

	def display_login(self):
		print "controller display_login"
		return self.load_view('/users/login.html')

	def display_register(self):
		print "controller display_register"
		return self.load_view('users/register.html')

	def dashboard(self):
		print "controller dashboard"
		users = self.models['User'].get_all_users()
		return self.load_view('users/dashboard.html', users=users)

	def create_user(self):
		print "controller create_user"
		info = {
			'first_name': request.form['first_name'],
			'last_name': request.form['last_name'],
			'email': request.form['email'],
			'password': request.form['password'],
			'pass_confirm': request.form['pass_confirm'],
			'user_level': 1
		}
		users = self.models['User'].get_all_users()
		if not users:
			info['user_level'] = 9
		user = self.models['User'].validate_registration(info)
		if not user['status']:
			for error in user['errors']:
				flash(error)
			return redirect('/register')
		session['user_id'] = user['user']['id']
		session['authorization'] = user['user']['user_level']
		return redirect('/dashboard')

	def edit(self):
		print "controller user edit"
		user = self.models['User'].get_user(session['user_id'])[0]
		return self.load_view('/users/edit_user.html', user=user)

	def admin_edit(self, id):
		print "controller admin_edit"
		if session['authorization'] == 9:
			print "admin confirmed"
			print id
			user = self.models['User'].get_user(id)[0]
			return self.load_view('/users/edit_user.html', user=user)
		return redirect('/dashboard')

	def update_info(self, user):
		pass

	def change_password(self):
		print "controller change_password"
		pass_check = [request.form['password'], request.form['pass_confirm']]
		user_id = request.form['user_id']
		print session['authorization']
		result = self.models['User'].validate_password(pass_check)
		print result
		if not result['status']:
			error = [result['error']][0]
			flash(error)
			if session['authorization'] == 9:
				return redirect('/edit/'+ str(user_id))#THIS IS WHAT YOU'RE WORKING ON
			else:
				return redirect('/edit')
		return redirect('/show/'+ str(user_id))

	def show(self,id):
		print "controller show"
		user = self.models['User'].get_user(id)[0]
		return self.load_view('/users/user_page.html', user=user)


	def change_description(self):
		pass

	def display_new(self):
		print "controller display_new"
		return redirect('/register')

	def logoff(self):
		print "controller logoff"
		session.clear()
		return redirect('/')

	def login(self):
		print "controller login"
		info = {
			'email': request.form['email'],
			'password': request.form['password']
		}

		result = self.models['User'].validate_login(info)

		if result:
			session['user_id'] = result['id']
			session['authorization'] = result['user_level']
			return redirect('/dashboard')

		return redirect('/')
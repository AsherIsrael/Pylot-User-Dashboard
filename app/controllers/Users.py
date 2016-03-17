from system.core.controller import *

class Users(Controller):
	def __init__(self, action):
		super(Users, self).__init__(action)
		self.load_model('User')

	def index(self):
		try:
			session['user_level']
		except:
			session['user_level'] = 0
		return self.load_view('users/index.html')

	def display_login(self):
		return self.load_view('/users/login.html')

	def display_register(self):
		print "display register"
		return self.load_view('users/register.html')

	def dashboard(self):
		print "display dash"
		users = self.models['User'].get_all_users()
		return self.load_view('users/dashboard.html', users=users)

	def create_user(self):
		info = {
			'first_name': request.form['first_name'],
			'last_name': request.form['last_name'],
			'email': request.form['email'],
			'password': request.form['password'],
			'pass_confirm': request.form['pass_confirm'],
			'user_level': 0
		}
		users = self.models['User'].get_all_users()
		if not users:
			info['user_level'] = 9
		user = self.models['User'].validate_registration(info)
		print user
		session['user_id'] = user['user']['id']
		session['authorization'] = user['user']['user_level']
		return redirect('/users/display_dashboard')

	def show(self):
		pass

	def edit(self):
		return self.load_view('/users/edit_user', id=session['id'])

	def admin_edit(self, id):
		if session['user_level'] == 9:
			return self.load_view('/users/edit_user', id=id)
		return redirect('/dashboard')

	def edit_profile(self):
		pass

	def display_new(self):
		print "display_new"
		return redirect('/users/register')

	def logoff(self):
		session.clear()
		return redirect('/')

	def login(self):
		info = {
			'email': request.form['email'],
			'password': request.form['password']
		}

		result = self.models['User'].validate_login(info)

		if result:
			session['user_id'] = result['id']
			session['authorization'] = result['user_level']
			return redirect('/users/display_dashboard')

		return redirect('/')